#!/bin/bash

migrate=''
requirements=''
superuser=''
shell=''

function info() {
    echo 'setup.sh [-r] for installing requirements '
    echo '         [-m] for migrations'
    echo '         [-s] for superuser'
    echo '         [-c] for shell'
    exit
}

cd school_diary

while getopts "rmsc" option
do
case "${option}" in
m) migrate='true';;
r) requirements='true';;
s) superuser='true';;
c) shell='true';;
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

if [[ -n "$shell" ]]; then
    python manage.py shell
    exit
fi

python manage.py runserver