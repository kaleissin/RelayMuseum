from django.contrib import admin

from cals.models import Language as CalsLanguage
from cals.models import User as CalsUser

from relay.models import *

class RingInline(admin.TabularInline):
    model = Ring
    fk_name = 'relay'
    max_num = 3

class RelayAdmin(admin.ModelAdmin):
    inlines = [RingInline,]
    ordering = ['pos', 'name']
admin.site.register(Relay, RelayAdmin)

class TorchAdmin(admin.ModelAdmin):
    ordering = ['pos', 'relay', 'ring', 'language']
    list_display = ['relay', 'ring', 'pos', 'language']
    list_display_links = ['pos', 'language']
    list_filter = ['relay']
admin.site.register(Torch, TorchAdmin)

admin.site.register(Participant)
admin.site.register(Language)
