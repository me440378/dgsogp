from django.db import models

class Metadata(models.Model):
    id = models.IntegerField(primary_key=True)
    source = models.CharField(max_length=255)
    amount = models.IntegerField(blank=True, null=True)
    feature = models.IntegerField(blank=True, null=True)
    hashsum = models.CharField(max_length=255)
    datasource_id = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'backend'
        db_table = 'metadata'