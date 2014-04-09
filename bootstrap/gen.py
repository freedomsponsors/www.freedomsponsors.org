# coding: utf-8
"""
Only use this if you want to update a bootstrapV.M.py file to a newer virtualenv!

Usage:
/path/to/specific/version/of/python gen.py
"""

import sys
import virtualenv


EXTENSION = """
# coding: utf-8
import os
from os.path import abspath, basename, dirname, join, pardir
import subprocess


# get current dir
def adjust_options(options, args):
    from hooks import VIRTUALENV

    # erase args
    while len(args):
        args.pop()

    # set virtualenv's dir
    args.append(VIRTUALENV)

# override default options
def extend_parser(parser):
    parser.set_defaults(unzip_setuptools=True,
                        use_distribute=True)


# delegate the final hooks to an external script so we don't need to change this.
def after_install(options, home_dir):
    from hooks import after_install
    after_install(options, home_dir)
"""


# the below syntax works on both 2.6 and 2.7.
filename = "bootstrap{0}.{1}.py".format(*sys.version_info)
output = virtualenv.create_bootstrap_script(EXTENSION)
f = open(filename, 'w').write(output)
