#!/bin/sh
# Coverage utility script

coverage -e
coverage -x manage.py test core --settings=frespo.test_settings
coverage -r -m > report.xml
