from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView
from .models import Paragony, SieciSklepow, Sklepy, KategorieZakupu, Zakupy
from .forms import PurchaseForm, BillForm
from django.db.models.functions import Lower
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect
import json


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

    template_name = "paragony_form.html"

    def get(self, request, *args, **kwargs):
        "GET forms ready!"
        bill_form = BillForm()
        PurchaseFormSet = inlineformset_factory(Paragony, Zakupy, exclude=('id',),
                            extra=1)

        formset = PurchaseFormSet()
        context = {'form': bill_form, 'formset': formset}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        "Handle form submission on POST request"
        bill_form = BillForm(data=request.POST)
        PurchaseFormSet = inlineformset_factory(Paragony, Zakupy, exclude=('id',))
        formset = PurchaseFormSet(data=request.POST)
        if bill_form.is_valid() and formset.is_valid():
            bill = bill_form.save()
            purchases = formset.save(commit=False)
            for purchase in purchases:
                purchase.paragony = bill
                purchase.save()
            # TODO use reverse('name_of_the_view_to_redirect_to') instead of '/'
            return HttpResponseRedirect('/form')
        context = {'form': bill_form, 'formset': formset}
        return self.render_to_response(context)
