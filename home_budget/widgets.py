from django.forms import (
    Select, TextInput, NumberInput, CheckboxInput, HiddenInput
)


def get_purchase_widgets():
    attributes = {
        'class': 'form-control',
        'required': 'required',
    }
    return {
        'name': TextInput(attrs=attributes),
        'product_category': Select(attrs=attributes),
        'unit_price': NumberInput(attrs=attributes),
        'amount': NumberInput(attrs=attributes),
    }


def get_purchase_labels():
    return {
        'name': "Nazwa",
        'product_category': "Kategoria",
        'unit_price': "Cena",
        'amount': "Ilość",
    }
