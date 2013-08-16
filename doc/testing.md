If you can run FreedomSponsors on your machine, you should also be able to run unit tests.

# Running unit tests

Make sure you're in the virtual environment

```shell
www.freedomsponsors.org$ source bin/activate

```

run tests
```shell
www.freedomsponsors.org$ cd djangoproject
djangoproject$ ./manage.py test core gh_frespo_integration

```

This will run all tests in packages 'core' and 'gh_frespo_integration'

# Running splinter tests

There is another set of tests that need additional setup before they can be ran.
Those tests live in the 'core_splinter_tests' package, and they use [Splinter](https://github.com/cobrateam/splinter) (a wrapper around Selenium). 

Those tests assume that you have chrome (or chromium) installed, and that you have chromedriver in your path.
If you don't have that, skip to the next section and then come back here.

run tests
```shell
djangoproject$ ./manage.py test core core_splinter_tests

```

It should start some browser instances and run some tests (have fun watching :-))

# Setup chromedriver

If you don't have Chrome or Chromium, use this command to install chromium:

```
sudo apt-get install chromium-browser
```

There are some `.sh` files in the djangoproject folder that run some tests (`test_all.sh`, `test_splinter.sh`, `coverage.sh`).
Those files are only there because I tend to have a hard time remembering commands :P.

Download the latest version of chromedriver:
https://code.google.com/p/chromedriver/downloads/list

Get the appropriate version for your OS, and unzip it somewhere (I used `~/bin`)

make sure the folder where you unzipped it is in the system path, and that the file is executable:

```shell
export PATH=$PATH:~/bin
chmod +x ~/bin/chromedriver
```

ok, that's it.

# Generating coverage reports

Did you know we have public test coverage reports?
Here: http://freedomsponsors.github.io/www.freedomsponsors.org/coverage_html_report/

You can generate those reports locally, by running:

```
djangoproject$ ./coverage.sh
```

The reports will be at djangoproject/coverage_html_report/index.html

# Help out

If you find the instructions above are incorrect or incomplete, please feel free to add an issue (or a pull request)
