from rest_framework import serializers
from backend.models import Datasources

class DatasourcesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Datasources
		fields = ('id', 'wgroup', 'wserver', 'type', 'source', 'putindb', 'related', 'pattern', 'target', 'state', 'tag')