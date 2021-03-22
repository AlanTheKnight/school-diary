from django.db import models

from apps.core.models import Users


class AllowedToUseAPIList(models.Model):
    """
    Model representing a list of users who are
    allowed to use API.
    """
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Разрешение на доступ к API"
        verbose_name_plural = "Доступ к API"

    def __str__(self):
        return "{} - ({})".format(self.user.email, self.user.account_type)
