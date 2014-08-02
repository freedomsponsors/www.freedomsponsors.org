set -e
python bootstrap
source bin/activate
cd djangoproject

coverage -e
coverage -x manage.py test --noinput core gh_frespo_integration
coverage -r -m > report.xml
# rm -Rf coverage_html_report
coverage xml '--include=core/*,gh_frespo_integration/*,bitcoin_frespo/*' '--omit=core/migrations/*,core/tests/*,bitcoin_frespo/migrations/*,gh_frespo_integration/migrations/*,gh_frespo_integration/tests/*'

cp -Rf * ../ 

