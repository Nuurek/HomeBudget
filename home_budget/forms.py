from django.forms import ModelForm, ModelChoiceField, DateField, Select, TextInput
from django.forms import formset_factory, inlineformset_factory, modelformset_factory

from .models import Paragony, Zakupy, Sklepy, SieciSklepow, KategorieZakupu
from .widgets import get_purchase_widgets, get_purchase_labels


class PurchaseForm(ModelForm):

    class Meta:
        model = Zakupy
        fields = ('nazwa_produktu', 'cena_jednostkowa', 'ilosc_produktu',
                    'kategorie_zakupu_nazwa', 'paragony')

class BillForm(ModelForm):

    class Meta:
        model = Paragony
        exclude = ()

    brand = ModelChoiceField(queryset=SieciSklepow.objects.all(),
        label="Sieć sklepów",
        label_suffix='',
        widget=Select(attrs={
            'class': 'form-control',
        })
    )
    sklepy_adres = ModelChoiceField(queryset=Sklepy.objects.all(),
        label="Sklep",
        label_suffix='',
        widget=Select(attrs={
            'class': 'form-control',
        })
    )
    czas_zakupu = DateField(input_formats=['%d/%m/%Y'],
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
    exclude=(), can_delete=False,
    widgets=get_purchase_widgets(),
    labels=get_purchase_labels(),
)


class PurchaseRetrieveFormSet(PurchaseFormSet):
    extra = 0
    can_delete = True


CategoryFormSet = modelformset_factory(
    KategorieZakupu,
    fields=('nazwa', 'czy_opcjonalny'),
)
