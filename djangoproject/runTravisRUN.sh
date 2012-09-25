export PATH=../tmp/bin:$PATH
echo '------------- RUNNING TESTS... ----------------'
./manage.py test core
code=$?
echo '------------- TESTS EXECUTION FINISHED (logs below) ----------------'
cat logs/frespo.log
exit $code


