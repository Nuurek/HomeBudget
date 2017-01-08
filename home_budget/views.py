from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Paragony, SieciSklepow, Sklepy
from django.db.models.functions import Lower
import json


class BillCreateView(TemplateView):

    template_name = "bill_create.html"

    def get_context_data(self, **kwargs):
        context = super(BillCreateView, self).get_context_data(**kwargs)
        brands = SieciSklepow.objects.all().order_by(Lower('nazwa'))
        context['brands'] = brands
        shops = Sklepy.objects.all().order_by(Lower('adres'))
        brands_shops = {}
        for shop in shops:
            brand = shop.sieci_sklepow_nazwa.nazwa
            if brand not in brands_shops:
                brands_shops[brand] = []

            brands_shops[brand].append(shop.adres)
        context['shops'] = json.dumps(brands_shops)
        return context
