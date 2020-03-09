from django.db import models

class Datainterfaces(models.Model):
	id = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    name = models.CharField(max_length=255)
    metadata_id = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'backend'
        db_table = 'datainterfaces'