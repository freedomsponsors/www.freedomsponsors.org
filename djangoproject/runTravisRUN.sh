export PATH=../tmp/bin:$PATH
echo '------------- RUNNING TESTS... ----------------'
./manage.py test core_splinter_tests core --settings=frespo.test_settings
code=$?
echo '------------- TESTS EXECUTION FINISHED (logs below) ----------------'
cat logs/frespo.log
exit $code


