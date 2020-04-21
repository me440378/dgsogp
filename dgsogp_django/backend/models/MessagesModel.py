from django.db import models

class Messages(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        app_label = 'backend'
        db_table = 'messages'