from rest_framework import serializers
from backend.models import Hadoopsources

class DatasourcesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Hadoopsources
		fields = ('id', 'source', 'dbstate', 'state', 'datasource_id', 'format')
