from django.views.generic import TemplateView
from django.db.models import F, Sum, Count
from decimal import *
import json

from receipts.models import Receipt
from .common import DateRangeView


class StatisticsView(TemplateView, DateRangeView):
    template_name = "statistics.html"

    def get(self, request, *args, **kwargs):
        start_date, end_date = self._get_date_range(
            request, "start-date", "end-date", "%d.%m.%Y", 30
        )

        daily_expenses = self._get_daily_expenses(start_date, end_date)

        must_have_expenses = self._get_filtered_daily_expenses(
            start_date, end_date, False
        )

        optional_expenses = self._get_filtered_daily_expenses(
            start_date, end_date, True
        )

        must_have_sum = self._get_sum_of_expenses(must_have_expenses) or Decimal(0)
        optional_sum = self._get_sum_of_expenses(optional_expenses) or Decimal(0)
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

    def _get_daily_expenses(self, start_date, end_date):
        queryset = self._get_daily_purchases(start_date, end_date)
        return self._sum_daily_totals(queryset)

    def _get_filtered_daily_expenses(self, start_date, end_date, optionality):
        queryset = self._get_daily_purchases(start_date, end_date)
        queryset = self._filter_expenses_by_optionality(queryset, optionality)
        return self._sum_daily_totals(queryset)

    def _sum_daily_totals(self, queryset):
        return queryset.annotate(total=Sum(
            F('purchase__unit_price')*F('purchase__amount')
        )).order_by('-time_of_purchase')

    def _filter_expenses_by_optionality(self, queryset, optionality):
        return queryset.filter(
            purchase__product_category__is_optional=optionality
        )

    def _get_daily_purchases(self, start_date, end_date):
        return Receipt.objects.values(
            'time_of_purchase',
        ).filter(time_of_purchase__range=(
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
            "x": expense["time_of_purchase"].strftime("%Y-%m-%d"),
            "y": str(expense["total"]),
            "group": group_id,
        } for expense in queryset]

        return vis_group
