from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='format_commit', needs_autoescape=True)
def format_commit(value, autoescape=True):

	def is_commit(obj):
		if not isinstance(obj, dict):
			return False
		return 'issues' in obj.get('url','')

	link = '<a href="{href}" target="_blank">#{number}</a>: {title}'
	def format(commit):
		html = link.format(
			href=esc(commit['html_url']),
			number=esc(commit['number']),
			title=esc(commit['title'])
		)
		return mark_safe(html)

	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x

	# Check if input is a list
	if isinstance(value, list):
		if all([is_commit(e) for e in value]):
			return mark_safe('<br>'.join([format(e) for e in value]))
		if all([isinstance(e,str) for e in value]):
			return mark_safe(', '.join(value))
		if all([isinstance(e,float) or isinstance(e,int) for e in value]):
			return mark_safe('<br>'.join(map(str,value)))
		return value
			
	# Input is not a list
	if isinstance(value, float):
		return "{0:.2f}".format(value)
	if not is_commit(value):
		return value
	return format(value)

@register.filter(name='un_underscore')
def un_underscore(string):
	return string.replace('_', ' ')

# adapted from https://github.com/guillaumeesquevin/django-colors
@register.filter(name='hex_to_rgb')
def hex_to_rgb(hex, format_string='rgb({r},{g},{b})'):
	"""Returns the RGB value of a hexadecimal color"""
	hex = hex.replace('#','')
	out = {	'r':int(hex[0:2], 16),
			'g':int(hex[2:4], 16),
			'b':int(hex[4:6], 16)}
	return format_string.format(**out)