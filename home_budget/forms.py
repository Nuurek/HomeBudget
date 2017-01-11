from django.forms import ModelForm
from .models import Paragony, Zakupy

class PurchaseForm(ModelForm):

    class Meta:
        model = Zakupy
        fields = ('nazwa_produktu', 'cena_jednostkowa', 'ilosc_produktu',
                    'kategorie_zakupu_nazwa', 'paragony')

class BillForm(ModelForm):

    class Meta:
        model = Paragony
        fields = ('czas_zakupu', 'sklepy_adres')
