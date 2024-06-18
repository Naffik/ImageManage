from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,
                                     null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)

    def __str__(self):
        return 'Profil użytkownika {}'.format(self.user.username)


class AccountTier(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    thumbnail_size = models.CharField(max_length=255, null=False, blank=False)
    original_link = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)
    expiring_link_duration_min = models.IntegerField(default=300)
    expiring_link_duration_max = models.IntegerField(default=30000)

    def __str__(self):
        return self.name
