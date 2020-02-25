from rest_framework import serializers
from backend.models import Metadata

class MetadataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Metadata
		fields = ('id', 'wgroup', 'wserver', 'type', 'source')