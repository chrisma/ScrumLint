from .base import SprintMetric
from ..settings import conf
import json

class JustInTimeDevelopment(SprintMetric):
	def _calculate_score(self, sprint, team):
		SCORE_COLUMN = 'Percentage'
		UPPER_BOUND = 0.3
		
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		results = results[sprint][team['name']]
		
		score_index = results['columns'].index(SCORE_COLUMN)
		value = results['rows'][0][score_index]

		if value > UPPER_BOUND:
			return 20
		r = 100 - (value*300)
		return r if r >= 0 else 0
