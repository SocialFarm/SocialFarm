from django.conf.urls.defaults import *

urlpatterns = patterns('fbbuis.fbbuismanage.views',
    (r'^$', 'manage'),
    (r'^create/$', 'create'),
    (r'^manage/$', 'manage'),
    (r'^manage/invite/(?P<bid>\d+)/$', 'manageinvite'),
    (r'^manage/members/(?P<bid>\d+)/$', 'managemembers'),
    (r'^manage/members/(?P<bid>\d+)/(?P<uid>\d+)/$', 'managemember'),
    (r'^manage/groups/(?P<bid>\d+)/$', 'managegroups'),
    (r'^manage/repdist/(?P<bid>\d+)/$', 'managerep'),
    (r'^manage/paydist/(?P<bid>\d+)/$', 'managepay'),
    (r'^events/$', 'events'),
    (r'^events/(?P<event_id>\d+)/$', 'eventbynum'),
    (r'^events/hide/(?P<event_id>\d+)/$', 'eventhide'),
    (r'^closeevent/(?P<event_id>\d+)/$', 'closeevent'),
    # Define other pages you want to create here
)

