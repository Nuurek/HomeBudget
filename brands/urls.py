from django.conf.urls import url
from .views import BrandListView, BrandDetailView


urlpatterns = [
    url(r'^$', BrandListView.as_view(), name='brands'),
    url(
        r'^(?P<brand_name>.+)',
        BrandDetailView.as_view(),
        name='brand'
    ),
]