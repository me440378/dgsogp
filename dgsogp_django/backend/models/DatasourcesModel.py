from django.db import models

class Datasources(models.Model):
    id = models.IntegerField(primary_key=True)
    wgroup = models.CharField(max_length=45)
    wserver = models.CharField(max_length=45)
    type = models.IntegerField()
    source = models.CharField(max_length=255)
    putindb = models.IntegerField(blank=True, null=True)
    related = models.IntegerField()
    pattern = models.IntegerField(blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)
    state = models.IntegerField()
    tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'backend'
        db_table = 'datasources'