import json
from django.db import models
from django.utils import timezone
from metricsapp.data import result_data
from jsonfield import JSONField
from model_utils.managers import InheritanceManager

from metricsapp.settings import conf

class Metric(models.Model):

	#Enables returning subclasses via select_subclasses()
	objects = InheritanceManager()

	name = models.CharField(max_length=50)
	description = models.CharField(max_length=2000)
	explanation = models.TextField(blank=True)
	query = models.CharField(max_length=2000)
	endpoint = models.CharField(max_length=200)
	score = models.FloatField(null=True, blank=True)
	results = JSONField(null=True)
	last_query = models.DateTimeField(null=True, blank=True)
	HIGH = 1.5
	NORMAL = 1.0
	LOW = 0.5
	SEVERITY_CHOICES = (
		(HIGH, 'High (1.5x)'),
		(NORMAL, 'Normal (1.0x)'),
		(LOW, 'Low (0.5x)'),
	)
	severity = models.FloatField(choices=SEVERITY_CHOICES,
								default=NORMAL)

	def __str__(self):
		return self.name

	def _run_query(self):
		return result_data[self.name]

	def _process(self, query_data):
		data = query_data['results'][0]
		result = {}
		result['rows'] = []
		for row in data['data']:
			result['rows'].append(row['row'])
		result['columns'] = data['columns']
		return result

	def _calculate_score(self):
		return 50*self.severity

	def run(self):
		self.results = self._process(self._run_query())
		self.score = self._calculate_score()
		self.last_query = timezone.now()
		self.save()

	def score_rating(self):
		if self.score >= 75:
			return 'good'
		if self.score <= 25:
			return 'bad'
		return 'ok'

	def get_results(self, *args, **kwargs):
		return self.results


class SprintMetric(Metric):
	def _run_query(self, sprint):
		return result_data[self.name + ' ' + sprint]

	def run(self):
		results = {}
		for sprint in conf.sprints:
			results[sprint] = self._process(self._run_query(sprint))
		self.results = results
		self.last_query = timezone.now()
		self.score = self._calculate_score()
		self.save()

	def get_results(self, sprint=conf.sprints[-1], *args, **kwargs):
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		return results[sprint]

class DailyUserStoryThroughput(SprintMetric):
	pass
