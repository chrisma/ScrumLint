# ScrumLint

## Setup
* Install the dependencies (preferably in a [virtualenv](https://pypi.python.org/pypi/virtualenv/))

  `pip install -r requirements.txt`

* Create the necessary database tables (incl. superuser)

  `python manage.py syncdb`

* Load in seed data

  `python manage.py runscript seed`
  
* Retrieve the data for all metrics

  `python manage.py run_metrics`

* Run the development server

  `python manage.py runserver`

* Visit the index page at `localhost:8000`
* Visit the admin at `localhost:8000/admin` (login with superuser credentials)
