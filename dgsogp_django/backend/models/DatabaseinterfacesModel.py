from django.db import models

class Databaseinterfaces(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    wserver = models.CharField(max_length=255)
    wport = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    datasource_id = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'backend'
        db_table = 'databaseinterfaces'