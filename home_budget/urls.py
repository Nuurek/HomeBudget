from django.conf.urls import url, include

from receipts.views import ReceiptListView
from .views.statistics import StatisticsView

urlpatterns = [
    url(r'^$', ReceiptListView.as_view(is_form=False), name="home"),
    url(r'receipts/', include('receipts.urls')),
    url(r'^categories/', include('categories.urls')),
    url(r'^brands/', include('brands.urls')),
    url(r'^statistics/$', StatisticsView.as_view(), name='statistics'),
]
