./manage.py test core --settings=frespo.test_settings
code1=$?
./manage.py test core_splinter_tests
code2=$?
code=$(expr $code1 + $code2)
exit $code