from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from collections import defaultdict
from django.db.models import F, Sum

from .models import Paragony, SieciSklepow, Sklepy, KategorieZakupu, Zakupy
from .forms import (
    PurchaseForm, BillForm, ShopForm, PurchaseFormSet,
    PurchaseRetrieveFormSet
)


class BillCreateView(TemplateView):

    template_name = "bill.html"

    def __init__(self, *args, **kwargs):
        super(BillCreateView, self).__init__(*args, **kwargs)
        self.initial_number_of_rows = 1

    def get(self, request, bill=None, initial_bill_data=None, *args, **kwargs):
        bill_form = BillForm(instance=bill, initial=initial_bill_data)

        PurchaseFormSet.extra = self.initial_number_of_rows
        purchase_formset = PurchaseFormSet(instance=bill)

        return self.render_context(bill_form, purchase_formset)

    def post(self, request, bill=None, *args, **kwargs):
        bill_form = BillForm(data=request.POST, instance=bill)

        purchase_formset = PurchaseFormSet(data=request.POST)

        if bill_form.is_valid() and purchase_formset.is_valid():
            if bill is None:
                bill = bill_form.save()
            else:
                old_purchases = Zakupy.objects.filter(paragony=bill)
                old_purchases.delete()

            purchases = purchase_formset.save(commit=False)
            for purchase in purchases:
                purchase.paragony = bill
                purchase.save()

            pk = bill.id
            return HttpResponseRedirect(reverse('bill_detail', args=[pk]))

        return self.render_context(bill_form, purchase_formset)

    def render_context(self, bill_form, purchase_formset):
        context = {
            'form': bill_form,
            'purchase_formset': purchase_formset,
            'shops': self._get_shops(),
        }

        return self.render_to_response(context)

    def _get_shops(self):
        shops = Sklepy.objects.all().values('sieci_sklepow_nazwa', 'adres') \
                        .order_by('sieci_sklepow_nazwa', 'adres')

        brands_shops = defaultdict(list)
        for shop in shops:
            brand = shop['sieci_sklepow_nazwa']
            brands_shops[brand].append(shop['adres'])

        return json.dumps(brands_shops)


class BillDetailView(BillCreateView):

    template_name = "bill_create.html"

    def __init__(self, *args, **kwargs):
        super(BillDetailView, self).__init__(*args, **kwargs)
        self.initial_number_of_rows = 0

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        bill = Paragony.objects.get(id=pk)
        shop = bill.sklepy_adres
        brand = shop.sieci_sklepow_nazwa
        initial_bill_data = {}
        initial_bill_data['brand'] = brand
        initial_bill_data['sklepy_adres'] = shop

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


class BillListView(ListView):
    template_name = "home.html"

    def get_queryset(self):
        queryset = Paragony.objects.all().values(
            'id',
            'sklepy_adres',
            'czas_zakupu',
            'sklepy_adres__sieci_sklepow_nazwa'
            ).annotate(total=Sum(
                F('zakupy__cena_jednostkowa')*F('zakupy__ilosc_produktu')
            ))
        print(queryset)
        return queryset
