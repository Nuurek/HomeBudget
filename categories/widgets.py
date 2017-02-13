from django.forms.widgets import TextInput, CheckboxInput


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