from rest_framework import serializers
from backend.models import Hadoopsources

class HadoopsourcesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Hadoopsources
		fields = ('id', 'source', 'state', 'datasource_id')
