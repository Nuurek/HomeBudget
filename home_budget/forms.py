from django.forms import (
    ModelForm, ModelChoiceField, DateField, Select, TextInput, CharField
)
from django.forms import (
    formset_factory, inlineformset_factory, modelformset_factory
)

from .models import Paragony, Zakupy, Sklepy, SieciSklepow, KategorieZakupu
from .widgets import (
    get_purchase_widgets, get_purchase_labels,
    get_categories_widgets, get_categories_labels,
    get_shops_widgets,
)


class BillForm(ModelForm):

    class Meta:
        model = Paragony
        exclude = ()

    brand = ModelChoiceField(
        queryset=SieciSklepow.objects.all(),
        label="Sieć sklepów",
        label_suffix='',
        widget=Select(attrs={
            'class': 'form-control',
        })
    )

    sklepy_id = ModelChoiceField(
        queryset=Sklepy.objects.all(),
        label="Sklep",
        label_suffix='',
        widget=Select(attrs={
            'class': 'form-control',
        })
    )

    czas_zakupu = DateField(
        input_formats=['%d/%m/%Y'],
        label="Data zakupu",
        label_suffix='',
        widget=TextInput(attrs={
            'class': 'form-control',
        })
    )


class ShopForm(ModelForm):

    class Meta:
        model = Sklepy
        fields = ('adres', 'sieci_sklepow_nazwa')

PurchaseFormSet = inlineformset_factory(
    Paragony, Zakupy,
    exclude=(), can_delete=True,
    widgets=get_purchase_widgets(),
    labels=get_purchase_labels(),
)


class PurchaseRetrieveFormSet(PurchaseFormSet):
    extra = 0
    can_delete = True


CategoryFormSet = modelformset_factory(
    KategorieZakupu,
    fields=('id', 'nazwa', 'czy_opcjonalny',),
    extra=0,
    can_delete=True,
    widgets=get_categories_widgets(),
    labels=get_categories_labels(),
)


class BrandForm(ModelForm):

    class Meta:
        model = SieciSklepow
        fields = ('nazwa',)

    nazwa = CharField(
        label="",
        label_suffix='',
        widget=TextInput(attrs={
            'class': 'form-control input-lg text-center',
            'readonly': '',
        })
    )


ShopFormSet = inlineformset_factory(
    SieciSklepow, Sklepy,
    exclude=(),
    can_delete=True,
    extra=0,
    widgets=get_shops_widgets(),
)
