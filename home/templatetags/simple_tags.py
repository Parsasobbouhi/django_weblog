from datetime import datetime
from django.template import Library


register = Library()

@register.simple_tag
def current_time(format_string):
    return datetime.now().strftime(format_string)