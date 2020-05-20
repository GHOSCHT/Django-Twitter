from django.db import models

# Create your models here.


class TwitterUser(models.Model):
    username = models.CharField(max_length=15)
    search_date = models.DateTimeField(auto_now=True)
