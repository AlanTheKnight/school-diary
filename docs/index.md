# Get started

## About this documentation

This documentation describes API and code of [diary for students](https://diary56.ru).
As you see, despite the fact that this diary was made for Russians only, we are writing
this documentation in English with hope it's not going to be a big problem.

For some people, especially who are not living in Russia, the idea of diary can be
a little bit strange. In our system of education, every student has a record book with
his/her marks. These books are getting more and more useless and recently they've been
replaced by e-diaries - systems for storing and managing marks of students by their teachers.

## What API allows you to do

Using our API, you can built your own app or extension for diary. Here is a simple exmaple of
what API can be used for. In this example Python request are used to get a list of post from our
news section.

```python
    import requests
    import json

    url = 'https://diary56.ru/api/'

    # Getting a token for permission
    r = requests.post(url + 'auth/', {
        'username': 'username1234',
        'password': 'password1234'
    })
    token = 'Token ' + json.loads(r.content.decode())['token']
    headers = {'Authorization': token}

    # Getting posts
    r = requests.get(url + 'news/', headers=headers)
    print(json.loads(r.content.decode()))
```

As result, you are going to get something like that:

```python
    [{'date': '2020-06-02T16:33:55.631140+03:00', 'title': 'Список литературы на лето', 'author': 'Admin', 'content': 'Текст', 'slug': 'list-of-summer-literature', 'image': 'https://diary56.ru/media/news/book-shielf.png'}]
```

In similar way you can create new posts, update them and do lots of other things.

## Setting up on localhost

To work with API or improve our webiste you'll need to set up the website on your
computer. In the process of development you will work with localhost only. You need
to consider that after the deployment your code will change a little bit as well as
a host will change from ```127.0.0.1:8000``` to ```diary56.ru```, so you should
style your code to use some configuration files to switch from loaclhost (development)
to deployed version.

### Linux & Mac

Check that ```python3``` is installed and create a virtual environment.
You can use any version of python from 3.6 to 3.8. Commands below
install git and virtualenv, creates a new virtual environment, clones
our github repository and runs ```setup.sh``` script.
This script is going to install needed requirements, make migrations and migrate
them into a database (sqlite used by default) as well as create a new superuser.  

```bash
    sudo apt-get install python-virtualenv git
    virtualenv --python=/usr/bin/python3 venv
    source ./venv/bin/activate
    git clone https://github.com/ideasoft-spb/school-diary.git
    cd school-diary
    chmod +x setup.sh
    ./setup.sh -r -m -s
```

In ```createsuperuser``` dialog enter ```Account type: 0```, your email and password.

Then open ```127.0.0.1:8000``` in browser.

### Windows

Install the following programs:

- [Git](https://git-scm.com/download/win)
- [Python 3.6 - 3.8](https://python.org/downloads/)

**It's highly recommended to create a virtual environment before installing the requirements.**

Run these commands:

```batch
    git clone https://github.com/ideasoft-spb/school-diary.git
    cd school-diary/school_diary
    python -m pip install -r ../requirements.txt
    python manage.py makemigrations
    python manage.py migrate diary
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
```

In ```createsuperuser``` dialog enter ```Account type: 0```, your email and password.

Then open ```127.0.0.1:8000``` in browser.
