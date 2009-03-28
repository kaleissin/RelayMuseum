from django import template

from cals.templatetags.cals_tags import integer, fraction

register = template.Library()

integer = register.filter(integer)
fraction = register.filter(fraction)
