# School Diary

## Setting up project on your computer

Clone this repository.

Then activate your virtual environment and install requirements:

    python -m pip install -r requirements.txt

Make migrations to database:

    python manage.py makemigrations
    python manage.py migrate

Before you will run server, create superuser account:

    python manage.py createsuperuser
    Email: your_email@email.com
    Account type: 0
    Password: somerandompassword

Now you can run server.

    python manage.py runserver

Go to 127.0.0.1:8000 in your browser and enjoy our website.

Superuser account let you create other administrators and teachers. Students register by themself.

### Tip: easier way for Linux users

Linux users can also use ``setup.sh`` file, that is located in the root folder.

    chmod +x setup.sh
    ./setup.sh

Usage:

    setup.sh [-r] for installing requirements
             [-m] for migrations
             [-u] for superuser
             [-s] for django shell
             [-t] for test

## Screenshots

![Teacher account](https://sun9-13.userapi.com/c856132/v856132311/21cdaf/2UbbgjtKKPs.jpg)

![Teacher interface](https://sun9-46.userapi.com/c856132/v856132311/21cda5/0hD1H2vYibQ.jpg)

## Useful functions

### Creating a map with all models in project

    pip install pyparsing pydot
    sudo apt install python-pydot python-pydot-ng graphviz
    python manage.py graph_models --pydot -a -g -o my_project_visualized.png

### List all urls in the project

    python manage.py show_urls

## Code styling & recommendations

- It's highly recommended using a linter, for example, *flake8*.
- Lines maximal length is 99 symbols (comments and docstrings are 79).
- Follow [PEP8](https://pep8.org)
- Indent using 4 spaces

We highly prefer using ```{% url %}``` tags is than using simple links because the address can be changed easily without changing any code. If you need to pass some parameters inside, use 
```{% url 'some_name' page=1 %}``` as keyword argument and ```{% url 'some_name' 1 %}``` as a positional one.

Also our Django views are **NOT** using class-based views.

As it was mentioned, you can create a cool .png map with all models and their connections.
There you will be able to see that we have the most part of our model created inside 'diary'
app. That's because before we started doing a code review and refresh our legacy code, almost all
of the project was there. Then we separated it and increased the readability of our code.
Anyway, traditionally we want to keep most of the models in the one app and import them from others.
That's it.
