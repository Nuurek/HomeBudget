from django.forms import ModelForm, ModelChoiceField, DateField
from .models import Paragony, Zakupy, Sklepy, SieciSklepow

class PurchaseForm(ModelForm):

    class Meta:
        model = Zakupy
        fields = ('nazwa_produktu', 'cena_jednostkowa', 'ilosc_produktu',
                    'kategorie_zakupu_nazwa', 'paragony')

class BillForm(ModelForm):

    brand = ModelChoiceField(queryset=SieciSklepow.objects.all())
    sklepy_adres = ModelChoiceField(queryset=Sklepy.objects.all(), disabled=False)
    czas_zakupu = DateField(input_formats=['%d/%m/%Y'], disabled=False)

    class Meta:
        model = Paragony
        exclude = ('brand',)


class ShopForm(ModelForm):

    class Meta:
        model = Sklepy
        fields = ('adres', 'sieci_sklepow_nazwa')
