<div align="center">

# School Diary

Open-source digital diary website for schools made with Django.

<img alt="Python 3.9+" src="https://img.shields.io/badge/Python_Version-3.9+-blue.svg">
<img alt="Python 3.9+" src="https://img.shields.io/badge/License-MIT-yellow.svg">


## This project uses

<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
<img alt="Django" src="https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/>
<img alt="JavaScript" src="https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/>
<img alt="HTML5" src="https://img.shields.io/badge/html5%20-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white"/>
<img alt="CSS3" src="https://img.shields.io/badge/css3%20-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white"/>
<img alt="Vue.js" src="https://img.shields.io/badge/vuejs%20-%2335495e.svg?&style=for-the-badge&logo=vue.js&logoColor=%234FC08D"/>
<img alt="Bootstrap" src="https://img.shields.io/badge/bootstrap%20-%23563D7C.svg?&style=for-the-badge&logo=bootstrap&logoColor=white"/>
<img alt="SQLite" src ="https://img.shields.io/badge/sqlite-%2307405e.svg?&style=for-the-badge&logo=sqlite&logoColor=white"/>
<img alt="Postgres" src ="https://img.shields.io/badge/postgres-orangered.svg?&style=for-the-badge&logo=postgresql"/>

## Screenshots

![](screenshots/1.png)

![](screenshots/2.png)

![](screenshots/3.png)

## Development setup

<div align="left">

### Preparation

Make sure you've installed Python 3.9+ and added it to `PATH`.
It's recommended to create an empty virtual environment before
installing dependencies.

### Installing dependencies

```
pip install poetry
poetry install
```

### Adding settings file

Create a file called `config.toml` in the root directory
of the project (the same where `manage.py` is located) with
the following content:

```toml
[main]
debug = true
secret_key = "<django secret key>"
allowed_hosts = ['127.0.0.1', 'localhost']

[email]
host = "<smtp server>"
address = "<email address>"
password = "<email passoword>"
port = "<smpt server port>"
use_tls = true
use_ssl = true

[other]
admins = [
    ['<name>', '<email>'],
    ['<name2>', '<email2>']
]

[database]
[database.postgres]
name = "<db name>"
user = "<db user>"
password = "<db password>"
host = "<db host>"
port = "<db port>"

[database.sqlite]
name = "db.sqlite3"

```


### Django stuff

```
cd school_diary
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Then open https://127.0.0.1:8000 and enjoy.

</div>

## Contact us

<a href="mailto:ideasoft.spb@gmail.com"><img alt="Gmail" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"/></a>
<a href="https://t.me/AlanTheKnight"><img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>

</div>

