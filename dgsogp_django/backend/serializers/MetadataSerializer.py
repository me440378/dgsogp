from rest_framework import serializers
from backend.models import Metadata

class MetadataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Metadata
		fields = ('id', 'source', 'amount', 'feature', 'hashsum', 'hadoopsource_id', 'format', 'state')
