from django.db import models
from django.conf import settings

from images.models import Image


class AccountTier(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    thumbnail_size = models.CharField(max_length=255, null=False, blank=False)
    original_link = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)
    expiring_link_duration_min = models.IntegerField(default=300)
    expiring_link_duration_max = models.IntegerField(default=30000)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,
                                     null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return 'User {} profile'.format(self.user.username)

    def image_count(self):
        images = Image.objects.filter(user=self.user)
        return images.count()