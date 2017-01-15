from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
import json
from collections import defaultdict
from django.db.models import F, Sum, Count

from .models import Paragony, SieciSklepow, Sklepy, KategorieZakupu, Zakupy
from .forms import (
    BillForm, ShopForm, PurchaseFormSet, PurchaseRetrieveFormSet,
    CategoryFormSet, BrandForm, ShopFormSet
)


class BillCreateView(TemplateView):

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
        print("Bill form: \n", bill_form.is_valid(), "\n", bill_form)
        print("\nFormset: ", purchase_formset.is_valid())
        if bill_form.is_valid() and purchase_formset.is_valid():
            if bill is None:
                print(bill_form.data)
                bill = bill_form.save()

            purchases = purchase_formset.save(commit=False)
            for purchase_for_deletion in purchase_formset.deleted_objects:
                purchase_for_deletion.delete()
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
        shops = Sklepy.objects.all() \
                        .values('sieci_sklepow_nazwa', 'id', 'adres') \
                        .order_by('sieci_sklepow_nazwa', 'adres')

        brands_shops = defaultdict(list)
        for shop in shops:
            brand = shop['sieci_sklepow_nazwa']
            brands_shops[brand].append({
                'id': shop['id'],
                'address': shop['adres']
            })

        return json.dumps(brands_shops)


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


class BillListView(ListView):
    template_name = "home.html"

    def get_queryset(self):
        queryset = Paragony.objects.all().values(
            'id',
            'sklepy_id__adres',
            'czas_zakupu',
            'sklepy_id__sieci_sklepow_nazwa'
            ).annotate(total=Sum(
                F('zakupy__cena_jednostkowa')*F('zakupy__ilosc_produktu')
            ))
        return queryset


class CategoryListView(TemplateView):
    template_name = "categories.html"

    def get(self, request, *args, **kwargs):
        formset = CategoryFormSet()

        context = {
            'formset': formset
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        formset = CategoryFormSet(data=request.POST)

        context = {
            'formset': formset
        }

        if formset.is_valid():
            try:
                formset.save()
            except IntegrityError as error:
                message = messages.error(
                    request,
                    'Jedna z kategorii posiada przypisane zakupy.'
                )
                return self.render_to_response(context)
            return HttpResponseRedirect(reverse('categories'))
        else:
            return self.render_to_response(context)


class BrandListView(ListView):
    template_name = "brands.html"

    model = SieciSklepow

    def get_queryset(self):
        queryset = SieciSklepow.objects.all().annotate(
            shops_count=Count('sklepy')
        )
        return queryset

    def post(self, request, *args, **kwargs):
        brand_name = request.POST['brand-name']

        try:
            SieciSklepow.objects.create(nazwa=brand_name)
        except IntegrityError as error:
            messages.error(
                request,
                'Sieć o podanej nazwie już istnieje.'
            )
            return HttpResponseRedirect(reverse('brands'))
        else:
            messages.success(
                request,
                "Sieć sklepów " + brand_name + " została stworzona."
            )
            return HttpResponseRedirect(reverse(
                "brand",
                kwargs={
                    "brand_name": brand_name,
                }
            ))


class BrandDetailView(TemplateView):
    template_name = "brand.html"

    def get(self, request, *args, **kwargs):
        brand_name = self.kwargs['brand_name']
        brand = SieciSklepow.objects.get(nazwa=brand_name)
        brand_form = BrandForm(instance=brand)
        brand_shops = Sklepy.objects.filter(sieci_sklepow_nazwa=brand)
        if len(brand_shops) == 0:
            ShopFormSet.extra = 1
        else:
            ShopFormSet.extra = 0

        brand_shops = ShopFormSet(
            instance=brand,
            queryset=brand_shops,
        )

        context = {
            "brand_form": brand_form,
            "brand_shops": brand_shops,
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.brand_name = self.kwargs['brand_name']
        self.brand = SieciSklepow.objects.get(nazwa=self.brand_name)

        self.brand_form = BrandForm(data=request.POST)

        self.brand_shops = Sklepy.objects.filter(sieci_sklepow_nazwa=self.brand)
        self.brand_shops_formset = ShopFormSet(
            data=request.POST,
            instance=self.brand,
            queryset=self.brand_shops
        )

        if "delete_brand" in request.POST:
            return self.delete_brand(request)
        else:
            if self.brand_shops_formset.is_valid():
                new_brand_shops = self.brand_shops_formset.save()

            return self.change_brand_name(request)

    def delete_brand(self, request):
        try:
            for shop in self.brand_shops:
                shop.delete()
            self.brand.delete()
        except IntegrityError as error:
            messages.error(
                request,
                "Nie można usunąć sieci " + self.brand_name +
                ". Do jednego ze sklepów jest przypisany zakup."
            )
            return HttpResponseRedirect(reverse(
                "brand",
                kwargs={
                    "brand_name": self.brand_name,
                }
            ))
        else:
            messages.success(
                request,
                'Sieć sklepów ' + self.brand_name +
                ' została pomyślnie usunięta.'
            )
            return HttpResponseRedirect(reverse('brands'))

    def change_brand_name(self, request):
        if request.POST['nazwa'] != self.brand_name:
            print("Different names")
            print(self.brand_form)
            if self.brand_form.is_valid():
                print("Valid")
                new_brand = self.brand_form.save()
                for shop in self.brand_shops:
                    shop.sieci_sklepow_nazwa = new_brand
                    shop.save()
                self.brand.delete()
                self.brand_name = new_brand.nazwa

        return HttpResponseRedirect(reverse(
            "brand",
            kwargs={
                "brand_name": self.brand_name,
            }
        ))
