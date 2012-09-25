www.freedomsponsors.org 
=======================

[![Build Status](https://secure.travis-ci.org/freedomsponsors/www.freedomsponsors.org.png)](http://travis-ci.org/freedomsponsors/www.freedomsponsors.org)

FreedomSponsors is a Django web application.

FS is made by, and for developers. 
If you'd like to help (bug reports, suggestions, or even code), you are more than welcome.
Please take a look at the open issues.

Instructions to run application locally:

```shell
# 1. Clone repo
git clone git://github.com/freedomsponsors/www.freedomsponsors.org.git

# 2. Create a 'frespo' database on postgres (default username and password is 'frespo')

# 2.1 Install misaka and pygments

    sudo pip install misaka
    sudo pip install pygments

# 3. Configure settings
mv frespo/env_settings.py_template frespo/env_settings.py
nano frespo/env_settings.py #edit according to your environment

# 3. Create database objects
cd www.freedomsponsors.org/djangoproject
./manage.py syncdb
./migrate.sh

# 4. Populate with some initial data
./manage.py loadFeedbackData
./manage.py loadProjects

# 5. Run!
./manage.py runserver # and visit http://localhost:8000
```

(If you find that the steps above are not actually accurate, please [open a new issue to let us know](https://github.com/freedomsponsors/www.freedomsponsors.org/issues/new)!)

You should also verify if you can run all the automatic tests successfully.
You will need to install [Splinter](https://github.com/cobrateam/splinter) (a Selenium wrapper), and you will also need need to create two test gmail accounts (and then specify username and password in your env_settings.py file).

Then you can run tests using

```shell
./manage.py test core
```

Also, there is a fully-functional test-environment at http://ambtest.freedomsponsors.org.
Feel free to use it as you like (might be useful when reading the code!). We provide no guarantee about the data on it though!

This software is licensed under the [AFFERO GENERAL PUBLIC LICENSE](http://www.gnu.org/licenses/agpl-3.0.html)
