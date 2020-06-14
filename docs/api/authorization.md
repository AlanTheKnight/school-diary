# Authorization

For security purposes, API of our diary is locked for unauthenticated users.
To start using it on localhost, you will need to to several things.

1. Open a project folder containing ```manage.py```
2. Create a new account on the website (skip if it was already created).
3. Run ```python manage.py shell```
4. Then do the following commands in the shell:

        from diary.models import Users
        from api.models import AllowedToUseAPIList

        user = Users.objects.get(email="USER EMAIL HERE")

        new = AllowedToUseAPIList.objects.create(user=user)
        new.save()

    The following commands will get your user from database by it's email,
    then add it to list of users who are allowed to use API.

Now let's try out new permissions to get our user token using [httpie](https://httpie.org/), for example:

    http POST http://127.0.0.1:8000/api/auth/ username=username password=password

Of course, don't forget to provide your email & password. You are going to get a token, something like that:

    {"token":"<your-token-here>"}

Let's also try to use this token to get some data from our API, like news.

    http GET http://127.0.0.1:8000/api/news/ 'Authorization: Token <your-token-here>'

That was all you need to do for the authentication. This process in production is the same except
the website address is going to change from *102.0.0.1* to *diary56.ru* and the user is going to be
added to ```AllowedToUseAPIList``` after you will contact us.
