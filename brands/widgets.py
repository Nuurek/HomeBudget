from django.forms.widgets import TextInput, HiddenInput


def get_shops_widgets():
    return {
        'address': TextInput(attrs={
            'class': 'form-control',
        }),
        'id': HiddenInput(),
        'brand': HiddenInput(),
    }