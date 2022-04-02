# COMP0034 Week 9 starter code

This repository contains the starter code for week 9.

The following are documented in the `activities` directory:

1. [Overview of testing activities for the coursework and the required set-up activities](activities/1_testing_overview_and_preparation.md)
2. [Testing the models using pytest](activities/2_testing_models.md)
3. [Testing routes of the Flask app with pytest and the Flask test client](activities/3_testing_routes.md)
4. [Testing the web app from a browser using selenium webdriver and pytest](activities/4_testing_browser.md)
5. [Using GitHub actions for continuous integration (CI), coverage and linting](activities/5_testing_github_actions.md)
6. [Lab 9](activities/lab9.md)

The `paralympics_app` directory has the app code to be tested. Please check that you can run the Flask app before you start
to create the tests.

**The starter test code will not run correctly until you complete the activities**. This is because the activities
complete fixtures that the tests rely on.

There is a separate repo that has some completed tests and a GitHub Actions workflow
at [https://github.com/nicholsons/comp0034_week9_paralympics](https://github.com/nicholsons/comp0034_week9_paralympics)

## Set-up

1. Create a repository by using
   the [Use this template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
   green button.
    - Use the Owner drop-down to select your GitHub account (if not already selected).
    - Type a name for the repo
    - Set visibility to private
    - Leave other options unselected
    - Select create repository from template
2. Clone the repository in your IDE
3. _Create_ and _activate_ a venv e.g. `python3 -m venv venv` then `source venv/bin/activate` (Mac)
   or `.\env\Scripts\activate` (Windows)
4. Install the libraries from requirements.txt e.g. `pip install -r requirements.txt`
5. Check that your IDE is configured to use `pytest`.
6. Check that you can run the Flask app by running `paralympics_app/app.py`.
