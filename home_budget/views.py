from django.views.generic import TemplateView
from django.db.models.functions import Lower
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

from .models import Paragony, SieciSklepow, Sklepy, KategorieZakupu, Zakupy
from .forms import PurchaseForm, BillForm, ShopForm
from .widgets import get_purchase_widgets, get_purchase_labels

class BillCreateView(TemplateView):

    template_name = "bill_create.html"

    def get_context_data(self, **kwargs):
        context = super(BillCreateView, self).get_context_data(**kwargs)

        context['brands'] = self.get_brands()
        context['shops'] = self.get_shops()
        context['categories'] = self.get_categories()

        return context

    def get_brands(self):
        return SieciSklepow.objects.all().order_by(Lower('nazwa'))

    def get_shops(self):
        shops = Sklepy.objects.all().order_by(Lower('adres'))
        brands_shops = {}
        for shop in shops:
            brand = shop.sieci_sklepow_nazwa.nazwa
            if brand not in brands_shops:
                brands_shops[brand] = []

            brands_shops[brand].append(shop.adres)

        return json.dumps(brands_shops)

    def get_categories(self):
        return KategorieZakupu.objects.all().order_by(Lower('nazwa'))


class BillFormView(TemplateView):

    template_name = "bill_create.html"

    def get(self, request, *args, **kwargs):
        bill_form = BillForm()

        PurchaseFormSet = inlineformset_factory(Paragony, Zakupy,
            exclude=(), extra=1, can_delete=False,
            widgets=get_purchase_widgets(),
            labels=get_purchase_labels(),
        )
        purchase_formset = PurchaseFormSet()

        context = {
            'form': bill_form,
            'purchase_formset': purchase_formset,
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        bill_form = BillForm(data=request.POST)
        
        PurchaseFormSet = inlineformset_factory(Paragony, Zakupy,
            exclude=(), can_delete=False,
            widgets=get_purchase_widgets(),
            labels=get_purchase_labels(),
        )
        formset = PurchaseFormSet(data=request.POST)

        if bill_form.is_valid() and formset.is_valid():
            bill = bill_form.save()
            purchases = formset.save(commit=False)
            for purchase in purchases:
                purchase.paragony = bill
                purchase.save()
            return HttpResponseRedirect(reverse('bill_create'))

        context = {
            'form': bill_form,
            'formset': formset

        }
        return self.render_to_response(context)
