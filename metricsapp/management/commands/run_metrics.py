from django.core.management.base import BaseCommand, CommandError
from metricsapp.models import Metric, SprintMetric

class Command(BaseCommand):
	help = 'Runs all available metrics.'

		#parser.add_argument('poll_id', nargs='+', type=int)
	def add_arguments(self, parser):
		parser.add_argument("-m", "--metric-names", type=str, dest="explicit", nargs="+")

	def handle(self, *args, **options):
		all_metrics = Metric.objects.filter(active=True).select_subclasses()
		explicit = options['explicit']
		if explicit:
			explicit_metrics = [all_metrics.get(name=name) for name in explicit]
			self._run_metrics(explicit_metrics)
		else:
			self._run_metrics(all_metrics)

	def _run_metrics(self, lst):
		for metric in lst:
			self.stdout.write('Running "{}"'.format(metric))
			metric.run()
