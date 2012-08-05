www.freedomsponsors.org
=======================

FreedomSponsors is a Django web application.
Help and pull requests are welcome!

To run app locally, follow these steps:

```shell
# 1. Clone repo
git clone git://github.com/freedomsponsors/www.freedomsponsors.org.git

# 2. Create a 'frespo' database on postgres (default username and password is 'frespo')

# 3. Configure settings
cd www.freedomsponsors.org/djangoproject
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