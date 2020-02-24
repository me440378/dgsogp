from django.db import models

class Metadata(models.Model):
    id = models.IntegerField(primary_key=True)
    amount = models.IntegerField()
    feature = models.IntegerField()
    hashsum = models.CharField(max_length=255)
    type = models.CharField(max_length=45)
    format = models.CharField(max_length=45)
    datasource_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'metadata'