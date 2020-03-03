python -m pip install -r requirements.txt
cd school_diary
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
