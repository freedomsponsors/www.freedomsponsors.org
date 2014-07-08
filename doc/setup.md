## Windows users

If you're a Windows user we suggest you set up a virtual machine using [VirtualBox](http://www.virtualbox.org) - Ubuntu
virtual machines can be downloaded [here](http://virtualboxes.org/images/ubuntu/). 

Alternatively, you can help us with [#185 - Windows development environment](https://github.com/freedomsponsors/www.freedomsponsors.org/issues/185)

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
  This will create a python virtualenv and install all dependecies listed on `requirements.txt` on it.
  If this command fails because of psycopg2, make sure you have installed postgresql-server-dev-all (mentioned on step 1)
  
  Because package django-emailmg has some compatibility issue with Django 1.6.5, we need to modify the following file:
  ```bash
    ./local/lib/python2.7/site-packages/emailmgr/utils.py, line 8
  ```
  Original code:
    ```bash
    from django.utils.hashcompat import sha_constructor
    ```

  Modified code:
    ```bash
    from hashlib import sha1 as sha_constructor
    ```

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
Please see: [Running unit tests](http://github.com/freedomsponsors/www.freedomsponsors.org/blob/master/doc/testing.md)
