from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('social_farm.notify.views',
	(r'^$', 'test'),
	(r'^facebook/(?P<uid>\d+)/$', 'facebook'),
)
