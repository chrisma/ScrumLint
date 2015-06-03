from django.contrib import admin
from .models import Metric, Category
import json

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
	list_display = ('__str__', 'list_of_categories', 'severity', 'active',)
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

	def list_of_categories(self, metric):
		return ', '.join([c.name for c in metric.categories.all()])

	def formatted_results(self, instance):
		pretty_json = json.dumps(instance.results, indent=2, sort_keys=True)
		return '<pre>{}</pre>'.format(pretty_json)
	formatted_results.short_description = "results"
	formatted_results.allow_tags = True