from django.db import models

class Datasources(models.Model):
    id = models.IntegerField(primary_key=True)
    wgroup = models.CharField(max_length=45)
    wserver = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    source = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'backend'
        db_table = 'datasources'