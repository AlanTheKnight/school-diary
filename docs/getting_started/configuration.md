# Setting up

To work with API or improve our webiste you'll need to set up the website on your
computer. In the process of development you will work with localhost only. You need
to consider that after the deployment your code will change a little bit as well as
a host will change from ```127.0.0.1:8000``` to ```diary56.ru```, so you should
style your code to use some configuration files to switch from loaclhost (development)
to deployed version.

## Preparation

- Check that python 3.6 - 3.8, pip and git are installed.
- Create a virtual environment and activate it (optional).

## Creating settings file

Some settings like ```SECRET_KEY```, ```DEBUG``` and
database user & password are stored in special file which
is added to ```.gitignore```.

Create a file called ```settings.ini``` with the following
content

```ini
[Settings]
debug = True
secret_key_a = 9-ma2)v%g@rstsd^qmau4-+mnnjmg8jcha&6=i05hyxbvkzoks

[Email]
user = <your email>
password = <your email password>
```

Change ```user``` and ```password``` values in ```Email``` section to
your credentials.

## Clone repository

```bash
git clone https://github.com/ideasoft-spb/school-diary.git
cd school-diary
```

**Important!**
Move ```settings.ini``` file to folder with ```settings.py```
(located in ```school_diary/school_diary/``` folder).

## Further actions

### Linux & Mac

```bash
chmod +x setup.sh
./setup.sh -r -m -s
```

*In ```createsuperuser``` dialog enter ```Account type: 0```, your email and password.*  
Finally, open ```127.0.0.1:8000``` in browser.

### Windows

```batch
python -m pip install -r ../requirements.txt
python manage.py makemigrations
python manage.py migrate diary
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

In ```createsuperuser``` dialog enter ```Account type: 0```, your email and password.  
Finally, open ```127.0.0.1:8000``` in browser.
