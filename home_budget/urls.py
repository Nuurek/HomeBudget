from django.conf.urls import url
from .views import BillCreateView, BillFormView


urlpatterns = [
    url(r'^$', BillCreateView.as_view()),
    url(r'^bill/create', BillFormView.as_view(), name='bill_create'),
]
