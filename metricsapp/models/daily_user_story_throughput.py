from .base import SprintMetric
from ..settings import conf
import json

class DailyUserStoryThroughput(SprintMetric):
	def _calculate_score(self, sprint=conf.sprints[-1]):
		SCORE_COLUMN = 'USperDev'
		UPPER_BOUND = 10
		LOWER_BOUND = 0.2
		
		if isinstance(self.results, str):
			results = json.loads(self.results)
			print('GOT A STRING, WANTED A DICT')
		else:
			results = self.results
		results = results[sprint]
		
		score_index = results['columns'].index(SCORE_COLUMN)
		value = results['rows'][0][score_index]
		
		if value > UPPER_BOUND or value < LOWER_BOUND:
			return 25
		r = 80 + (value*5)
		return r if r<=100 else 100