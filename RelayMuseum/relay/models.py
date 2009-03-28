from django.db import models
from django.template.defaultfilters import slugify

from cals.models import Language as CalsLanguage
from cals.models import User as CalsUser

def re_slugify(queryset):
    for object in queryset.objects.all():
        object.slug = slugify(object.name)
        object.save(force_update=True)

class Participant(models.Model):
    cals_user = models.ForeignKey(CalsUser, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name and self.cals_user:
            self.name = self.cals_user.get_profile().display_name
        super(Participant, self).save(*args, **kwargs)

    def relays(self):
        return sorted(set(torch.relay for torch in self.torches.all()))

    def languages(self):
        return sorted(set(torch.language for torch in self.torches.all()))

class Language(models.Model):
    cals_language = models.ForeignKey(CalsLanguage, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name and self.cals_language:
            self.name = self.cals_language.name
        self.slug = slugify(self.name)
        super(Language, self).save(*args, **kwargs)

    def relays(self):
        return sorted(set(torch.relay for torch in self.torches.all()))

    def participants(self):
        return sorted(set(torch.participant for torch in self.torches.all()))

class Relay(models.Model):
    RELAY_SUBTYPES = (
            ('standard', 'Standard'),
            ('inverse', 'Inverse'),
            )
    name = models.CharField(max_length=40)
    slug = models.SlugField(blank=True, null=True, editable=False)
    relay_master = models.ForeignKey(Participant, related_name='relay_mastering')
    subtype = models.CharField(max_length=20, 
            choices=RELAY_SUBTYPES,
            default='standard')
    homepage = models.URLField(blank=True, null=True)
    pos = models.IntegerField('position', default=0, unique=True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['pos']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Relay, self).save(*args, **kwargs)

class Ring(models.Model):
    RING_SUBTYPES = (
            ('standard', 'Standard'),
            ('romance', 'Romance'),
            )
    relay = models.ForeignKey(Relay, related_name='rings')
    ring_master = models.ForeignKey(Participant, blank=True, null=True, related_name='ring_mastering')
    name = models.CharField(max_length=10)
    slug = models.SlugField(blank=True, null=True, editable=False)
    subtype = models.CharField(max_length=20, 
        choices=RING_SUBTYPES,
        default='standard')
    end = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        unique_together = ('relay', 'name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.ring_master:
            self.ring_master = self.relay.relay_master
        self.slug = slugify(self.name)
        super(Ring, self).save(*args, **kwargs)

class Torch(models.Model):
    followed = models.ForeignKey('Torch', null=True, blank=True, related_name='follows')
    relay = models.ForeignKey(Relay, related_name='torches')
    ring = models.ForeignKey(Ring, blank=True, null=True, related_name='torches')
    participant = models.ForeignKey(Participant, related_name='torches')
    language = models.ForeignKey(Language, related_name='torches')
    first = models.BooleanField(default=False)
    last = models.BooleanField(default=False)
    pos = models.IntegerField('position', default=0)
    torch = models.TextField(
            help_text='The text that was sent to the next participant')
    smooth_translation = models.TextField(
            blank=True, null=True,
            help_text='Smooth English translation of the torch sent')
    translation_of_received = models.TextField(
            blank=True, null=True,
            help_text='Translation of the torch received')
    mini_dictionary = models.TextField(
            blank=True, null=True,
            help_text='Mini dictionary covering the expressions, words and affixes in the torch')
    mini_grammar = models.TextField(
            blank=True, null=True,
            help_text='Mini grammar covering the phenomena in the torch')

    class Meta:
        verbose_name_plural = 'torches'
        unique_together = ('relay', 'ring', 'pos')
        ordering = ('pos',)

    def __unicode__(self):
        return u'%s by %s' % (self.language.name, self.participant.name)

    def save(self, *args, **kwargs):
        # Denormalization
        if not self.relay:
            self.relay = self.ring.relay
        super(Torch, self).save(*args, **kwargs)
