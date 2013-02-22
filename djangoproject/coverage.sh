#!/bin/sh
# Coverage utility script
set -e
coverage -e
# coverage -x manage.py test core gh_frespo_integration core_splinter_tests
coverage -x manage.py test core core_splinter_tests
coverage -r -m > report.xml
rm -Rf coverage_html_report
# coverage html '--include=core/*,gh_frespo_integration/*,bitcoin_frespo/*' '--omit=core/migrations/*'
coverage html '--include=core/*,bitcoin_frespo/*' '--omit=core/migrations/*'
