from django.db import models

class Hadoopsources(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.IntegerField()
    source = models.CharField(max_length=255)
    datasource_id = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'backend'
        db_table = 'hadoopsources'