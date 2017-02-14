from django.conf.urls import url, include
from .views.bills import BillCreateView, BillDetailView, BillListView
from .views.statistics import StatisticsView


urlpatterns = [
    url(r'^$', BillListView.as_view(is_form=False), name="home"),
    url(r'^bills/create/$', BillCreateView.as_view(), name='bill_create'),
    url(
        r'^bills/(?P<pk>[0-9]+)',
        BillDetailView.as_view(),
        name='bill_detail'
    ),
    url(r'^bills/', BillListView.as_view(), name="bill_list"),
    url(r'^categories/', include('categories.urls')),
    url(r'^brands/', include('brands.urls')),
    url(r'^statistics/$', StatisticsView.as_view(), name='statistics'),
]
