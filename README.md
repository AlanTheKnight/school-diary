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

Superuser account let you create other andministrators and teachers. Students register by themself.

To automatically create migrations and run the server, use our ```setup.sh``` and ```setup.bat``` files.

Linux:

    chmod +x setup.sh
    ./setup.sh
    
Windows:

    setup.bat

**Attention! Your environment need to be set up so python3 is launched using 'python' command.**
