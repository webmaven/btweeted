Introduction
============

BTweeted is a simple Twitter search app. It keeps track of the phrases searched
for in order to display recent and popular (ie. as searched for through the app
) searches.

The application was built during a consulting client's new developer onboarding,
to demonstrate my basic competency with Python and Django.

Installing
==========

The following instructions assume that you have Python 2.7 and virtualenv 
installed. If not, make sure you have pip installed (http://www.pip-installer.org/en/latest/installing.html),
and then install virtualenv (http://www.virtualenv.org/en/latest/virtualenv.html#installation).::
    git clone git@github.com:webmaven/btweeted.git
    mkvirtualenv btweeted
    cd btweeted
    cp btweeted/secretsettings.txt btweeted/secretsettings.py
    vim btweeted/secretsettings.py
    source ./bin/activate
    pip install -r requirements.txt
    python ./manage.py syncdb
    python ./manage.py runserver

Go to http://127.0.0.1:8000 

Note that there is a step in the middle to edit a secretsettings.py file that
you create from an example secretsettings.txt file. Instructions are in the
example file.

Testing
=======

Run the tests as follows::
    python manage.py test phrases

You can also see the test coverage::

    python manage.py test_coverage phrases

Requirements
============

The following are the requirements that were given for development of the app:

* A requirements file so that others can install your site easily
* A readme file describing your site, how to set it up, and how to use it.
* A django site
 * An app with:
  * A model of phrases to search for.  This model has:
   * The phrase
   * The the number of times the phrase was searched for from the app.
   * The datetime of the last search for the phrase.
  * A form to enter the search phrase.
  * Views to search for the phrase and view a list of search results.
  * A twitter client used to fetch the results from the search. If you
    choose to use an open-source Python Twitter library, you must still wrap
    that library in a client module for separation of concerns from views.
  * Automated unit tests to prove your app works as desired
  * All text displayed to the user must be translated

I extended the requirements a bit:

* Phrases that are extremely similar (only case and leading/trailing whitespace
  differences so far) are treated as identical for search popularity purposes.

