from django.contrib import admin
from .models import Metric, Category

admin.site.register(Metric)
admin.site.register(Category)