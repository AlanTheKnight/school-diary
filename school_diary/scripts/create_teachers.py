from core import models
import getpass


def run():
    for i in range(0, int(input("Enter amount of teachers you want to create: "))):
        email = input("Email: ")
        fn = input("First name: ")
        surname = input("Surname: ")
        sn = input("Second name: ")
        password = getpass.getpass(prompt="Password: ")
        confirm = input("Comfirm (y/n)") == 'y'
        if confirm:
            user = models.Users.objects.create_user(email=email)
            user.set_password(password)
            user.account_type = 2
            user.is_staff = False
            user.is_superuser = False
            user.save()
            teacher = models.Teachers.objects.create(
                account=user, first_name=fn, second_name=sn, surname=surname
            )
            teacher.save()

