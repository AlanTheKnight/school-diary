#!/bin/bash

migrate=''
requirements=''
superuser=''

function info() {
    echo 'setup.sh [-r] for installing requirements '
    echo '         [-m] for migrations'
    echo '         [-s] for superuser'
    exit
}

cd school_diary

while getopts "rms" option
do
case "${option}" in
m) migrate='true';;
r) requirements='true';;
s) superuser='true';;
*) info
esac
done

if [[ -n "$requirements" ]]; then
    python -m pip install -r ../requirements.txt
fi

if [[ -n "$migrate" ]]; then
    python manage.py makemigrations
    python manage.py migrate diary
    python manage.py migrate
fi

if [[ -n "$superuser" ]]; then
    echo "Creating a super user..."
    python manage.py createsuperuser
fi

python manage.py runserver