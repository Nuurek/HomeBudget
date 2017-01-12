from django.conf.urls import url
from .views import BillCreateView, BillDetailsView


urlpatterns = [
    url(r'^$', BillCreateView.as_view()),
    url(r'^bills/(?P<pk>[0-9]+)', BillDetailsView.as_view(), name='bill_details'),
    url(r'^bills/create', BillCreateView.as_view(), name='bill_create'),
]
