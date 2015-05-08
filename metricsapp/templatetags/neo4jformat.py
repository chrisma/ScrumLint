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

	link = '<a href="{}" target="_blank">#{}</a>'
	def format(commit):
		html = link.format(
			esc(commit['html_url']), esc(commit['number'])
		)
		return mark_safe(html)

	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x

	# Check if input is a list
	if isinstance(value, list):
		if all([is_commit(e) for e in value]):
			return mark_safe(', '.join([format(e) for e in value]))
		if all([isinstance(e,str) for e in value]):
			return mark_safe(', '.join(value))
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
