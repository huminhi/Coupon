from django.conf.urls import url
from auth.views import Authentication

urlpatterns = [
    url(r'^login$', Authentication.login(), name='login'),
    url(r'^logout$', Authentication.logout(), name='logout'),
]