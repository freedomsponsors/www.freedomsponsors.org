www.freedomsponsors.org
=======================

[![Build Status](https://secure.travis-ci.org/freedomsponsors/www.freedomsponsors.org.png)](http://travis-ci.org/freedomsponsors/www.freedomsponsors.org)

FreedomSponsors is a Django web application.

FS is made by, and for developers.
If you'd like to help (bug reports, suggestions, or even code), you are more than welcome.
Please take a look at the open issues.

Also, feel free to join the [mailing list](https://groups.google.com/forum/?hl=en&fromgroups#!forum/freedomsponsors)

## How to setup a development environment

1. Clone repo.

  ```bash
  git clone git://github.com/freedomsponsors/www.freedomsponsors.org.git
  ```

2. Create a virtualenv and install dependencies.

  ```bash
  python bootstrap
  ```

  Note that to install the `psycopg2` package you must have Postgres installed on your system. Otherwise the *pip install* might fail.

3. Configure settings.

  ```bash
  cp frespo/env_settings.py_template frespo/env_settings.py
  nano frespo/env_settings.py # edit according to your environment
  ```

4. Setup the database.

  4.1 Create a `frespo` database on postgres (default username and password is `frespo`).

  4.2 Apply the schema:

    ```bash
    cd www.freedomsponsors.org/djangoproject
    ./manage.py syncdb
    ./migrate.sh
    ```

  4.3 Load the initial data.

    ```bash
    ./manage.py loadFeedbackData
    ./manage.py loadProjects
    ```

5. Run the development server!

  ```bash
  ./manage.py runserver
  ```

   Visit http://localhost:8000 on your browser.

*Note: If you find that the steps above are not actually accurate, please [open a new issue to let us know](https://github.com/freedomsponsors/www.freedomsponsors.org/issues/new).*


## Running the test suite

You will need to install [Splinter](https://github.com/cobrateam/splinter) (a Selenium wrapper), and you will also need need to create two test gmail accounts (and then specify username and password in your env_settings.py file).

To run unit tests, please refer to the [Testing](https://github.com/freedomsponsors/www.freedomsponsors.org/wiki/Testing) wiki page.

Also, there is a fully-functional test-environment at http://ambtest.freedomsponsors.org.
Feel free to use it as you like (might be useful when reading the code!). We provide no guarantee about the data on it though!

## Licensing

This software is licensed under the [AFFERO GENERAL PUBLIC LICENSE](http://www.gnu.org/licenses/agpl-3.0.html)
