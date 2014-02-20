from django.db import models	
from django.contrib.auth.models import User

class FacebookProfile(models.Model):
    user = models.ForeignKey(User)
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(
        max_length=250
        )

    def __unicode__(self):
        return "{0}".format(self.user)

class contacts(models.Model):
    user = models.ForeignKey(User)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    alternateNumber = models.CharField(max_length=15)
