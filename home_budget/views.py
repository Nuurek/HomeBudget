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


class BillCreateView(TemplateView):

    template_name = "bill_create.html"

    def get_shops(self):
        shops = Sklepy.objects.all().values('sieci_sklepow_nazwa', 'adres').order_by('sieci_sklepow_nazwa', 'adres')

        brands_shops = defaultdict(list)
        for shop in shops:
            brand = shop['sieci_sklepow_nazwa']
            brands_shops[brand].append(shop['adres'])

        return json.dumps(brands_shops)

    def get(self, request, *args, **kwargs):
        bill_form = BillForm()

        purchase_formset = PurchaseFormSet()

        context = {
            'form': bill_form,
            'purchase_formset': purchase_formset,
            'shops': self.get_shops(),
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        bill_form = BillForm(data=request.POST)

        formset = PurchaseFormSet(data=request.POST)

        print("POST")
        print(request.POST)
        print("Bill: ", bill_form)
        print("Is valid: ", bill_form.is_valid())
        print("Purchases: ", formset)
        print("Is valid: ", formset.is_valid())

        if bill_form.is_valid() and formset.is_valid():
            bill = bill_form.save()
            purchases = formset.save(commit=False)
            for purchase in purchases:
                purchase.paragony = bill
                purchase.save()
            return HttpResponseRedirect(reverse('bill_create'))

        context = {
            'form': bill_form,
            'formset': formset,
            'shops': self.get_shops(),
        }
        return self.render_to_response(context)

class BillDetailsView(TemplateView):

    template_name = "bill_create.html"

    def get_shops(self):
        shops = Sklepy.objects.all().values('sieci_sklepow_nazwa', 'adres').order_by('sieci_sklepow_nazwa', 'adres')

        brands_shops = defaultdict(list)
        for shop in shops:
            brand = shop['sieci_sklepow_nazwa']
            brands_shops[brand].append(shop['adres'])

        return json.dumps(brands_shops)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        bill = Paragony.objects.get(id=pk)
        bill_form = BillForm(instance=bill)

        purchases = Zakupy.objects.filter(paragony=pk)

        purchase_formset = PurchaseRetrieveFormSet(instance=bill)

        context = {
            'form': bill_form,
            'purchase_formset': purchase_formset,
            'shops': self.get_shops(),
        }

        return self.render_to_response(context)
