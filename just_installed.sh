python -m pip install -r requirements.txt
cd school_diary
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username administrator --email ideasoft-spb@yandex.com
python manage.py runserver
