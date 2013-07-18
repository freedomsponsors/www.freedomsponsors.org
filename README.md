[![Stories in Ready](http://badge.waffle.io/freedomsponsors/www.freedomsponsors.org.png)](http://waffle.io/freedomsponsors/www.freedomsponsors.org)  
www.freedomsponsors.org 
=======================

[![Build Status](https://secure.travis-ci.org/freedomsponsors/www.freedomsponsors.org.png)](http://travis-ci.org/freedomsponsors/www.freedomsponsors.org)

FreedomSponsors is a Django web application.

FS is made by, and for developers. 
If you'd like to help (bug reports, suggestions, or even code), you are more than welcome.
Please take a look at the open issues.

Also, feel free to join the [mailing list](https://groups.google.com/forum/?hl=en&fromgroups#!forum/freedomsponsors)

Testing coverage reports: [here](http://freedomsponsors.github.com/www.freedomsponsors.org/coverage_html_report/)

## Windows users

If you're a Windows user we suggest you set up a virtual machine using [VirtualBox](http://www.virtualbox.org) - Ubuntu
virtual machines can be downloaded [here](http://virtualboxes.org/images/ubuntu/). 

## Running

Instructions to run application locally:

1. You'll need a few tools for the next steps - make sure all of them are installed before proceeding to the next steps.

 1.1 Make sure your package information is up to date.
 
 ```bash
 $ sudo apt-get update --fix-missing
 ```
 
 1.2 Install Git.
 
  ```bash
  $ sudo apt-get install git
  ```
 
 1.3 Install PostgreSQL.
 
 ```bash
 $ sudo apt-get install postgresql 
 $ sudo apt-get install postgresql-server-dev-all # Make sure you have this.
 ```
 1.4 Install python-dev.
 
 ```bash
 $ sudo apt-get install python-dev
 ```
 1.5 Install python-lxml.
 
 ```bash
 $ sudo apt-get install python-lxml libxslt-dev
 ```
 
 1.6 Install libpq-dev.
 
 ```bash
 $ sudo apt-get install libpq-dev
 ```
 
 1.7 Install pip.
 
 ```bash
 $ sudo apt-get install python-pip
 ```
 
2. Clone the web application repository.

  ```bash
  $ git clone git://github.com/freedomsponsors/www.freedomsponsors.org.git
  ```

3. Create the database/default user.
  
    ```bash
    $ sudo su postgres #run the next command as postgres
    $ createuser -d -SRP frespo # this will prompot you to create a password (just use frespo for now)
    $ createdb -O frespo frespo
    $ exit # go back to your normal user
    ```

4. Configure settings.

  ```bash
  $ cd djangoproject
  $ cp frespo/env_settings.py_template frespo/env_settings.py
  # edit the env_settings.py file - you must change the definitions shown below (values as used in this walkthrough):
  # ENVIRONMENT = 'DEV'
  # DATABASE_NAME = 'frespo'
  # DATABASE_USER = 'frespo'
  # DATABASE_PASS = 'frespo'  
  $ nano frespo/env_settings.py 
  ```
5. Create a virtualenv and install dependencies.

    ```bash
    $ python bootstrap
    ```
  If this command fails because of psycopg2, make sure you have installed postgresql-server-dev-all (mentioned on step 1)

  Then you can enter the virtualenv:

    ```bash
    $ source bin/activate
    ```
  To exit the virtualenv

    ```bash
    $ deactivate
    ```
  You'll need to be in the virtual environment to use `./manage.py ...` commands

6. Create database objects.

  ```bash  
  $ cd www.freedomsponsors.org/djangoproject
  $ ./manage.py syncdb --migrate --noinput
  ```

7. Run!

  ```bash
  $ ./manage.py runserver # and visit http://localhost:8000
  ```

If you find that the steps above are not actually accurate, please [open a new issue to let us know](https://github.com/freedomsponsors/www.freedomsponsors.org/issues/new)!

You should also verify if you can run all the automatic tests successfully.
You will need to install [Splinter](https://github.com/cobrateam/splinter) (a Selenium wrapper), and you will also need need to create two test gmail accounts (and then specify username and password in your env_settings.py file).

To run unit tests, please refer to the [Testing](https://github.com/freedomsponsors/www.freedomsponsors.org/wiki/Testing) wiki page.

Also, there is a fully-functional test-environment at http://ambtest.freedomsponsors.org.
Feel free to use it as you like (might be useful when reading the code!). We provide no guarantee about the data on it though!

## Licensing

This software is licensed under the [AFFERO GENERAL PUBLIC LICENSE](http://www.gnu.org/licenses/agpl-3.0.html)
