# Unit testing models in a Flask app

## Introduction

Unit tests test a unit of code, i.e. the smallest piece of code that can be logically isolated in the code, such as a
function. You already learned how to do this in COMP0035 so this is not covered again here. You should already be able
to create unit tests for helper functions in your code. This might for example be functions that you created to prepare
the data for use in particular charts, or helper functions used in your Flask routes.

In this activity we will look at an example of how you might use unit testing to test the models classes in a Flask app

Examples of testing the models using functional tests are covered in the next activity.

## Identify the test cases

First consider writing the tests using the GIVEN, WHEN, THEN model. This both documents the test and helps you to work
out the structure of the test.

For example, consider the User model in [models.py](../paralympics_app/models.py). The following may be an appropriate
unit test for the construction of a new User object:

```text
GIVEN a User model
WHEN a new User is created
THEN check the first_name, last_name, email, and password fields are defined correctly. Password should be hashed.
```

## Write the test

The test above has been added to [tests/unit/test_models.py](../tests/unit/test_models.py) for you. This is no different
to the structure of the tests that you already learned in COMP0035. Remember to use appropriate naming convention for
the test directory, test code files and the test functions.

There are 4 asserts in the test which you may decide contravenes the principle of 'test should have one reason to fail'.
In this case I felt that all the asserts are necessary to show that a new user is created correctly. You could separate
this into 4 separate tests if you prefer.

```python
from paralympics_app.models import User


def test_new_user_details_correct():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first_name, last_name, email, and password fields are defined correctly
    """
    user_data = {
        'first_name': 'Meat',
        'last_name': 'Loaf',
        'password_text': 'BatOutOfHell',
        'email': 'meat@bat.org'
    }

    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password_text=user_data['password_text'])

    assert user.first_name == 'Meat'
    assert user.last_name == 'Loaf'
    assert user.email == 'meat@bat.org'
    assert user.password != 'BatOutOfHell'
```

Run the test using whichever method you preferred in COMP0035 and whichever method your IDE supports.

As a minimum you should be able to run this from the terminal in the venv:

```
pytest -v tests/unit/test_models.py
```

## Create more unit tests for the models

Create a few more tests to ensure you can do this. There are a number of models you could write tests for. For example:

- test that a profile can be added for a given user
- test that a competition entry can be added

The 'Medals' and 'Region' table are populated using functions in [`__init__.py`](../paralympics_app/__init__.py)
in `add_noc_data(db_name)` and `add_medals_data(db_name)`. You could consider testing those functions as unit tests.

In the next activity we will look at tests for the models that require other components to be configured before the
tests can be created, that is it can't be tested in isolation as a simple unit test.
