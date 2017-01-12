from django.conf.urls import url
from .views import BillCreateView, BillDetailView, BillListView


urlpatterns = [
    url(r'^$', BillListView.as_view()),
    url(r'^bills/create', BillCreateView.as_view(), name='bill_create'),
    url(r'^bills/(?P<pk>[0-9]+)', BillDetailView.as_view(), name='bill_detail'),
]
