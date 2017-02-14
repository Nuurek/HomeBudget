from django.forms import ModelForm, ModelChoiceField, inlineformset_factory
from django.forms.fields import DateField
from django.forms.widgets import Select, DateInput
from datetime import date
from brands.models import Brand, Shop
from .models import Receipt, Purchase
from .widgets import (
    get_purchase_widgets, get_purchase_labels,
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

    shop = ModelChoiceField(
        queryset=Shop.objects.all(),
        label="Sklep",
        label_suffix='',
        widget=Select(attrs={
            'class': 'form-control',
        })
    )

    time_of_purchase = DateField(
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
