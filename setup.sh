python3 -m pip install -r requirements.txt
cd school_diary
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --username administrator --email ideasoft-spb@yandex.com
python3 manage.py runserver
