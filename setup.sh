#!/bin/bash

migrate=''
requirements=''
superuser=''
shell=''
testing=''

function info() {
    echo 'setup.sh [-r] for installing requirements '
    echo '         [-m] for migrations'
    echo '         [-u] for superuser'
    echo '         [-s] for shell'
    echo '         [-t] for test'
    exit
}

cd school_diary

while getopts "mrusth" option
do
case "${option}" in
m) migrate='true';;
r) requirements='true';;
u) superuser='true';;
s) shell='true';;
t) testing='true';;
h) info
esac
done

if [[ -n "$requirements" ]]; then
    python -m pip install -r ../requirements.txt
    exit
fi

if [[ -n "$migrate" ]]; then
    python manage.py makemigrations
    python manage.py migrate
    exit
fi

if [[ -n "$superuser" ]]; then
    echo "Creating a super user..."
    python manage.py createsuperuser
    exit
fi

if [[ -n "$testing" ]]; then
    python manage.py test
    exit
fi

if [[ -n "$shell" ]]; then
    python manage.py shell
    exit
fi

python manage.py runserver