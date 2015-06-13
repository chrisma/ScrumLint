from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

def trunc(string, length=75, end='..'):
	if len(string) > length:
		return string[:length] + end
	return string

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
			title=esc(trunc(issue['title']))
		)
		return mark_safe(html)

	commit_link = '<a href="{href}" target="_blank" title="{html_title}">{commit_message}</a>'
	def commit_format(commit):
		html = commit_link.format(
			href=esc(commit['html_url']),
			commit_message=esc(trunc(commit['commit_message'])),
			html_title=esc(commit['commit_message'])
		)
		return mark_safe(html)

	def float_format(f):
		formatted = "{0:.2f}".format(f)
		if formatted == '0.00':
			return '0'
		if formatted.endswith('.00'):
			return formatted[:-3]
		return formatted

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

@register.filter(name='floor_to_multiple')
def floor_to_multiple(num, multiple=10):
	"""Round down number to nearest multiple"""
	num = float(num)
	multiple = float(multiple)
	return num - (num % multiple)
