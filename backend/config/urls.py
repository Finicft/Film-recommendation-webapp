import os
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from api.views import root,public,search

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
project_root = os.path.realpath('../')

urlpatterns=[
    url(r'^$', root, name='root'),
    url(r'^api\/search', search, name='search'),
    url(r'^public\/.+', public, name='public'),
    # url(r'api/node$', hello, name='hello')
]