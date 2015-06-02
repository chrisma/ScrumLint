from django.contrib import admin
from .models import Metric, Category
import json

admin.site.register(Category)

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
	class Media:
		css = {
			"all": ("admin/metric_detail.css",)
		}
		# js = ("my_code.js",)

	# Columns to be shown on overview page
	list_display = ('__str__', 'list_of_categories', 'active',)
	# Model attributes to show filters for (on the right side)
	list_filter = ('active',)
	readonly_fields = ('last_query', 'formatted_results',)
	exclude = ('results',)

	def list_of_categories(self, metric):
		return ', '.join([c.name for c in metric.categories.all()])

	def formatted_results(self, instance):
		pretty_json = json.dumps(instance.results, indent=2, sort_keys=True)
		return '<pre>{}</pre>'.format(pretty_json)
	formatted_results.short_description = "results"
	formatted_results.allow_tags = True