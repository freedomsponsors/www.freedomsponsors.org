set -e
python bootstrap
source bin/activate
cd djangoproject
cp frespo/env_settings.py_template frespo/env_settings.py 

coverage -e
coverage -x manage.py test --noinput core gh_frespo_integration
coverage -r -m > report.xml
# rm -Rf coverage_html_report
coverage xml '--include=core/*,gh_frespo_integration/*,bitcoin_frespo/*' '--omit=core/migrations/*'

cp -Rf * ../ 

# coverage erase
# coverage run --source='core' '--omit=core/tests/**,core/migrations/**' manage.py test --noinput core
# coverage xml
# cp -Rf * ../../

# set -
# deactivate || : # virtualenv