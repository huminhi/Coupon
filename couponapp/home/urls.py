from django.conf.urls.defaults import url, include
from couponapp.home import views

urlpatterns = [
    url(r'^$', views.HomeView.index())
]