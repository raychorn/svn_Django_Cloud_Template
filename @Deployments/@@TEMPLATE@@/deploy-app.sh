#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:/usr/local/@@TEMPLATE@@/vyperlogix_2_7_0.zip:/usr/share/pyshared
#python ./deploy-app.py --name=$1 --verbose
python ./deploy-app.py --netstat --verbose

