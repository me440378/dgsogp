from rest_framework import serializers
from backend.models import Metadata

class MetadataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Metadata
		fields = ('id', 'amount', 'feature', 'hashsum', 'type', 'format', 'datasource_id')