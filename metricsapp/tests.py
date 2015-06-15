from django.test import TestCase

from metricsapp.models import Category, SprintMetric

class CategoryTest(TestCase):
	def setUp(self):
		self.empty_cat = Category()
		self.empty_cat.save()
		self.nonempty_cat = Category()
		self.nonempty_cat.save()
		metric = SprintMetric()
		metric.save()
		self.nonempty_cat.metric_set.add(metric)

	def test_is_empty(self):
		"""is_empty() instance method checks for number of associated metrics"""
		self.assertTrue(self.empty_cat.is_empty(), 'Empty categories reported correctly.')
		self.assertFalse(self.nonempty_cat.is_empty(), 'Categories with one metric are not empty')
