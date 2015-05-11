from django.core.management.base import BaseCommand, CommandError
from metricsapp.models import Metric, SprintMetric

class Command(BaseCommand):
    help = 'Runs all available metrics.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for metric in Metric.objects.all().select_subclasses():
            self.stdout.write('Running "{}"'.format(metric))
            metric.run()
