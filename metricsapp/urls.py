from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sprint/(?P<sprint_index>[0-9]+)/$', views.index, name='index'),
]