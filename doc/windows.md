It's possible to run a limited environment for FreedomSponsors on windows.
This environment can be used for front-end development (only)

To run a fully functional environment, the webapp needs more python dependencies and not all of them play nice with windows.
(You can try, though - maybe you`ll suceed where I failed :-))

Anyway the steps below will tell you how you can get a front-end dev environment up.

## 1. Install Python2
Get it: [win32](http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi) or [amd64](http://www.python.org/ftp/python/2.7.6/python-2.7.6.amd64.msi)

## 2. Install SetupTools 

Get it: [win32](http://www.lfd.uci.edu/~gohlke/pythonlibs/dmemghrp/setuptools-1.3.2.win32-py2.7.exe) or [amd64](http://www.lfd.uci.edu/~gohlke/pythonlibs/dmemghrp/setuptools-1.3.2.win-amd64-py2.7.exe)

## 3. Install pip

Get it: [win32](http://www.lfd.uci.edu/~gohlke/pythonlibs/dmemghrp/pip-1.4.1.win32-py2.7.exe) or [amd64](http://www.lfd.uci.edu/~gohlke/pythonlibs/dmemghrp/pip-1.4.1.win-amd64-py2.7.exe)

## 4. Fix your PATH

You need to make sure you can run pip.
Windows has and environment variable named PATH that tells it where to search for executables on the command line.
After you install pip with the command above, pip.exe is placed at C:\Python27\Scripts, but that folder is not in the PATH.
You need to manually change PATH to include it. To edit your path:

* Open Windows Explorer and click "Computer" or "My Computer"

![Click properties](https://raw.github.com/freedomsponsors/www.freedomsponsors.org/master/doc/win_properties.png)

* Click on "advanced settings"

![Advanced Settings](https://raw.github.com/freedomsponsors/www.freedomsponsors.org/master/doc/win_config.png)

* Click on "environment variables"

![Click Environment Variables](https://raw.github.com/freedomsponsors/www.freedomsponsors.org/master/doc/win_click_envvars.png)

* Find the PATH variable and edit

![Click Environment Variables](https://raw.github.com/freedomsponsors/www.freedomsponsors.org/master/doc/win_path.png)

* Add ";C\Python27\Scripts" and close everything

![Click Environment Variables](https://raw.github.com/freedomsponsors/www.freedomsponsors.org/master/doc/win_path_edit.png)

Now open a new cmd prompt and type "pip" to see if cmd can find it. If not, review your steps!

## 5. Install virtualenv

On your prompt type

```
pip install virtualenv
```

## 6. Fork/clone this repo.

If you haven't already, fork and clone this repo.
Then open a cmd prompt and cd into it.

## 7. Create a virtualenv called ENV

```
C:\work\solo\www.freedomsponsors.org>virtualenv ENV
```

## 8. Activate your newly created virtualenv

Whenever you're working on the project you need to have this virtualenv activated.

```
C:\work\solo\www.freedomsponsors.org>ENV\Scripts\activate
(ENV) C:\work\solo\www.freedomsponsors.org>
```

Notice how the prompt changes to tell you that you're in the (ENV) virtualenv
To deactivate the virtualenv, simply type

```
deactivate
```

## 9. Install FreedomSponsors python dependencies (make sure you activate your virtualenv first!)

```
C:\work\solo\www.freedomsponsors.org>ENV\Scripts\activate
(ENV) C:\work\solo\www.freedomsponsors.org>pip install -r requirements-win.txt
```

## 10. Run the webapp

```
(ENV) C:\work\solo\www.freedomsponsors.org>cd djangoproject
(ENV) C:\work\solo\www.freedomsponsors.org\djangoproject>manage.py runserver --settings=frespo.settings_sandbox
```

Now point your browser to http://localhost:8000/sandbox
Sweet. :-)

You wanna know that:

* Templates (html) live in the `djangoproject\templates\core2` directory,
* Static files (css/js) live in `djangoprojects\statfiles`
* Routes are configured in `djangoproject\sandbox\urls.py`
* Fake data for the pages is set on `djangoproject\sandbox\views.py`

If you find any mistakes in the instructions above, don't hesitate to open an issue!

