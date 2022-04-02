# Browser testing with Selenium Webdriver

## Selenium webdriver overview

The Flask test client cannot fully emulate the environment of a running application. For example, an application that
relies on JavaScript code running in the client browser will not work, as the JavaScript code included in the responses
will be returned to the test without being executed. The behaviour of the application may also vary in different
browsers.

The selenium webdriver API allows you to programmatically interact with a browser the way a real user would and is most
commonly used for testing. Support is provided for most programming languages. It does not have a built-in framework for
actually running tests (relies on provided tools, e.g. unittest).

If you completed the week 5 learning materials then you have already used Selenium webdriver to test a Dash application.

## Getting started

You will need to install selenium e.g. `pip install selenium`. It was included in requirements.txt for this repository.

You also need to install the correct driver for your browser and operating system. This is explained below and in more
detail in the [Getting Started documentation](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/)
on the Selenium website.

Selenium currently supports testing using Chrome, Firefox, Edge, Internet Explorer and Safari. You can use any of these.
The teaching materials in this course focus on Chrome.

There is some additional guidance on how to install Chromedriver in
the [week 5 repository](https://github.com/nicholsons/comp0034_week5/blob/master/activities/1_testing_dash.md).

## Creating fixtures to support browser tests

You will need to create two fixtures:

1. To create the ChromeDriver (or whichever driver you are using) which is required to control access to the browser
2. TO create and stop a Flask app server that the browser can make requests to

The first fixture below creates a ChromeDriver with options that are required for running in a continuous integration (
CI) environment. Note that if you want to see the tests running on your computer in the browser then you should comment
out the 'headless' option.

The second fixture runs and stops the Flask app. Unlike the functional testing which used a test client, Selenium tests
from a browser which accesses a server with the app running. Since we don't have the app running on a server then you
need to create a running version of the Flask app that Selenium can access. There is very little documentation
explaining how to use Flask with Selenium and Pytest. You may wish to investigate `pytest-flask` and use
its `live_server` fixture rather than the following.

If you have been using unittest with Flask-Testing rather than pytest then you will be able to use their `'live_server`
fixture. However, in this repository we are using pytest, so you will need to create the fixture.

```python
import multiprocessing
import pytest

from selenium.webdriver import Chrome, ChromeOptions


@pytest.fixture(scope='class')
def chrome_driver(request):
    """ Selenium webdriver with options to support running in GitHub actions
    Note:
        For CI: `headless` and `disable-gpu` not commented out
        For running on your computer: `headless` and `disable-gpu` to be commented out
    """
    options = ChromeOptions()
    options.add_argument("--headless")  # use for GitHub Actions CI
    options.add_argument('--disable-gpu') # use for GitHub Actions CI
    options.add_argument("--window-size=1920,1080")
    chrome_driver = Chrome(options=options)
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()


@pytest.fixture(scope='class')
def run_app(app):
    """
    Fixture to run the Flask app for Selenium browser tests
    """
    multiprocessing.set_start_method("fork")  # Needed in Python 3.8 and later
    process = multiprocessing.Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()
```

## Create a new test

A test file has been created at [tests/browser/test_app_browser.py](../tests/browser/test_app_browser.py).

For no reason other than that all the examples to date have shown test functions, this file contains a test class and
even test case is a function in that class. This is simply to show you how to create tests as a class for those who
prefer object-oriented code. You do not need to write tests as a class in order to carry out the Selenium tests!

The first test is to check that the app is running and can be accessed through the browser. If you configured your app
to run on a different port from the default 5000 then you would need to use the appropriate port in the code below.

```python
@pytest.mark.usefixtures('chrome_driver', 'run_app')
class TestMyAppBrowser:
    def test_app_is_running(self):
        self.driver.get("http://127.0.0.1:5000/")
        assert self.driver.title == 'Home page'
```

Run the test and check that it runs successfully. It should if you have already added the required fixtures to
conftest.py.

## Writing tests

Once you have tested you can access the web app then you can start to create functional tests. You might consider
writing tests to check your user stories, use cases or requirements.

Assuming you are using pytest then you will use the same assertions. However, how you carry out the steps in the test is
now very different.

You are using a browser and so you can only navigate the page in the way that a browser can i.e. using the DOM (see week
2 teaching materials).

### Targeting elements

Selenium works by [targeting elements](https://www.selenium.dev/documentation/webdriver/elements/) on a web page. You
will need to identify elements on the page to target.

There are eight different built-in element location strategies in WebDriver. These
are [listed here](https://www.selenium.dev/documentation/webdriver/elements/locators/#traditional-locators). The
recommended approach is to use `id` wherever possible as this avoids more complex DOM traversals.

Selenium also
supports [relative locators](https://www.selenium.dev/documentation/webdriver/elements/locators/#relative-locators) such
as 'Above', 'Below', 'Left of' etc.

The [Python code syntax for finding the elements](https://www.selenium.dev/documentation/webdriver/elements/finders/)
using these location strategies is shown in the Selenium documentation. For example:

```python
driver.find_element(By.ID, "cheese")
driver.find_element(By.CLASS_NAME, "tomatoes")
driver.find_element_by_css_selector("#fruits .tomatoes")
elements = driver.find_elements(By.TAG_NAME, 'p')
```

Once you have targeted, or selected, an element then you typically want to do something such as click on it, select a
value, enter text etc.

### Interacting with web elements

[The documentation](https://www.selenium.dev/documentation/webdriver/elements/interactions/) states there are only 5
basic commands that can be executed on an element:

- [click](https://w3c.github.io/webdriver/#element-click) (applies to any element)
- [send keys](https://w3c.github.io/webdriver/#element-send-keys) (only applies to text fields and content editable
  elements)
- [clear](https://w3c.github.io/webdriver/#element-clear) (only applies to text fields and content editable elements)
- submit (only applies to form elements)
- select (see [Select List Elements](https://www.selenium.dev/documentation/webdriver/elements/select_lists/))

If you want to complete a form, then you can pass values to complete an element e.g. to add the name Charles to the name
input of a form:

```python
# Navigate to Google search url
driver.get("http://www.google.com")

# Enter "webdriver" text and perform "ENTER" keyboard action to search for the term 'webdriver'
driver.find_element(By.NAME, "q").send_keys("webdriver" + Keys.ENTER)
```

### Waits

It is possible that a test executes faster than the browser responds, you may therefore need to include
explicit [waits](https://www.selenium.dev/documentation/en/webdriver/waits/) e.g. to wait until a particular element is
loaded before trying to locate it in the test. You can wait for any of
the [expected conditions listed in the documentation](https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html?highlight=expected)
.

```python
WebDriverWait(driver, timeout=3).until(some_condition)
```

Or wait for a specific period of time:

```python
driver.implicitly_wait(10)
```

### Assertions

The Selenium Webdriver API relies on a testing library for the test capability. You therefore use the assertions for the
testing library you choose e.g. pytest or unittest.

The example test in `tests/browser/test_app_browser.py` shows the sequence of interactions with the browser with
assertions at relevant points. This tests a use case of 'register a new user'.

```python
from selenium.webdriver.common.by import By


def test_signup_succeeds(self):
    """
    Test that a user can create an account using the signup form if all fields are filled out correctly,
    and that they are redirected to the index page.
    """
    # Go to the home page
    self.driver.get('http://127.0.0.1:5000/')

    # Click signup menu link
    # See https://www.selenium.dev/documentation/webdriver/waits/
    self.driver.implicitly_wait(5)
    self.driver.find_element(By.ID, "nav-signup").click()

    # Test person data
    first_name = "First"
    last_name = "Last"
    email = "email@ucl.ac.uk"
    password = "password1"
    password_repeat = "password1"

    # Fill in registration form
    self.driver.find_element(By.ID, "first_name").send_keys(first_name)
    self.driver.find_element(By.ID, "last_name").send_keys(last_name)
    self.driver.find_element(By.ID, "email").send_keys(email)
    self.driver.find_element(By.ID, "password").send_keys(password)
    self.driver.find_element(By.ID, "password_repeat").send_keys(password_repeat)
    self.driver.find_element(By.ID, "btn-signup").click()

    # Assert that browser redirects to index page
    self.driver.implicitly_wait(10)
    assert self.driver.current_url == 'http://127.0.0.1:5000/'

    # Assert success message is flashed on the index page
    message = self.driver.find_element(By.ID, "flash-messages").text
    assert f"Hello, {first_name} {last_name}. You are signed up." in message
```

## Run the test

To see the test running you will need to make sure that the driver fixture has the following line commented
out: `# options.add_argument("--headless")`. Running the browser in headless mode is required for the CI environment on
GitHub, however if you want to see the tests executing in the browser on your computer then you need it not to be in
headless mode.
