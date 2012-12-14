import sys
import subprocess
from os.path import abspath, join, dirname


# the below syntax works on both 2.6 and 2.7.
print "Bootstraping Virtualenv for Python {0}.{1}".format(*sys.version_info)

DIR    = dirname(__file__)
module = "bootstrap{0}.{1}.py".format(*sys.version_info)
script = abspath(join(DIR, module))

subprocess.call([sys.executable, script])
