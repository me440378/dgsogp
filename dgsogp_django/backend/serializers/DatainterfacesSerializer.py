from rest_framework import serializers
from backend.models import Datainterfaces

class DatainterfacesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Datainterfaces
		fields = ('id', 'type', 'name', 'metadata_id')