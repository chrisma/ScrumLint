#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# manage.py dumpscript metricsapp
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script

from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    # You probably want to uncomment on of these two lines
    # @transaction.atomic  # Django 1.6
    # @transaction.commit_on_success  # Django <1.6
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: Category

    from metricsapp.models.base import Category

    metricsapp_category_1 = Category()
    metricsapp_category_1.name = 'Backlog Maintenance'
    metricsapp_category_1 = importer.save_or_locate(metricsapp_category_1)

    metricsapp_category_2 = Category()
    metricsapp_category_2.name = 'Best Practices'
    metricsapp_category_2 = importer.save_or_locate(metricsapp_category_2)

    metricsapp_category_3 = Category()
    metricsapp_category_3.name = 'Workload'
    metricsapp_category_3 = importer.save_or_locate(metricsapp_category_3)

    # Processing model: DailyUserStoryThroughput

    from metricsapp.models.daily_user_story_throughput import DailyUserStoryThroughput

    metricsapp_dailyuserstorythroughput_1 = DailyUserStoryThroughput()
    metricsapp_dailyuserstorythroughput_1.name = 'Daily User Story Throughput'
    metricsapp_dailyuserstorythroughput_1.description = 'Amount of user story a developer is assigned on average per day.'
    metricsapp_dailyuserstorythroughput_1.explanation = 'The average amount of user stories that were assigned to a developer in a sprint (i.e. #sprintUS / #devs). This is without regard to the complexity of each story. A good visualization for this is the amount of user stories a developer has to accomplish on a full work day on average (i.e. (#sprintUS / #devs) / #workDays). If this is significantly lower than average / previously, the stories possibly are too large and should be split, to allow easier parallel work and future estimation. If this number is high (especially higher than a critical threshold [10?]), it is possible that nonfunctional requirements (e.g. tests, design requirements, deployment, “definition of done”) and communication and context  switching overhead were underrated and there are too many stories in the sprint.'
    metricsapp_dailyuserstorythroughput_1.query = "MATCH (l:GithubLabel)-[:labels]-(i:GithubIssue)-[:milestone]->(m:GithubMilestone) WHERE m.title = '{sprint}' AND l.name = '{label}' WITH m.title as Sprint, count(i) as AmountOfIssues, l.name as Team MATCH (u:GithubUser) WHERE u.role <> 'org' AND u.team = '{team}' RETURN AmountOfIssues, count(u) as devs, round(100 * (toFloat(AmountOfIssues) / count(u))) / 100 as USperDev"
    metricsapp_dailyuserstorythroughput_1.endpoint = 'sample endpoint'
    metricsapp_dailyuserstorythroughput_1.active = True
    metricsapp_dailyuserstorythroughput_1.severity = 0.5
    metricsapp_dailyuserstorythroughput_1 = importer.save_or_locate(metricsapp_dailyuserstorythroughput_1)
    metricsapp_dailyuserstorythroughput_1.categories.add(metricsapp_category_3)


    # Processing model: JustInTimeDevelopment

    from metricsapp.models.just_in_time_development import JustInTimeDevelopment

    metricsapp_justintimedevelopment_1 = JustInTimeDevelopment()
    metricsapp_justintimedevelopment_1.name = 'Just-In-Time Development'
    metricsapp_justintimedevelopment_1.description = 'Commits within 30 minutes sprint deadline.'
    metricsapp_justintimedevelopment_1.explanation = 'Amount of commits during the last day / last week of the sprint. If everything was last minute, the Scrum meetings were ineffective, due to lack of content. Furthermore, blockers for / from other teams could not be communicated.\r\n'
    metricsapp_justintimedevelopment_1.query = 'MATCH (m:GithubMilestone), (g:GithubCommit)-[:committer]-(u:GithubUser) WHERE u.team = "{team}" WITH m, g, (m.due_on+60*60*15) - g.commit_committer_date as SecsDistance WHERE SecsDistance>0 AND SecsDistance<60*60*72 AND m.title = "{sprint}" WITH m, count(g) as JITcommits MATCH (h:GithubCommit)-[:committer]-(u:GithubUser) WHERE h.commit_committer_date < m.due_on AND u.team = "{team}" WITH JITcommits, count(h) as TotalCommits RETURN JITcommits, TotalCommits, (JITcommits*1.0)/TotalCommits as Percentage'
    metricsapp_justintimedevelopment_1.endpoint = 'sample endpoint'
    metricsapp_justintimedevelopment_1.active = True
    metricsapp_justintimedevelopment_1.severity = 1.0
    metricsapp_justintimedevelopment_1 = importer.save_or_locate(metricsapp_justintimedevelopment_1)
    metricsapp_justintimedevelopment_1.categories.add(metricsapp_category_2)

    # Processing model: ForgottenOnes

    from metricsapp.models.forgotten_ones import ForgottenOnes

    metricsapp_forgottenones_1 = ForgottenOnes()
    metricsapp_forgottenones_1.name = 'Forgotten Ones'
    metricsapp_forgottenones_1.description = 'User stories that are still open in previous sprints.'
    metricsapp_forgottenones_1.explanation = "Amount of user stories in previous sprints that are not closed. It is likely that these user stories were worked on, but were simply not closed due to negligence or were “backup” stories that  weren't of high priority. These stories should be closed (or moved) to promote better overview or need special attention if they really were forgotten."
    metricsapp_forgottenones_1.query = 'MATCH (m:GithubMilestone)-[:milestone]-(i:GithubIssue)-[:labels]-(l:GithubLabel) WHERE m.title = "{sprint}" and m.due_on<timestamp() and i.state="open" and l.name = "{label}" WITH m, m.title as Sprint, collect(DISTINCT i) as OpenIssues, count(DISTINCT i) as Amount MATCH m-[:milestone]-(j:GithubIssue)-[:labels]-(l:GithubLabel) WHERE l.name = "{label}" WITH OpenIssues, count(j) as Total, Amount RETURN Amount, OpenIssues, Total, (Amount*1.0)/Total as Percentage'
    metricsapp_forgottenones_1.endpoint = 'sample endpoint'
    metricsapp_forgottenones_1.active = True
    metricsapp_forgottenones_1.severity = 0.5
    metricsapp_forgottenones_1 = importer.save_or_locate(metricsapp_forgottenones_1)
    metricsapp_forgottenones_1.categories.add(metricsapp_category_1)

    # Processing model: NeverEndingStory

    from metricsapp.models.never_ending_story import NeverEndingStory

    metricsapp_neverendingstory_1 = NeverEndingStory()
    metricsapp_neverendingstory_1.name = 'Never-ending Story'
    metricsapp_neverendingstory_1.description = 'User stories that were in the backlog of 3 or more sprints.'
    metricsapp_neverendingstory_1.explanation = 'A user story that is assigned to the sprint backlog of more than 3 sprints, with or without commits referencing it. The more never-ending stories there are in a project, the more likely it is that blockers and dependencies will become an issue.\r\n'
    metricsapp_neverendingstory_1.query = 'Match (e:GithubIssueEvent)-[:issue]-(i:GithubIssue)-[:labels]-(l:GithubLabel) WHERE e.event="milestoned" AND e.milestone_title IN [{sprint_list}] AND l.name = "{label}" WITH i, collect(DISTINCT e.milestone_title) as Sprints WITH i, Sprints, length(Sprints) as InSprints WHERE InSprints > 2 RETURN i as Issues, InSprints, Sprints'
    metricsapp_neverendingstory_1.endpoint = 'sample endpoint'
    metricsapp_neverendingstory_1.active = True
    metricsapp_neverendingstory_1.severity = 1.0
    metricsapp_neverendingstory_1 = importer.save_or_locate(metricsapp_neverendingstory_1)
    metricsapp_neverendingstory_1.categories.add(metricsapp_category_1)

    print()
    print("DONE The metrics are now in the database.")
    print("Run 'python manage.py run_metrics' to retrieve the data for all metrics.")