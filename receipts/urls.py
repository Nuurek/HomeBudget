from django.conf.urls import url
from .views import ReceiptCreateView, ReceiptDetailView, ReceiptListView

urlpatterns = [
    url(r'^$', ReceiptListView.as_view(), name="receipt_list"),
    url(r'^new/$', ReceiptCreateView.as_view(), name='receipt_create'),
    url(
        r'^(?P<pk>[0-9]+)',
        ReceiptDetailView.as_view(),
        name='receipt_detail'
    ),
]
