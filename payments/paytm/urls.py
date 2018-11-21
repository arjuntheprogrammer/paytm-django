from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^payment/', views.payment, name='payment'),
    url(r'^response/', views.response, name='response'),
]
