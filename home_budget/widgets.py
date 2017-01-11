from django.forms import Select, TextInput, NumberInput


def get_purchase_widgets():
    attrs = {
        'class': 'form-control',
    }
    return {
        'nazwa_produktu': TextInput(attrs=attrs),
        'kategorie_zakupu_nazwa': Select(attrs=attrs),
        'cena_jednostkowa': NumberInput(attrs=attrs),
        'ilosc_produktu': NumberInput(attrs=attrs),
    }

def get_purchase_labels():
    return {
        'nazwa_produktu': "Nazwa",
        'kategorie_zakupu_nazwa': "Kategoria",
        'cena_jednostkowa': "Cena",
        'ilosc_produktu': "Ilość",
    }
