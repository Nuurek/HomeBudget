from django.views.generic import TemplateView, DetailView
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from collections import defaultdict

from .models import Paragony, SieciSklepow, Sklepy, KategorieZakupu, Zakupy
from .forms import (
    PurchaseForm, BillForm, ShopForm, PurchaseFormSet,
    PurchaseRetrieveFormSet
)


class BillView(TemplateView):

    template_name = "bill_create.html"

    def get(self, request, bill=None,
        *args, **kwargs):

        initial_bill_data = {}

        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            bill = Paragony.objects.get(id=pk)
            shop = bill.sklepy_adres
            brand = shop.sieci_sklepow_nazwa
            PurchaseFormSet.extra = 0
            initial_bill_data['brand'] = brand
            initial_bill_data['sklepy_adres'] = shop
        else:
            PurchaseFormSet.extra = 1

        bill_form = BillForm(instance=bill, initial=initial_bill_data)

        purchase_formset = PurchaseFormSet(instance=bill)

        return self.render_context(bill_form, purchase_formset)

    def post(self, request, *args, **kwargs):

        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            bill = Paragony.objects.get(id=pk)
        else:
            bill = None

        bill_form = BillForm(data=request.POST, instance=bill)

        purchase_formset = PurchaseFormSet(data=request.POST)

        if bill_form.is_valid() and purchase_formset.is_valid():
            if 'pk' not in self.kwargs:
                bill = bill_form.save()
            old_purchases = Zakupy.objects.filter(paragony=bill)
            print(old_purchases)
            old_purchases.delete()
            purchases = purchase_formset.save(commit=False)
            for purchase in purchases:
                print(purchase)
                purchase.paragony = bill
                purchase.save()
            return HttpResponseRedirect(reverse('bill_details'), args=[pk])

        return self.render_context(bill_form, purchase_formset)

    def render_context(self, bill_form, purchase_formset):
        context = {
            'form': bill_form,
            'purchase_formset': purchase_formset,
            'shops': self._get_shops(),
        }

        return self.render_to_response(context)

    def _get_shops(self):
        shops = Sklepy.objects.all().values('sieci_sklepow_nazwa', 'adres').order_by('sieci_sklepow_nazwa', 'adres')

        brands_shops = defaultdict(list)
        for shop in shops:
            brand = shop['sieci_sklepow_nazwa']
            brands_shops[brand].append(shop['adres'])

        return json.dumps(brands_shops)
