from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sprint/(?P<sprint_index>[0-9]+)/team/(?P<team_name>\w+)$', views.index, name='index'),
]