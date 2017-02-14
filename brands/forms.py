from django.forms import ModelForm, CharField, inlineformset_factory
from django.forms.widgets import TextInput
from .models import Brand, Shop
from .widgets import get_shops_widgets


class BrandForm(ModelForm):

    class Meta:
        model = Brand
        fields = ("name",)

    name = CharField(
        label="Nazwa",
        label_suffix='',
        widget=TextInput(attrs={
            'class': 'form-control input-lg text-center',
            'readonly': False,
        })
    )


ShopFormSet = inlineformset_factory(
    Brand, Shop,
    exclude=(),
    can_delete=True,
    extra=0,
    widgets=get_shops_widgets(),
)
