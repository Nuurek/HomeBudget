from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import F, Sum, Count
import json
from datetime import date, datetime, timedelta
import calendar
from collections import defaultdict

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
            )).order_by('-czas_zakupu')
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
        formset = CategoryFormSet(
            data=request.POST,
            queryset=KategorieZakupu.objects.all()
        )

        context = {
            'formset': formset
        }

        for key, value in request.POST.items():
            print(key, ": ", value)
        for form in formset:
            print(form)
            print("Valid? ", form.is_valid())
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
            error_code = str(error).partition(':')[0].partition('-')[2]

            error_messages = {
                "01400": "Sieć sklepów musi posiadać nazwę.",
                "00001": "Sieć sklepów o podanej nazwie już istnieje.",
            }

            messages.error(
                request,
                error_messages[error_code]
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

        self.brand_shops = Sklepy.objects.filter(
            sieci_sklepow_nazwa=self.brand
        )
        self.brand_shops_formset = ShopFormSet(
            data=request.POST,
            instance=self.brand,
            queryset=self.brand_shops
        )

        if "delete_brand" in request.POST:
            return self.delete_brand(request)
        else:
            if self.brand_shops_formset.is_valid():
                try:
                    new_brand_shops = self.brand_shops_formset.save()
                except:
                    messages.error(
                        request,
                        "Nie można usunąć jednego ze sklepów ze względu" +
                        " na istniejące paragony."
                    )
                    return HttpResponseRedirect(reverse(
                        "brand",
                        kwargs={
                            "brand_name": self.brand_name,
                        }
                    ))

                messages.success(
                    request,
                    "Sklepy zostały zaktualizowane."
                )

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
        new_brand_name = request.POST['nazwa']

        if new_brand_name == '':
            messages.error(
                request,
                "Sieć sklepów musi posiadać nazwę."
            )

        if new_brand_name != self.brand_name:
            print(self.brand_form)
            if self.brand_form.is_valid():
                new_brand = self.brand_form.save()
                for shop in self.brand_shops:
                    shop.sieci_sklepow_nazwa = new_brand
                    shop.save()
                self.brand.delete()
                self.brand_name = new_brand.nazwa
                messages.success(
                    request,
                    "Nazwa sieci została zmieniona."
                )

        return HttpResponseRedirect(reverse(
            "brand",
            kwargs={
                "brand_name": self.brand_name,
            }
        ))


class StatisticsView(TemplateView):
    template_name = "statistics.html"

    def get(self, request, *args, **kwargs):
        start_date, end_date = self._get_date_range(request=request)

        daily_expenses = self._get_daily_expenses(start_date, end_date)

        must_have_expenses = self._get_filtered_daily_expenses(
            start_date, end_date, False
        )

        optional_expenses = self._get_filtered_daily_expenses(
            start_date, end_date, True
        )

        must_have_sum = self._get_sum_of_expenses(must_have_expenses)
        optional_sum = self._get_sum_of_expenses(optional_expenses)
        total_sum = must_have_sum + optional_sum

        grouped_json_expenses = self._get_grouped_json_expenses(
            must_have_expenses,
            optional_expenses
        )

        context = {
            "daily_expenses": grouped_json_expenses,
            "total_sum": total_sum,
            "must_have_sum": must_have_sum,
            "optional_sum": optional_sum,
            "start_date": json.dumps(start_date.strftime("%Y-%m-%d")),
            "end_date": json.dumps(end_date.strftime("%Y-%m-%d")),
        }

        return self.render_to_response(context)

    def _get_date_range(self, request):
        try:
            end_date = datetime.strptime(
                request.GET.get('end-date'),
                "%d.%m.%Y"
            )
        except:
            end_date = datetime.now()

        try:
            start_date = datetime.strptime(
                request.GET.get('start-date'),
                "%d.%m.%Y"
            )
        except:
            start_date = end_date - timedelta(days=30)

        return start_date, end_date

    def _get_daily_expenses(self, start_date, end_date):
        queryset = self._get_daily_purchases(start_date, end_date)
        return self._sum_daily_totals(queryset)

    def _get_filtered_daily_expenses(self, start_date, end_date, optionality):
        queryset = self._get_daily_purchases(start_date, end_date)
        queryset = self._filter_expenses_by_optionality(queryset, optionality)
        return self._sum_daily_totals(queryset)

    def _sum_daily_totals(self, queryset):
        return queryset.annotate(total=Sum(
            F('zakupy__cena_jednostkowa')*F('zakupy__ilosc_produktu')
        )).order_by('-czas_zakupu')

    def _filter_expenses_by_optionality(self, queryset, optionality):
        return queryset.filter(
            zakupy__kategorie_zakupu_id__czy_opcjonalny=optionality
        )

    def _get_daily_purchases(self, start_date, end_date):
        return Paragony.objects.values(
            'czas_zakupu',
        ).filter(czas_zakupu__range=(
            start_date,
            end_date
        ))

    def _get_sum_of_expenses(self, expenses):
        return expenses.aggregate(sum=Sum('total'))['sum']

    def _get_grouped_json_expenses(self, must_have, optional):
        return json.dumps(
            self._queryset_to_json_vis_group(must_have, 0) +
            self._queryset_to_json_vis_group(optional, 1)
        )

    def _queryset_to_json_vis_group(self, queryset, group_id):
        vis_group = [{
            "x": expense["czas_zakupu"].strftime("%Y-%m-%d"),
            "y": expense["total"],
            "group": group_id,
        } for expense in queryset]

        return vis_group
