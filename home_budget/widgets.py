from django.forms import (
    Select, TextInput, NumberInput, CheckboxInput, HiddenInput
)


def get_purchase_widgets():
    attrs = {
        'class': 'form-control',
        'required': 'required',
    }
    return {
        'nazwa_produktu': TextInput(attrs=attrs),
        'kategorie_zakupu_id': Select(attrs=attrs),
        'cena_jednostkowa': NumberInput(attrs=attrs),
        'ilosc_produktu': NumberInput(attrs=attrs),
    }


def get_purchase_labels():
    return {
        'nazwa_produktu': "Nazwa",
        'kategorie_zakupu_id': "Kategoria",
        'cena_jednostkowa': "Cena",
        'ilosc_produktu': "Ilość",
    }


def get_categories_widgets():
    return {
        'name': TextInput(attrs={
            'class': 'form-control',
        }),
        'is_optional': CheckboxInput(attrs={
            'class': '',
        }),
    }


def get_categories_labels():
    return {
        'name': "Nazwa",
        'is_optional': "Czy opcjonalne?",
    }


def get_shops_widgets():
    return {
        'address': TextInput(attrs={
            'class': 'form-control',
        }),
        'id': HiddenInput(),
        'brand': HiddenInput(),
    }
