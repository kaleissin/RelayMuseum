from django.contrib import admin
from django.apps import apps

ACTSTREAM = apps.is_installed('actstream')
if ACTSTREAM:
    from actstream import action

from relay.models import *


class ActstreamMixin(object):
    if ACTSTREAM:
        def save_model(self, request, obj, form, change):
            obj.save()
            if change:
                action.send(request.user, verb='updated', action_object=obj)
            else:
                action.send(request.user, verb='added', action_object=obj)


class RingInline(admin.TabularInline):
    model = Ring
    fk_name = 'relay'
    max_num = 6


class RingAdmin(ActstreamMixin, admin.ModelAdmin):
    model = Ring
    list_filter = ['relay']
admin.site.register(Ring, RingAdmin)


class RelayAdmin(ActstreamMixin, admin.ModelAdmin):
    inlines = [RingInline,]
    ordering = ['pos', 'name']
    list_display = ('pos', 'name')
    list_display_links = ('pos', 'name')
admin.site.register(Relay, RelayAdmin)


class TorchFileInline(admin.TabularInline):
    model = TorchFile
    fk_name = 'torch'


class TorchAdmin(ActstreamMixin, admin.ModelAdmin):
    inlines = [TorchFileInline]
    ordering = ['relay', 'ring', 'pos', 'language']
    list_display = ['relay', 'ring', 'pos', 'language', 'participant']
    list_display_links = ['pos', 'language', 'participant']
    list_filter = ['relay']
    save_on_top = True
    search_fields = ['^language__name', '^participant__name', '^participant__cals_user__profile__display_name']
admin.site.register(Torch, TorchAdmin)


class ParticipantAdmin(ActstreamMixin, admin.ModelAdmin):
    list_display = ('name', 'cals_user')
admin.site.register(Participant, ParticipantAdmin)


class TorchFileAdmin(ActstreamMixin, admin.ModelAdmin):
    model = TorchFile
    list_display = ['category', 'torch', 'filename', 'mimetype']
    list_filter = ['category', 'mimetype']
admin.site.register(TorchFile, TorchFileAdmin)

class LanguageAdmin(ActstreamMixin, admin.ModelAdmin):
    model = Language
admin.site.register(Language, LanguageAdmin)
