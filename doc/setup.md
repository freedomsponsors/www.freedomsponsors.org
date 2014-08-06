## Operating system

FreedomSponsors uses a few python libs that I could never get to work properly on Windows or Mac.
That means you need linux to get FS running on your machine.

You can get Ubuntu VMs for VirtualBox [here](http://virtualboxes.org/images/ubuntu/). 

Alternatively, you can [run FS in sandbox mode](https://github.com/freedomsponsors/www.freedomsponsors.org/blob/master/doc/windows.md) (no database, good enough to work with html/css/js only)

## Running

Instructions to run application locally:

1. Install Postgresql and some other needed libs

  ```bash
  $ sudo apt-get update --fix-missing
  $ sudo apt-get install postgresql postgresql-server-dev-all \
  python-dev python-lxml libxslt-dev libpq-dev pgadmin3
  ```

2. Clone the repo.

  ```bash
  $ git clone git://github.com/freedomsponsors/www.freedomsponsors.org.git
  $ cd www.freedomsponsors.org
  ```

3. Create the database/default user.
  
  ```bash
  $ sudo su postgres #run the next command as postgres
  $ createuser -d -SRP frespo # this will prompot you to create a password (just use frespo for now)
  $ createdb -O frespo frespo
  $ exit # go back to your normal user
  ```

4. Create a virtualenv and install dependencies.

  ```bash
  $ python bootstrap
  ```

  This will create a python virtualenv and install all dependecies listed on `requirements.txt` on it.
  If this command fails because of psycopg2, make sure you have installed postgresql-server-dev-all (mentioned on step 1)

  Then you can activate the virtualenv:

  ```bash
  $ source bin/activate
  ```

  To deactivate the virtualenv

  ```bash
  $ deactivate
  ```

  **Remember**: You'll need to be in the virtual environment to use `./manage.py ...` commands

5. Create database objects.

  ```bash  
  $ cd djangoproject
  $ ./manage.py syncdb --migrate --noinput
  ```

6. Run!

  ```bash
  $ ./manage.py runserver # and visit http://localhost:8000
  ```

Next: 
* [make sure you can run unit tests](http://github.com/freedomsponsors/www.freedomsponsors.org/blob/master/doc/testing.md)
* [Customize your settings](http://github.com/freedomsponsors/www.freedomsponsors.org/blob/master/doc/custom_settings.md)
