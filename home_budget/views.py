from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Paragony, SieciSklepow, Sklepy, KategorieZakupu
from django.db.models.functions import Lower
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
