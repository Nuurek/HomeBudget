from django.forms import ModelForm, ModelChoiceField, DateField, Select, TextInput
from .models import Paragony, Zakupy, Sklepy, SieciSklepow

class PurchaseForm(ModelForm):

    class Meta:
        model = Zakupy
        fields = ('nazwa_produktu', 'cena_jednostkowa', 'ilosc_produktu',
                    'kategorie_zakupu_nazwa', 'paragony')

class BillForm(ModelForm):

    class Meta:
        model = Paragony
        exclude = ('brand',)

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
        disabled=True,
        widget=Select(attrs={
            'class': 'form-control',
        })
    )
    czas_zakupu = DateField(input_formats=['%d/%m/%Y'],
        label="Data zakupu",
        label_suffix='',
        disabled=True,
        widget=TextInput(attrs={
            'class': 'form-control',
        })
    )


class ShopForm(ModelForm):

    class Meta:
        model = Sklepy
        fields = ('adres', 'sieci_sklepow_nazwa')
