from django import template
from main.models import settings
register = template.Library()


@register.filter
def setting(placeholder, value):
    for k, v in settings:
        if k == value:
            return v


register.filter('setting', setting)