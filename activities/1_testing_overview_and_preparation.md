# Overview of testing for the coursework

## Testing covered so far and what will be introduced this week

In COMP0035 you covered the types of testing in a project, focusing largely on testing applications (rather than testing
associated with data science).

For the coursework you wrote unit tests in pytest, and may have used GitHub actions to automatically run those tests
when commits are pushed, a process called 'continuous integration'. You also considered the use of coverage to determine
the extent to which the tests cover your code.

In week 5 of COMP0034 you were introduced to integration testing (sometimes referred to as component, functional or
scenario testing) where you used the Selenium framework in combination with pytest asserts to test that the Dash
application worked.

This week you will look at further combinations of these tools to test Flask:

- Using pytest and a Flask test client to test Flask routes and models
- Using Selenium with pytest to test components or functions of the app via a web browser
- Adding the tests to a GitHub Actions continuous integration workflow

## Summary of the types of tests and the associated testing libraries and tools you may wish to use for the coursework

There isn't a single type of testing that will cover all aspects of the app so the following table attempts to summarise
which 'tool' to use for which testing 'job'.

| Aspect to be tested                                                                                        | Test library and/or tools to use                                                | Related activity                                                         |
|:-----------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------|:-------------------------------------------------------------------------|
| Python helper functions e.g. to prepare data, create charts, utility functions for routes; database models | Pytest unit tests (pytest or unittest)                                          | 2_testing_models.md (testing Python functions was covered in COMP0035)   |
| Flask routes                                                                                               | Pytest unit tests (pytest or unittest) + Flask test client code                 | 3_testing_routes.md                                                      |
| Functional tests e.g. use cases or user stories, by carrying out sequences of steps in a web browser       | Selenium web driver (pytest or unittest) + Flask test client code               | 4_testing_browser.md                                                     |
| Dash app testing                                                                                           | Selenium web driver with pytest + Dash test client                              | Covered in COMP0034 week 5                                               |
| Continuous integration i.e. running tests automatically on pushing a commit to GitHub                      | GitHub Actions workflow written in YAML `.yml` + choice of tests from the above | 5_testing_browser.md                                                     |

For the coursework it is suggested that you do not carry out Dash app testing in the way that is recommended in their
documentation. Once you have integrated the Dash app into Flask you can no longer use the Dash test client in the way
described in the documentation. Instead, you could test the dashboard as for a route in your Flask app, or include in
your Flask Selenium tests.

For any of the pytest tests, tests are usually in a `tests` directory in the project, written in python
files. `fixtures` can be added to `conftest.py` and used in the tests.

## Pytest or unittest?

Unittest is provided with python. There are also helper libraries such as Flask-Testing that extend unittest for working
with Flask apps.

Pytest supports execution of unittest test cases, with additional features that purport to make it easier to write test
cases. The [official Flask tutorial](https://flask.palletsprojects.com/en/1.1.x/testing/) uses pytest.

The activities in the course materials use pytest since this is what was used in COMP0035. You may choose either
unittest or pytest for the coursework. While unittest and Flask-Testing are not covered in the course teaching
materials, there are examples and documentation online if you prefer to use these rather than pytest.

Selenium webdriver, which is used in a later activity, works with both pytest and unittest.

## Adding tests to the project directory

The project structure with all the above tests added _might_ look like the following. In particular, the location
of `app.py`, `config.py`, `data`, `dash_app`, blueprints etc. will vary depending on how you decided to structure your
project. If you chose to use unittest rather than pytest then you will not have a `conftest.py` since this is specific
to pytest.

```text
├── app.py
├── config.py
├── your_app
│   ├── __init__.py
│   ├── models.py
│   └── static  [or there may separate static directories within each blueprint]
│       ├──  ... css will go here
│   └── templates  [or there may separate templates directories within each blueprint]
│       ├──  ... html files will go here
│   └── ...blueprint folders... [optional]
│   └── dash_app
│       ├── layout.py
│       ├── callbacks.py
├── data
│       ├──  ... data set, database will go here
├── tests
│   ├── conftest.py
│   ├── functional
│       ├── __init__.py
│       ├── test_auth.py  (e.g. test the routes in auth )
│       └── test_main.py  (e.g. test the routes in main )
│   └── unit
│       ├── __init__.py
│       ├── test_models.py
│       └── test_helper_functions.py
│   └── component
│       ├── __init__.py
│       └── test_browser_flask.py  (e.g. Selenium tests for Flask app )
└── .github
│   └── workflows
│       └── my_app_ci.yml
├── requirements.txt
├── .gitignore
├── README.md
└── venv
```

## Configure testing for your Flask project

### Install the relevant test libraries

You will need to install the relevant test libraries.

If you were to cover all types of testing mentioned previously using pytest then would need:

```text
pytest
pytest-cov
selenium
```

These are included in the `requirements.txt` for this repository.

If you are using unittest instead of pytest then you would need a different coverage library and you may also want to
use Flask-Testing.

### Configure your IDE

You may also need to configure your IDE to use pytest to run the tests. Search the documentation for your IDE.

### Check your TestConfig parameters in your Flask app

If you are using the approach covered in the teaching activities then it is likely you are configuring your Flask app
using the factory approach and the `create_app()` function. Further you are likely configuring the Flask app for
different environments using `config.py`. If this is not the case then you will need to apply the following guidance to
the method you are using for configuring a Flask app.

Modify (or check) that you have the following parameters in your test configuration in `config.py`. For example in
the `paralympics_app/config.py` it is:

```python
class TestConfig(Config):
    TESTING = True
    #  You may wish to use an in-memory database rather than one saved to file for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    #  False for testing but turn to True if you want to echo SQL to the console for debugging database queries
    SQLALCHEMY_ECHO = False
    #  Tests will fail without this. This allows forms to be submitted from the tests without the CSRF token
    WTF_CSRF_ENABLED = False
```

### Installing your own project
The following documentation may be useful, particularly for those experiencing issues with discovery of modules/packages.
https://docs.pytest.org/en/6.2.x/goodpractices.html

The recommendation copied from that source is:

For development, we recommend you use venv for virtual environments and pip for installing your application and any dependencies, as well as the pytest package itself. This ensures your code and dependencies are isolated from your system Python installation.

Next, place a setup.py file in the root of your package with the following minimum content:

```python
from setuptools import setup, find_packages

setup(name="PACKAGENAME", packages=find_packages())
```

Where PACKAGENAME is the name of your package. You can then install your package in “editable” mode by running from the same directory:

```python
pip install -e .
```

which lets you change your source code (both tests and application) and rerun tests at will. This is similar to running python setup.py develop or conda develop in that it installs your package using a symlink to your development code.

