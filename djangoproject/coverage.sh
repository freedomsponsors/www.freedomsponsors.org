#!/bin/sh
# Coverage utility script
set -e
coverage -e
coverage -x manage.py test core gh_frespo_integration core_splinter_tests
coverage -r -m > report.xml
rm -Rf coverage_html_report
coverage html '--include=core/*' '--omit=core/migrations/*'
