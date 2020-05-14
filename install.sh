#!/bin/bash

echo -e "\n\n\t\tInstalling / Upgrading pip\n\n"
python -m pip install --upgrade pip
echo -e "\n\n\t\tInstalling / Upgrading virtualenv\n\n"
pip install virtualenv
echo -e "\n\n\t\tCreating virtual environment \"virtualenv\"\n\n"
virtualenv virtualenv
echo -e "\n\n\t\tActivating virtual environment \"virtualenv\"\n\n"
. virtualenv/Scripts/activate
echo -e "\n\n\t\tInstalling dependencies in virtual environment \"virtualenv\"\n\n"
pip install -r requirements.txt
echo -e "\n\n\t\tRunning app\n\n"
py app/app.py
echo -e "\n\n\t\tRun \". virtualenv/Scripts/activate\" to use the virtual environment.\n\n"
