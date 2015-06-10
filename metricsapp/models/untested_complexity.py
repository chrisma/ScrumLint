from .base import SprintMetric

class UntestedComplexity(SprintMetric):
	def _calculate_score(self, sprint, team):
		SCORE_COLUMN = 'Percentage'
		
		value = self.get_value(sprint, team, SCORE_COLUMN)
		if value is None:
			value = 0
		
		r = 100-(value*100*2.3)
		return r if r>0 else 0
