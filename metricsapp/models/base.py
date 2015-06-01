import json
from django.db import models
from django.utils import timezone
from ..data import result_data
from jsonfield import JSONField
from model_utils.managers import InheritanceManager
import requests

from ..settings import conf

class Category(models.Model):
	name = models.CharField(max_length=50)

	def rate(self, sprint):
		return Metric.rate(self.metric_set.select_subclasses(), sprint)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)

class Metric(models.Model):

	@classmethod
	def rate(cls, list_of_metrics, sprint):
		rating = 0
		max_rating = 0
		for metric in list_of_metrics:
			metric_results = metric.get_results(sprint)
			rating += metric_results['score'] * metric.severity
			max_rating += 100 * metric.severity
		result = (rating/max_rating)*100
		return round(result, 2) 

	#Enables returning subclasses via select_subclasses()
	objects = InheritanceManager()

	categories = models.ManyToManyField(Category)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=2000)
	explanation = models.TextField(blank=True)
	query = models.TextField()
	endpoint = models.CharField(max_length=200)
	results = JSONField(null=True)
	last_query = models.DateTimeField(null=True, blank=True)
	active = models.BooleanField(default=True)
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

	def _calculate_score(self, *args, **kwargs):
		return 50*self.severity

	def run(self):
		self.results = self._process(self._run_query())
		self.last_query = timezone.now()
		self.save()

	def score_rating(self, score):
		if score <= 25:
			return 'bad'
		if score >= 80:
			return 'good'
		if score <= 60:
			return 'improvement'
		return 'ok'

	def get_results(self, *args, **kwargs):
		score = self._calculate_score()
		rating = self.score_rating(score)
		return {'data':self.results, 'score':score, 'rating':rating}


class SprintMetric(Metric):
	def _run_query(self, sprint=None):
		url = 'http://192.168.30.196:7478/db/data/transaction/commit'
		payload = {
			"statements" : [ {
				"statement" : self.query.format(sprint=sprint)
			} ]
		}
		headers = {'Accept': 'application/json; charset=UTF-8', 'Content-Type': 'application/json'}
		r = requests.post(url, data=json.dumps(payload), headers=headers)

		print(sprint, r.text[:100])

		return r.json()

	def run(self):
		results = {}
		for sprint in conf.sprints:
			results[sprint] = self._process(self._run_query(sprint))
		self.results = results
		self.last_query = timezone.now()
		self.save()

	def get_results(self, sprint=conf.sprints[-1], *args, **kwargs):
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		score = self._calculate_score(sprint)
		rating = self.score_rating(score)
		return {'data':results[sprint], 'score':score, 'rating':rating}
