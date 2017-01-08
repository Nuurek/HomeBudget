from django.conf.urls import url
from .views import BillCreateView


urlpatterns = [
    url(r'^$', BillCreateView.as_view()),
]
