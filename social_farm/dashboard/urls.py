from django.conf.urls.defaults import patterns, include, url
from social_farm.dashboard.views import FacebookView

urlpatterns = patterns('social_farm.dashboard.views',
	(r'^$', 'test'),
	(r'^facebook/$', FacebookView.as_view()),
)
