from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='format_commit', needs_autoescape=True)
def format_commit(value, autoescape=True):

	def is_issue(obj):
		if not isinstance(obj, dict):
			return False
		return 'issues' in obj.get('url','')

	def is_commit(obj):
		if not isinstance(obj, dict):
			return False
		return 'commits' in obj.get('url','')

	issue_link = '<a href="{href}" target="_blank">#{number}</a>: {title}'
	def issue_format(issue):
		html = issue_link.format(
			href=esc(issue['html_url']),
			number=esc(issue['number']),
			title=esc(issue['title'])
		)
		return mark_safe(html)

	commit_link = '<a href="{href}" target="_blank">{commit_message}</a>'
	def commit_format(commit):
		html = commit_link.format(
			href=esc(commit['html_url']),
			commit_message=esc(commit['commit_message'])
		)
		return mark_safe(html)

	def float_format(f):
		return "{0:g}".format(f)

	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x

	# Check if input is a list
	if isinstance(value, list):
		if all([is_issue(e) for e in value]):
			return mark_safe('<br>'.join([issue_format(e) for e in value]))
		if all([is_commit(e) for e in value]):
			return mark_safe('<br>'.join([commit_format(e) for e in value]))
		if all([isinstance(e,str) for e in value]):
			return mark_safe(', '.join(value))
		if all([isinstance(e,float) for e in value]):
			return mark_safe('<br>'.join([float_format(f) for f in value]))
		if all([isinstance(e,int) for e in value]):
			return mark_safe('<br>'.join(map(str,value)))
		return value
			
	# Input is not a list
	if isinstance(value, float):
		return float_format(value)
	if is_issue(value):
		return issue_format(value)
	if is_commit(value):
		return commit_format(value)
	return value

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