from django.forms import modelformset_factory
from .models import ProductCategory
from .widgets import get_categories_widgets, get_categories_labels


CategoryFormSet = modelformset_factory(
    ProductCategory,
    fields=("name", "is_optional",),
    extra=0,
    can_delete=True,
    widgets=get_categories_widgets(),
    labels=get_categories_labels(),
)