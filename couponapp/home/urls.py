from django.conf.urls import url, include
from couponapp.home import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view())
]