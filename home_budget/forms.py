from django.forms import (
    ModelForm, ModelChoiceField, DateField, Select, TextInput, CharField,
    DateInput
)
from django.forms import (
    formset_factory, inlineformset_factory, modelformset_factory
)
from datetime import date

from .models import Receipt, Purchase, Shop, Brand, ProductCategory
from .widgets import (
    get_purchase_widgets, get_purchase_labels,
    get_categories_widgets, get_categories_labels,
    get_shops_widgets,
)


class BillForm(ModelForm):

    class Meta:
        model = Receipt
        exclude = ()

    brand = ModelChoiceField(
        queryset=Brand.objects.all(),
        label="Sieć sklepów",
        label_suffix='',
        widget=Select(attrs={
            'class': 'form-control',
        })
    )

    sklepy_id = ModelChoiceField(
        queryset=Shop.objects.all(),
        label="Sklep",
        label_suffix='',
        widget=Select(attrs={
            'class': 'form-control',
        })
    )

    czas_zakupu = DateField(
        input_formats=['%d.%m.%Y'],
        label="Data zakupu",
        label_suffix='',
        initial=date.today,
        widget=DateInput(attrs={
            'class': 'form-control',
            'format': "%d.%m.%Y",
        })
    )


PurchaseFormSet = inlineformset_factory(
    Receipt, Purchase,
    exclude=(), can_delete=True,
    widgets=get_purchase_widgets(),
    labels=get_purchase_labels(),
)


class PurchaseRetrieveFormSet(PurchaseFormSet):
    extra = 0
    can_delete = True


CategoryFormSet = modelformset_factory(
    ProductCategory,
    fields=("name", "is_optional",),
    extra=0,
    can_delete=True,
    widgets=get_categories_widgets(),
    labels=get_categories_labels(),
)


class BrandForm(ModelForm):

    class Meta:
        model = Brand
        fields = ("name",)

    name = CharField(
        label="",
        label_suffix='',
        widget=TextInput(attrs={
            'class': 'form-control input-lg text-center',
            'readonly': '',
        })
    )


ShopFormSet = inlineformset_factory(
    Brand, Shop,
    exclude=(),
    can_delete=True,
    extra=0,
    widgets=get_shops_widgets(),
)
