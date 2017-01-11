from django.conf.urls import url
from .views import BillCreateView, BillFormView


urlpatterns = [
    url(r'^$', BillCreateView.as_view()),
    url(r'^form', BillFormView.as_view()),
]
