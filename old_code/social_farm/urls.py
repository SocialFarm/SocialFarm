from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^social/', include('socialregistration.urls')),
    url(r'^notify/', include('social_farm.notify.urls')),
    url(r'^dashboard/', include('social_farm.dashboard.urls')),
    # Examples:
    # url(r'^$', 'social_farm.views.home', name='home'),
    # url(r'^social_farm/', include('social_farm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
