# Functional tests for Flask routes

## Introduction

Functional or integration tests, test multiple components of a software application to make sure the components are
working together properly. Typically, these tests focus on functionality that the user will be using.

In this activity we will cover tests that require other components, rather than those that check for specific
functionality from a user perspective. Specifically it considers how to test:

- Interaction with a SQLAlchemy database
- Flask application routes

## Identify the test cases

The first example is to test whether the home page can be returned. This could be expressed as:

```python
"""
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (HTTP GET request)
    THEN a success response code (200) is received (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200)
"""
```

The second example is to test whether a new user with a profile can be added to the database, e.g.

```python
"""
    GIVEN the app is created with a database
    WHEN a new user with a profile is inserted in the database
    THEN the row count in the User and Profile tables should increase by one and the same user_id should be in both tables
"""
```

It might seem tedious to write the tests like this, and you do not have to do so, however you as you are getting started
with testing you might find it helps you to think about:

- things you might need to set up for your tests (e.g. other components, data)
- steps to carry out in the test
- assertions that may be appropriate for your tests
- edge cases and error cases

## Create Flask specific fixtures in `conftest.py`

These tests all rely on the Flask app running (e.g. to access a route) or for resources to be available (e.g. the
database). Since the same things will be needed for multiple tests then rather than define them as set-up actions in
every test, you can instead create them as pytest `fixtures`.

The concept of fixtures and how and where to write them was explained in COMP0035 so this is not repeated here. Please
refer to COMP0035 if you need to refresh your understanding.

For this activity there is a single `conftest.py` in the root of the `tests` directory. In this you will create fixtures
to do the following:

1. Create a Flask app
2. Create a test client that can be used to make HTTP requests and other actions
3. Create a database
4. Roll back all database changes at the end of each test
5. Create a new user
6. Create a new user with a profile
7. Provide data to create a user

The first test, to test the home page, needs two `fixtures`, it needs a running Flask app and a test client to allow a
the home page to be requested.

### Flask contexts and testing

Flask uses contexts to store information. The concept and use of contexts is explained nicely by Patrick
Kennedy [in this article](https://testdriven.io/blog/flask-contexts/) and
in [this video presentation](https://youtu.be/90nMybVBI9s). You may get by without understanding this, however if you
encounter "working outside of application context" errors testing then the video in particular may help you to
understand the concept sufficiently to troubleshoot the errors.

Flask provides and creates the contexts for you when it receives a request.

When a request is received, Flask provides two contexts:

| Context    | Description    | Available Objects |
|:------- |:------ |:------------|
| Application    | Keeps track of the application-level data (configuration variables, logger, database connection)    | current_app, g |
| Request    | Keeps track of the request-level data (URL, HTTP method, headers, request data, session info)    | request, session |

source: [Patrick Kennedy](https://testdriven.io/blog/flask-contexts/)

When creating our app, much of the code has been called from routes which run when a request is received. We haven't
needed to be concerned about the underlying contexts.

However, in tests if we try to access some of these objects we need to first create a context. Flask provides a test
client function, `test_client`, that can be used in testing. Request context's can be pushed to this
using `test_request_context`.

Patrick Kennedy again nicely summarises the solutions that can be used in the test code to create these:

| Object        | Context               | Common Error                           | Solution                              |
|:--------------|:----------------------|:---------------------------------------|:--------------------------------------|
| `current_app` | Application Context   | Working outside of application context | `with app.app_context():`             |
| `g`           | Application Context   | Working outside of application context | `with app.test_request_context('/'):` |
| `request`     | Request Context       | Working outside of request context     | `with app.test_request_context('/'):` |
| `session`     | Request Context       | Working outside of request context     | `with app.test_request_context('/'):` |

You will see these used as we create the fixtures.

### Create the app and test client fixtures

The first fixture you will need is to create a Flask app. You do this using the factory function `create_app`
in `paralympics_app/__init__.py`. Remember that you need to provide a Flask configuration suitable for testing. Refer to
activity 1 for more info on the Flask config for testing.

Add the following code to `tests/conftest.py`:

```python
import pytest
from paralympics_app import create_app, config


@pytest.fixture(scope='session')
def app():
    """Create a Flask app for the testing"""
    app = create_app(config_class_name=config.TestingConfig)
    yield app
```

See the pytest documentation to understand the use
of [yield](https://docs.pytest.org/en/latest/how-to/fixtures.html#yield-fixtures-recommended).

The next fixture to add to `conftest.py` is
the [test client](https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.test_client). This takes the app as a
parameter and returns the test client for use in the tests.

```python
import pytest


@pytest.fixture(scope='session')
def test_client(app):
    """Create a Flask test client using the Flask app."""
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client
```

### Create a test to check the home page is valid

You should now have just enough fixtures to run the first test to check that the home page is valid.

The following test is in [`tests/functional/test_main.py`](../tests/functional/test_main.py).

```python
def test_index_page_valid(test_client):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (HTTP GET request)
    THEN a success response code (200) is received ()
    """
    response = test_client.get('/')
    assert response.status_code == 200
```

`GIVEN` requires the Flask app which will be created for us by the app fixture so we don't need to do anything further
for this test.

`WHEN` says that we need to go to the home page which is done with the test client using `client.get('/')`. You can read
more about [HTTP request methods])(https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods).

When you submit a request to a url using the test client it returns a response. The response contains attributes that
you can check for in your assertions.

For example, `response.status_code` will tell you the status code that was
returned. [List of HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

`response.data` gives you the HTML content so you can check for any content you would expect in the HTML such as the
value of a particular tag. To match strings from the response data you need to use the binary syntax
e.g. `assert b'some string' in response.data`

We want to test the result of going to the home page so we really need `response = client.get('/')`

`THEN` is the assertion which in this case checks that in the response the status code is 200.

Run the test.

### Create fixtures to use the database

Since we also need to be able to use the SQLAlchemy database then we need two further fixtures:

1. To provide and initialise the database with the tables; and insert data into some tables.
2. To handle rolling back transactions between each test. This test has function scope (i.e. per test).

Add the following to `conftest.py`

```python
import pytest
from paralympics_app import db as _db, add_medals_data, add_noc_data


@pytest.fixture(scope='session')
def db(app):
    """
    Return a session wide database using a Flask-SQLAlchemy database connection.
    """
    with app.app_context():
        _db.app = app
        _db.create_all()
        add_medals_data(_db)
        add_noc_data(_db)
    yield _db
    _db.drop_all()


# https://docs.pytest.org/en/latest/how-to/fixtures.html#autouse-fixtures-fixtures-you-don-t-have-to-request
@pytest.fixture(scope='function', autouse=True)
def session(db, app):
    """ Roll back database changes at the end of each test """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        sess = db.create_scoped_session(options=options)
        db.session = sess
        yield sess
        sess.remove()
        transaction.rollback()
        connection.close()
```

You now have sufficient fixtures to run tests that use the database.

### Create a test that requires the database

The following code in [`tests/functional/test_models.py`](../tests/functional/test_models.py) tests when a new user is
created and inserted in the User table that the user table is increased by one. This isn't a particualy useful test but
is simple enough to illustrate the use of database in a test.

```python
from paralympics_app.models import User


def test_user_table_has_one_more_row(db):
    """
        GIVEN the app is created with a database
        WHEN a new user is inserted in the User table
        THEN the row count should increase by one
    """
    user_data = {
        'first_name': 'Alice',
        'last_name': 'Cooper',
        'password_text': 'SchoolsOut',
        'email': 'a_cooper@poison.net'
    }

    row_count_start = User.query.count()
    new_user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                    password_text=user_data['password_text'])
    db.session.add(new_user)
    db.session.commit()
    row_count_end = User.query.count()
    assert row_count_end - row_count_start == 1
```

Run the test.

## Next steps

You will need other fixtures for testing the app and your coursework. Some of these are included in [Lab 9](lab9.md).

Try and think of a few more tests yourself and implement them e.g.

- That you can successfully access each of the web pages in the app by asserting for status codes in the response or for
  text in the response data.
- What you would expect to happen when a User tries to add a profile with the same username as another user.
- What you expect to happen when a User submits a competition entry.
