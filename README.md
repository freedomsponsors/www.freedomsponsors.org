www.freedomsponsors.org 
=======================

[![Build Status](https://secure.travis-ci.org/freedomsponsors/www.freedomsponsors.org.png)](http://travis-ci.org/freedomsponsors/www.freedomsponsors.org)

FreedomSponsors is a Django web application.

FS is made by, and for developers. 
If you'd like to help (bug reports, suggestions, or even code), you are more than welcome.
Please take a look at the open issues.

## Running

Instructions to run application locally:

1. Clone repo.

  ```bash
  git clone git://github.com/freedomsponsors/www.freedomsponsors.org.git
  ```

2. Create a `frespo` database on postgres (default username and password is `frespo`).

  2.1 Install dependencies.

    ```bash
    sudo pip install -r requirements.txt
    ```

    Depending on your environment, psycopg2 installation with pip might fail.
    If that's your case, you might also wanna try.

    ```bash
    sudo apt-get install python-psycopg2
    ```

3. Configure settings.

  ```bash
  mv frespo/env_settings.py_template frespo/env_settings.py
  nano frespo/env_settings.py # edit according to your environment
  ```

4. Create database objects.

  ```bash
  cd www.freedomsponsors.org/djangoproject
  ./manage.py syncdb
  ./migrate.sh
  ```

5. Populate with some initial data.

  ```bash
  ./manage.py loadFeedbackData
  ./manage.py loadProjects
  ```

6. Run!

  ```bash
  ./manage.py runserver # and visit http://localhost:8000
  ```

If you find that the steps above are not actually accurate, please [open a new issue to let us know](https://github.com/freedomsponsors/www.freedomsponsors.org/issues/new)!

You should also verify if you can run all the automatic tests successfully.
You will need to install [Splinter](https://github.com/cobrateam/splinter) (a Selenium wrapper), and you will also need need to create two test gmail accounts (and then specify username and password in your env_settings.py file).

To run unit tests, please refer to the [Testing](https://github.com/freedomsponsors/www.freedomsponsors.org/wiki/Testing) wiki page.

Also, there is a fully-functional test-environment at http://ambtest.freedomsponsors.org.
Feel free to use it as you like (might be useful when reading the code!). We provide no guarantee about the data on it though!

## Licensing

This software is licensed under the [AFFERO GENERAL PUBLIC LICENSE](http://www.gnu.org/licenses/agpl-3.0.html)
