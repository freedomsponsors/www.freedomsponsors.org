export PATH=../tmp/bin:$PATH
echo '------------- RUNNING TESTS... ----------------'
./test_all.sh
code=$?
echo '------------- TESTS EXECUTION FINISHED (logs below) ----------------'
cat logs/frespo.log
exit $code