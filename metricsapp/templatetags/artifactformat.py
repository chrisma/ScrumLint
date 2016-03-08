from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

register = template.Library()

def trunc(string, length=75, end='..'):
	if len(string) > length:
		return string[:length] + end
	return string

def is_issue(obj):
	if not isinstance(obj, dict):
		return False
	return 'issues' in obj.get('url','')

def is_commit(obj):
	if not isinstance(obj, dict):
		return False
	return 'commits' in obj.get('url','')

def is_user(obj):
	if not isinstance(obj, dict):
		return False
	return 'users' in obj.get('url','')

def _format_issue(issue, esc):
	"""Format a Github issue object for display.
	esc : escape function
	"""
	issue_link = '<a href="{href}" target="_blank">#{number}</a>: {title}'
	issue_html = issue_link.format(
		href=esc(issue['html_url']),
		number=esc(issue['number']),
		title=esc(trunc(issue['title']))
	)
	return mark_safe(issue_html)

def _format_commit(commit, esc):
	"""Format a Github commit object for display.
	esc : escape function
	"""
	commit_link = '<a href="{href}" target="_blank" title="{html_title} | {author}">[{sha}] {commit_message}</a>'
	commit_html = commit_link.format(
		href=esc(commit['html_url']),
		commit_message=esc(trunc(commit['commit_message'], length=50)),
		sha=esc(trunc(commit['sha'], length=6, end='')),
		author=esc(commit['commit_author_name']),
		html_title=esc(commit['commit_message'])
	)
	return mark_safe(commit_html)

def _format_user(user, esc):
	# avatar_url
	"""Format a Github user object for display.
	esc : escape function
	"""
	user_link = '<a href="{href}" target="_blank" title="Github ID:{html_title}"><img style="height: 30px; border-radius: 15px;" src="{avatar_url}"> {login}</a>'
	user_html = user_link.format(
		href=esc(user['html_url']),
		html_title=esc(user['id']),
		login=esc(user['login']),
		avatar_url=esc(user['avatar_url'])
	)
	return mark_safe(user_html)

def float_format(f):
	formatted = "{0:.2f}".format(f)
	if formatted.endswith('.00'):
		return formatted[:-3]
	return formatted

@register.filter(name='format_artifact', needs_autoescape=True)
def format_artifact(value, autoescape=True):
	esc = conditional_escape if autoescape else lambda x: x

	# Check if input is a list
	if isinstance(value, list):
		if all([is_user(e) for e in value]):
			return mark_safe(', '.join([_format_user(e, esc) for e in value]))
		if all([is_issue(e) for e in value]):
			return mark_safe('<br>'.join([_format_issue(e, esc) for e in value]))
		if all([is_commit(e) for e in value]):
			return mark_safe('<br>'.join([_format_commit(e, esc) for e in value]))
		if all([isinstance(e,str) or isinstance(e,unicode) for e in value]):
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
		return _format_issue(value, esc)
	if is_commit(value):
		return _format_commit(value, esc)
	if is_user(value):
		return _format_user(value, esc)
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

@register.filter(name='to_js_var')
def to_js_var(string):
	"""Convert string to valid Javascript variable name"""
	string = slugify(str(string))
	string = string.replace('-','_')
	return string
