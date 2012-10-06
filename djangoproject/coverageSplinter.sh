#!/bin/sh
# Coverage utility script

export COVERAGE_PROCESS_START=.coveragerc
coverage -e
coverage -x manage.py test core_splinter_tests
coverage -r -m > report.xml
coverage html '--include=core/*'
