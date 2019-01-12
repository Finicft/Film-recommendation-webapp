from django.conf.urls import include, url
from api.views import hello

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns=[
    url(r'^$', hello, name='hello')
]
