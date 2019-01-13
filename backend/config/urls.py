import os
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from api.views import root,public,node, children_nodes, search

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
project_root = os.path.realpath('../')

urlpatterns=[
    url(r'^$', root, name='root'),
    url(r'^public\/.+', public, name='root'),
    url(r'^api\/node', node, name='root'),
    url(r'^api\/children_nodes', children_nodes, name='root'),
    url(r'^api\/search', search, name='search'),
    # url(r'api/node$', hello, name='hello')
]