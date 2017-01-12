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

    def get(self, request, instance=None, Formset=PurchaseFormSet,
        *args, **kwargs):
        bill_form = BillForm(data=None, instance=instance)

        purchase_formset = Formset(data=None, instance=instance)

        return self.render_context(bill_form, purchase_formset)

    def post(self, request, *args, **kwargs):
        bill_form = BillForm(data=request.POST)

        purchase_formset = PurchaseFormSet(data=request.POST)

        if bill_form.is_valid() and purchase_formset.is_valid():
            bill = bill_form.save()
            purchases = purchase_formset.save(commit=False)
            for purchase in purchases:
                purchase.paragony = bill
                purchase.save()
            return HttpResponseRedirect(reverse('bill_create'))

        return self.render_context(bill_form, purchase_formset)

    def render_context(self, bill_form, purchase_formset):
        print(bill_form)
        print(purchase_formset)

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


class BillDetailsView(BillCreateView):

    template_name = "bill_details.html"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        bill = Paragony.objects.get(id=pk)

        return super(BillDetailsView, self).get(request, bill, PurchaseRetrieveFormSet, *args, **kwargs)
