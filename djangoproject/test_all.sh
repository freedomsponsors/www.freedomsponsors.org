export TEST_DBMS=SQLITE
./manage.py test core
code1=$?
export TEST_DBMS=POSTGRES
./manage.py test core_splinter_tests
code2=$?
code=$(expr $code1 + $code2)
exit $code