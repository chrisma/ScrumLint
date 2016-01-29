# ScrumLint

ScrumLint is a "linter" for agile processes. It aims at supporting a development team in adopting or adhering to agile practices. ScrumLint identifies and quantifies violations, instances where the executed process deviates from the defined one, as mandated by Scrum or agile best practices.

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.45319.svg)](http://dx.doi.org/10.5281/zenodo.45319)

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
