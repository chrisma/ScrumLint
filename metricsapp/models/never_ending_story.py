from .base import SprintMetric
from ..settings import conf
import json
from django.utils import timezone

class NeverEndingStory(SprintMetric):
	def _calculate_score(self, sprint, team):
		UPPER_BOUND = 10
		LOWER_BOUND = 0.2
		MULTIPLIER_COLUMN = "InSprints"
		
		if (isinstance(self.results, str) or isinstance(self.results, unicode)):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		amount = len(results[sprint][team['name']]['rows'])
		multiplier = self.get_value(sprint, team, MULTIPLIER_COLUMN) or 1
		score = 100 - (amount*multiplier*5)
		return score if score > 0 else 0

	def run(self):
		# Setup data structure
		results = {}
		for sprint in conf.sprints:
			results[sprint] = {}
			for team in conf.teams:
				results[sprint][team['name']] = {'rows':[], 'columns':[]}

		# Fill data structure
		for team in conf.teams:
			team_results = self._process(self._run_query(None,team))
			for row in team_results['rows']:
				for sprint in row[-1][:-1]:
					results[sprint][team['name']]['rows'].append(row)
					results[sprint][team['name']]['columns'] = team_results['columns']

		self.results = results

		self.last_query = timezone.now()
		self.save()
