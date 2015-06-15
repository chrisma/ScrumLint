from .base import SprintMetric

class TutorScores(SprintMetric):
	def _calculate_score(self, sprint, team):
		SCORE_COLUMN = 'AveragedRating'
		
		value = self.get_value(sprint, team, SCORE_COLUMN)
		if value is None:
			value = 0
		
		r = value*10
		if r > 100:
			return 100
		if r < 0:
			return 0
		return r 
