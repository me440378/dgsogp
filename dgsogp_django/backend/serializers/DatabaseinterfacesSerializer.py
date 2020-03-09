from rest_framework import serializers
from backend.models import Databaseinterfaces

class DatabaseinterfacesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Databaseinterfaces
		fields = ('id', 'type', 'wserver', 'wport', 'name', 'datasource_id')