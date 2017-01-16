from django.views.generic import TemplateView
from django.db.models import F, Sum, Count
import json
from datetime import date, datetime, timedelta
import calendar

from ..models import Paragony


class StatisticsView(TemplateView):
    template_name = "statistics.html"

    def get(self, request, *args, **kwargs):
        start_date, end_date = self._get_date_range(request=request)

        daily_expenses = self._get_daily_expenses(start_date, end_date)

        must_have_expenses = self._get_filtered_daily_expenses(
            start_date, end_date, False
        )

        optional_expenses = self._get_filtered_daily_expenses(
            start_date, end_date, True
        )

        must_have_sum = self._get_sum_of_expenses(must_have_expenses)
        optional_sum = self._get_sum_of_expenses(optional_expenses)
        total_sum = must_have_sum + optional_sum

        grouped_json_expenses = self._get_grouped_json_expenses(
            must_have_expenses,
            optional_expenses
        )

        context = {
            "daily_expenses": grouped_json_expenses,
            "total_sum": total_sum,
            "must_have_sum": must_have_sum,
            "optional_sum": optional_sum,
            "start_date": json.dumps(start_date.strftime("%Y-%m-%d")),
            "end_date": json.dumps(end_date.strftime("%Y-%m-%d")),
        }

        return self.render_to_response(context)

    def _get_date_range(self, request):
        try:
            end_date = datetime.strptime(
                request.GET.get('end-date'),
                "%d.%m.%Y"
            )
        except:
            end_date = datetime.now()

        try:
            start_date = datetime.strptime(
                request.GET.get('start-date'),
                "%d.%m.%Y"
            )
        except:
            start_date = end_date - timedelta(days=30)

        return start_date, end_date

    def _get_daily_expenses(self, start_date, end_date):
        queryset = self._get_daily_purchases(start_date, end_date)
        return self._sum_daily_totals(queryset)

    def _get_filtered_daily_expenses(self, start_date, end_date, optionality):
        queryset = self._get_daily_purchases(start_date, end_date)
        queryset = self._filter_expenses_by_optionality(queryset, optionality)
        return self._sum_daily_totals(queryset)

    def _sum_daily_totals(self, queryset):
        return queryset.annotate(total=Sum(
            F('zakupy__cena_jednostkowa')*F('zakupy__ilosc_produktu')
        )).order_by('-czas_zakupu')

    def _filter_expenses_by_optionality(self, queryset, optionality):
        return queryset.filter(
            zakupy__kategorie_zakupu_id__czy_opcjonalny=optionality
        )

    def _get_daily_purchases(self, start_date, end_date):
        return Paragony.objects.values(
            'czas_zakupu',
        ).filter(czas_zakupu__range=(
            start_date,
            end_date
        ))

    def _get_sum_of_expenses(self, expenses):
        return expenses.aggregate(sum=Sum('total'))['sum']

    def _get_grouped_json_expenses(self, must_have, optional):
        return json.dumps(
            self._queryset_to_json_vis_group(must_have, 0) +
            self._queryset_to_json_vis_group(optional, 1)
        )

    def _queryset_to_json_vis_group(self, queryset, group_id):
        vis_group = [{
            "x": expense["czas_zakupu"].strftime("%Y-%m-%d"),
            "y": expense["total"],
            "group": group_id,
        } for expense in queryset]

        return vis_group
