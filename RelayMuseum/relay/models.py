from django.db import models
from django.template.defaultfilters import slugify

from cals.models import Language as CalsLanguage
from cals.models import User as CalsUser
from translation.models import get_interlinear

def re_slugify(queryset):
    for object in queryset.objects.all():
        object.slug = slugify(object.name)
        object.save(force_update=True)

def clone_ringtorch(relay, torch):
    pass
    #rings = relay.

class Participant(models.Model):
    cals_user = models.ForeignKey(CalsUser, null=True, blank=True, related_name='relays')
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

    def rings(self):
        rings = self.ring_mastering.all()
        relays = {}
        for ring in rings:
            relays.setdefault(ring.relay.name, [])
            relays[ring.relay.name].append(ring)
        out = []
        for relayname, rings in relays.items():
            relay = Relay.objects.get(name=relayname) 
            if relay.rings.count() == len(rings):
                out.append(relay)
            else:
                out.append(ring)
        return out

class Language(models.Model):
    cals_language = models.ForeignKey(CalsLanguage, null=True, blank=True, related_name='relays')
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    slug = models.SlugField(blank=True, null=True, editable=False, unique=True)

    class Meta:
        ordering = ['name']
        unique_together = ('cals_language', 'name', 'slug')

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
    missing = models.BooleanField(default=True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['pos']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Relay, self).save(*args, **kwargs)

    @property
    def num_torches(self):
        return sum(ring.num_torches for ring in self.rings.all())

    @property
    def missing_torches(self):
        return self.num_torches - self.torches.count()

class Ring(models.Model):
    RING_SUBTYPES = (
            ('standard', 'Standard'),
            ('romance', 'Romance'),
            )
    relay = models.ForeignKey(Relay, related_name='rings')
    ring_master = models.ForeignKey(Participant, blank=True, null=True, related_name='ring_mastering')
    name = models.CharField(max_length=10, default='_')
    slug = models.SlugField(blank=True, null=True, editable=False)
    subtype = models.CharField(max_length=20, 
        choices=RING_SUBTYPES,
        default='standard')
    end = models.DateTimeField(blank=True, null=True)
    num_torches = models.PositiveIntegerField('Number of torches', default=0)

    class Meta:
        ordering = ['id', 'name']
        unique_together = ('relay', 'name')
        order_with_respect_to = 'relay'

    def __unicode__(self):
        if self.name != u'_':
            return u'%s, ring %s' % (self.relay.name, self.name)
        else:
            return u'%s' % self.relay.name

    def save(self, *args, **kwargs):
        if not self.ring_master:
            self.ring_master = self.relay.relay_master
        self.slug = slugify(self.name)
        super(Ring, self).save(*args, **kwargs)

    @property
    def missing_torches(self):
        return self.num_torches - self.torches.count()

class Torch(models.Model):
    INTERLINEAR_FORMATS = (
            ('monospace', 'WYSIWYG monospace'),
            ('leipzig', 'Leipzig Glossing Rules'),
    )

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
    abbreviations = models.TextField(
            blank=True, null=True,
            help_text='Abbreviations')
    interlinear = models.TextField('Interlinear', blank=True, null=True, default='', db_column='il_text')
    il_xhtml = models.TextField('Interlinear, formatted', blank=True, null=True, default='', db_column='il_xhtml', editable=False)
    il_format = models.CharField('Interlinear format', max_length=20, choices=INTERLINEAR_FORMATS, blank=True, default='monospace')

    class Meta:
        verbose_name_plural = 'torches'
        unique_together = ('relay', 'ring', 'pos')
        ordering = ('ring', 'pos',)
        order_with_respect_to = 'ring'

    def __unicode__(self):
        return u'%s ring %s: %s by %s' % (self.relay.name, self.ring.name, self.language.name, self.participant.name)

    def save(self, *args, **kwargs):
        if self.interlinear.strip():
            self.il_xhtml = get_interlinear(self)
        # Denormalization
        if not self.relay and self.ring:
            self.relay = self.ring.relay
        if not self.ring and self.relay:
            rings = self.relay.rings.all()
            num_rings = rings.count()
            if num_rings in (0, 1):
                # Probably a one-ring relay...
                self.ring, created = Ring.objects.get_or_create(relay=self.relay)
            else:
                # Just pick one
                self.ring = self.relay.rings.all()[0]
        super(Torch, self).save(*args, **kwargs)

    def get_interlinear(self):
        return get_interlinear(self)

    def simple_name(self):
        return u'%s by %s' % (self.language.name, self.participant.name)

