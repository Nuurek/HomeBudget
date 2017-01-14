from django.conf.urls import url
from .views import (
    BillCreateView, BillDetailView, BillListView, CategoryListView,
    BrandListView, ShopListView
)


urlpatterns = [
    url(r'^$', BillListView.as_view()),
    url(r'^bills/create', BillCreateView.as_view(), name='bill_create'),
    url(
        r'^bills/(?P<pk>[0-9]+)',
        BillDetailView.as_view(),
        name='bill_detail'
    ),
    url(r'^categories', CategoryListView.as_view(), name='categories'),
    url(r'^brands', BrandListView.as_view(), name='brands'),
    url(r'^shops', ShopListView.as_view(), name='shops'),
]
