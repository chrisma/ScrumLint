from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index),
    url(r'^sprint/(?P<sprint_index>[0-9]+)$', views.index),
    url(r'^team/(?P<team_name>\w+)$', views.index),
    url(r'^sprint/(?P<sprint_index>[0-9]+)/team/(?P<team_name>\w+)$', views.index, name='index'),
	url(r'^compare$', views.compare),
	url(r'^compare/sprint/(?P<sprint_index>[0-9]+)$', views.compare, name='compare'),
	url(r'^deactivate$', views.deactivate, name='deactivate'),
	url(r'^latest-sprint-badge/$', views.latest_sprint_badge),
	url(r'^latest-sprint-badge/team/(?P<team_name>\w+)$', views.latest_sprint_badge, name='badge'),
]