#!/bin/bash

python -m pip install --upgrade pip
pip install virtualenv
virtualenv virtualenv
. virtualenv/Scripts/activate
pip install -r requirements.txt
