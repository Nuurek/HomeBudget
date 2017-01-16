from django.conf.urls import url
from .views.bills import BillCreateView, BillDetailView, BillListView
from .views.categories import CategoryListView
from .views.brands import BrandListView, BrandDetailView
from .views.statistics import StatisticsView


urlpatterns = [
    url(r'^$', BillListView.as_view(), name="home"),
    url(r'^bills/create/$', BillCreateView.as_view(), name='bill_create'),
    url(
        r'^bills/(?P<pk>[0-9]+)',
        BillDetailView.as_view(),
        name='bill_detail'
    ),
    url(r'^categories/$', CategoryListView.as_view(), name='categories'),
    url(r'^brands/$', BrandListView.as_view(), name='brands'),
    url(
        r'^brands/(?P<brand_name>.+)',
        BrandDetailView.as_view(),
        name='brand'
    ),
    url(r'^statistics/$', StatisticsView.as_view(), name='statistics'),
]
