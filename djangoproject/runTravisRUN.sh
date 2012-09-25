export PATH=../tmp/bin:$PATH; 
echo '------------- RUNNING TESTS... ----------------'; 
code=$(./manage.py test core); 
echo '------------- TESTS EXECUTION FINISHED (logs below) ----------------'; 
cat logs/frespo.log; 
exit $code


