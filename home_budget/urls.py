from django.conf.urls import url
from .views import BillView


urlpatterns = [
    url(r'^$', BillView.as_view()),
    url(r'^bills/create', BillView.as_view(), name='bill_create'),
    url(r'^bills/(?P<pk>[0-9]+)', BillView.as_view(), name='bill_details'),
]
