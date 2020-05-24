# School Diary

## Setting up project on your computer

Download or clone this repository.

Send an email to ideasoft-spb@yandex.com asking the permission to run our website. 
We will send you back and email with .ini file you need to copy to the folder where settings.py is located. After that, change some values in .ini file and set 'user' and 'password' values in 'Email' section - these are login and password for email account (we use Yandex, probably you will need to change port in settings.py). 
Also it contains some fields for PostgreSQL database. You can ignore this values until you'll want to turn debug mode to false. Debug mode is also located in .ini file ('Settings' section contains debug and secret_key variables). To change debug to False, specify an empty value:

    [Section]
    debug = 

Any debug value except an empty one will turn on debug mode.

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
    
Go to http://127.0.0.1:8000/ in your browser and enjoy our diary.

Superuser account let you create other administrators and teachers. Students register by themself.

To automatically create migrations and run the server, use our ```setup.sh``` and ```setup.bat``` files.

Linux:

    chmod +x setup.sh
    ./setup.sh
    
Windows:

    setup.bat

**Attention! Your environment need to be set up so python3 is launched using 'python' command.**

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
