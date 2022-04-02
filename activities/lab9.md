# Lab 7: Testing

This focuses on creating functional tests and browser tests with Selenium. Unit tests and using GitHub Actions were
covered in COMP0035.

## Functional tests: create tests for the auth module

Refer to [3_testing_routes.md](3_testing_routes.md) for guidance.

### Write the test documentation

Write GIVEN, WHEN, THEN documentation for the following (add them
to [tests/functional/test_auth.py](../tests/functional/test_auth.py)):

- Sign up a new user
- Login with an incorrect email address (error message should be displayed on the form)
- Login with an incorrect password (error message should be displayed on the form)
- Login with correct details
- Login, choose Logout from the navbar, you should be logged out (and login is then available in the navbar)

### Create fixtures for use in the tests

For many of the tests we need to create a test User. Add the following fixtures to the tests to help you.

```python
import pytest
from paralympics_app.models import User, Profile


@pytest.fixture(scope='module')
def user_data():
    """ Data to create a new user"""
    user_data = {
        'first_name': 'Alice',
        'last_name': 'Cooper',
        'password_text': 'SchoolsOut',
        'email': 'a_cooper@poison.net'
    }
    yield user_data


@pytest.fixture(scope='module')
def new_user(user_data):
    """ Create a user without a profile and add them to the database. Allow the user object to be used in tests. """
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password_text=user_data['password_text'])
    yield user


@pytest.fixture(scope='function')
def user_with_profile():
    """ Creates a user with a profile. """
    user_data = {
        'first_name': 'Alison',
        'last_name': 'Krauss',
        'password_text': 'RaisingSand',
        'email': 'a_krauss@mymail.net'
    }
    profile_data = {
        'username': 'AK',
        'bio': 'My favourite paralympic sport is dressage.'
    }

    profile = Profile(username=profile_data['username'], bio=profile_data['bio'])
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password_text=user_data['password_text'])
    user.profile.append(profile)
    yield user


@pytest.fixture(scope='function')
def login_default_user(test_client, user_data):
    """Log in the user and logout at the end of the test"""
    test_client.post('/login', data=dict(email=user_data['email'], password=user_data['password']),
                     follow_redirects=True)
    yield
    test_client.get('/logout', follow_redirects=True)
```

## Write the tests

If you have already specified the tests using the `GIVEN, WHEN, THEN` structure then you should be able to work out the
test code. Remember:

- 'GIVEN' suggests any preparation that is needed, e.g. such as creating a test user
- 'WHEN' suggests the action to carry out with the client
- 'THEN' suggests the assertion

## Write tests

Create a python file with an appropriate name, e.g. it should start with `test_` and be in the `tests` directory.

Try and write test code for each of the tests.

One of the things you will need is to handle routes that redirect to another route. For example if you try to access a
page that requires login, and you are not logged in, then you will be redirected to the login page. An example of the
syntax for this is shown below:

```python
def test_dashboard_not_allowed_when_user_not_logged_in(test_client):
    """
    GIVEN A user is not logged
    WHEN they access the dashboard menu option
    THEN they should be redirected to the login page
    """
    response = test_client.get('/dashboard/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
```

## Selenium browser tests
Refer to [4_testing_browser.md](4_testing_browser.md) for guidance.

Try to create a number of tests to match things that a user may do on the web app, e.g.:

- go to the competition page and submit an entry
- create a profile with username and bio
- login with an incorrect password and check that it fails (consider creating a fixture to create a new user in the database first)
- access the dashboard (requires login) and then use one of the selectors to change the charts that are
  displayed
