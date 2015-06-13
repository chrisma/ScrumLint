from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

# adapted from https://github.com/guillaumeesquevin/django-colors
@register.filter(name='hex_to_rgb')
def hex_to_rgb(hex, format_string='rgb({r},{g},{b})'):
	"""Returns the RGB value of a hexadecimal color"""
	hex = hex.replace('#','')
	out = {	'r':int(hex[0:2], 16),
			'g':int(hex[2:4], 16),
			'b':int(hex[4:6], 16)}
	return format_string.format(**out)