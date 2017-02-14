from django.views.generic import TemplateView, CreateView
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages


from .models import Brand, Shop
from .forms import BrandForm, ShopFormSet


class BrandListView(CreateView):
    model = Brand
    template_name = "brands.html"
    form_class = BrandForm

    def get_queryset(self):
        queryset = Brand.objects.all().annotate(
            shops_count=Count('shop')
        )
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = self.get_queryset()
        return super(BrandListView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        brand_form = BrandForm(request.POST)

        if brand_form.is_valid():
            brand_form.save()

            brand_name = brand_form.cleaned_data['name']

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
        else:
            messages.error(
                request,
                "Sieć sklepów musi posiadać nazwę."
            )
            return HttpResponseRedirect(reverse('brands'))


class BrandDetailView(TemplateView):
    template_name = "brand.html"

    def get(self, request, *args, **kwargs):
        brand_name = self.kwargs['brand_name']
        brand = Brand.objects.get(name=brand_name)
        brand_form = BrandForm(instance=brand)
        brand_shops = Shop.objects.filter(brand=brand)
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
        self.brand = Brand.objects.get(name=self.brand_name)

        self.brand_form = BrandForm(data=request.POST)

        self.brand_shops = Shop.objects.filter(
            brand=self.brand
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
        new_brand_name = request.POST['name']

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
                    shop.brand = new_brand
                    shop.save()
                self.brand.delete()
                self.brand_name = new_brand.name
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
from django.shortcuts import render

# Create your views here.
