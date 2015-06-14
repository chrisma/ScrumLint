from django.contrib import admin
from .models import Metric, Category
import json
from django.template.defaultfilters import pluralize, timesince

admin.site.register(Category)

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
	class Media:
		css = {
			"all": ("admin/metric_detail.css", 
					"admin/pretty-json.css",)
		}
		js = ("admin/underscore-min.js",
			  "admin/backbone-min.js",
			  "admin/pretty-json-min.js",
			  "admin/style-json.js",)

	# Columns to be shown on overview page
	list_display = ('__str__', 'list_of_categories', 'last_updated', 'severity', 'active',)
	# Model attributes to show filters for (on the right side)
	list_filter = ('active', 'severity',)
	readonly_fields = ('last_query', 'formatted_results',)
	# suit tabs
	suit_form_tabs = (('general', 'General'), ('query', 'Query information'))
	fieldsets = [
		(None, {
			'classes': ('suit-tab', 'suit-tab-general',),
			'fields': ['name', 'description', 'categories', 'explanation', 'active', 'severity']
		}),
		(None, {
			'classes': ('suit-tab', 'suit-tab-query',),
			'fields': ['query', 'endpoint', 'last_query', 'formatted_results']
		}),
	]
	# Register custom action
	actions = ['activate']

	def list_of_categories(self, metric):
		return ', '.join([c.name for c in metric.categories.all()])

	def last_updated(self, metric):
		return timesince(metric.last_query)

	def formatted_results(self, instance):
		pretty_json = json.dumps(instance.results, indent=2, sort_keys=True)
		return '<pre>{}</pre>'.format(pretty_json)
	formatted_results.short_description = "results"
	formatted_results.allow_tags = True

	def show_update_message(self, request, queryset):
		count = queryset.count()
		message = '{amount} {model}{s} {plural} updated.'.format(
			amount = count,
			model = queryset.model.__name__.lower(),
			s = pluralize(count),
			plural = pluralize(count, 'was,were')
		)
		self.message_user(request, message)

	def activate(self, request, queryset):
		queryset.update(active=True)
		self.show_update_message(request, queryset)
	activate.short_description = "Mark selected metrics as active"
