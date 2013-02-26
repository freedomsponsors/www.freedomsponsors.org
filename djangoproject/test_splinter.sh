export DISPLAY=:99.0
export ENV_SETTINGS=test_settings
/sbin/start-stop-daemon --start --quiet --pidfile /tmp/cucumber_xvfb_99.pid --make-pidfile --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1280x1024x16
./manage.py test core_splinter_tests
killall Xvfb