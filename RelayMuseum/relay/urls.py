from django.conf.urls.defaults import *

from relay.models import *

relay_list = {
        'queryset': Relay.objects.all(),
        'extra_context': { 'me': 'relay', }
    }

ring_list = {
        'queryset': Ring.objects.all(),
        'extra_context': { 'me': 'relay', }
    }

language_list = {
        'queryset': Language.objects.all(),
        'extra_context': { 'me': 'language', }
    }

participant_list = {
        'queryset': Participant.objects.all(),
        'extra_context': { 'me': 'participant', }
    }

urlpatterns = patterns('django.views.generic',
        (r'^relay/(?P<slug>[-a-z0-9._]+)/$', 'list_detail.object_detail', dict(relay_list)),
        (r'^relay/$', 'list_detail.object_list', dict(relay_list)),
        (r'^language/(?P<slug>[-a-z0-9._]+)/$', 'list_detail.object_detail', dict(language_list)),
        (r'^language/$', 'list_detail.object_list', dict(language_list)),
        (r'^participant/(?P<slug>[-a-z0-9._]+)/$', 'list_detail.object_detail', dict(participant_list)),
        (r'^participant/$', 'list_detail.object_list', dict(participant_list)),
)

urlpatterns += patterns('relay.views',
        (r'^relay/(?P<relay>[-a-z0-9._]+)/(?P<ring>[a-z0-9._]+)/(?P<id>[0-9]+)/$', 'torch_detail'),
        (r'^relay/(?P<relay>[-a-z0-9._]+)/(?P<ring>[a-z0-9._]+)/([?](?P<action>smooth))?$',
        'show_ring'),
        (r'^statistics/$', 'show_statistics'),
)

