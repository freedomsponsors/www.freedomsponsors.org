#!/bin/bash
BOOTSTRAP=`dirname $0`
VENV=$BOOTSTRAP/..
source $VENV/bin/activate && $@
