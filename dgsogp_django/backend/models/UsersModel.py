from django.db import models

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'backend'
        db_table = 'users'