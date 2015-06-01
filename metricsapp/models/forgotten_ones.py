from .base import SprintMetric
from ..settings import conf
import json

class ForgottenOnes(SprintMetric):
	def _calculate_score(self, sprint, team):
		SCORE_COLUMN = 'Percentage'
		UPPER_BOUND = 0.1

		value = self.get_value(sprint, team, SCORE_COLUMN)
		if value is None:
			value = 0
		r = 100 - (value*400)
		return r if r >= 0 else 0