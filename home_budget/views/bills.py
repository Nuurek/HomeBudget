from django.views.generic import TemplateView, ListView
from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from datetime import datetime

from ..models import Paragony, Zakupy, Sklepy
from ..forms import BillForm, PurchaseFormSet
from .common import DateRangeView, BillView


class BillCreateView(TemplateView, BillView):

    template_name = "bill.html"

    def __init__(self, *args, **kwargs):
        super(BillCreateView, self).__init__(*args, **kwargs)
        self.initial_number_of_rows = 1

    def get(self, request, bill=None, initial_bill_data=None, *args, **kwargs):
        bill_form = BillForm(instance=bill, initial=initial_bill_data)

        PurchaseFormSet.extra = self.initial_number_of_rows

        purchase_formset = PurchaseFormSet(
            instance=bill,
            queryset=Zakupy.objects.filter(paragony=bill)
        )

        return self.render_context(bill_form, purchase_formset)

    def post(self, request, bill=None, *args, **kwargs):
        bill_form = BillForm(data=request.POST, instance=bill)
        purchase_formset = PurchaseFormSet(
            data=request.POST,
            instance=bill,
            queryset=Zakupy.objects.filter(paragony=bill)
        )

        if bill_form.is_valid() and purchase_formset.is_valid():
            bill = bill_form.save()

            purchases = purchase_formset.save(commit=False)
            for purchase_for_deletion in purchase_formset.deleted_objects:
                purchase_for_deletion.delete()
            for purchase in purchases:
                purchase.paragony = bill
                try:
                    purchase.save()
                except IntegrityError as error:
                    messages.error(
                        request,
                        "Błędne dane zakupu!"
                    )

            purchases = Zakupy.objects.filter(paragony=bill)

            if len(purchases) > 0:
                pk = bill.id
                print("Bill again: ", bill)
                return HttpResponseRedirect(reverse('bill_detail', args=[pk]))
            else:
                bill.delete()
                return self.render_context(bill_form, purchase_formset)

        return self.render_context(bill_form, purchase_formset)

    def render_context(self, bill_form, purchase_formset):
        context = {
            'form': bill_form,
            'purchase_formset': purchase_formset,
            'shops': self._get_shops(),
        }

        return self.render_to_response(context)


class BillDetailView(BillCreateView):

    template_name = "bill_create.html"

    def __init__(self, *args, **kwargs):
        super(BillDetailView, self).__init__(*args, **kwargs)
        self.initial_number_of_rows = 0

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        bill = Paragony.objects.get(id=pk)
        shop = Sklepy.objects.get(id=bill.sklepy_id.id)
        brand = shop.adres
        initial_bill_data = {}
        initial_bill_data['brand'] = shop.sieci_sklepow_nazwa
        initial_bill_data['sklepy_adres'] = shop.adres

        return super(BillDetailView, self).get(
            request, bill=bill, initial_bill_data=initial_bill_data,
            *args, **kwargs
        )

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        bill = Paragony.objects.get(id=pk)

        return super(BillDetailView, self).post(
            request, bill=bill, *args, **kwargs
        )


class BillListView(ListView, DateRangeView, BillView):
    template_name = "bill_list.html"

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)

        context['start_date'] = self.start_date.strftime("%d.%m.%Y")
        context['end_date'] = self.end_date.strftime("%d.%m.%Y")
        context['query'] = '&start-date=' + context['start_date'] + \
            '&end-date=' + context['end_date']
        return context

    def get_queryset(self):
        self.start_date, self.end_date = self._get_date_range(
            self.request, "start-date", "end-date", "%d.%m.%Y", 30
        )

        queryset = Paragony.objects.all().values(
            'id',
            'sklepy_id__adres',
            'czas_zakupu',
            'sklepy_id__sieci_sklepow_nazwa'
            ).filter(czas_zakupu__range=(
                self.start_date, self.end_date
            )).annotate(total=Sum(
                F('zakupy__cena_jednostkowa')*F('zakupy__ilosc_produktu')
            )).order_by('-czas_zakupu')

        return queryset
