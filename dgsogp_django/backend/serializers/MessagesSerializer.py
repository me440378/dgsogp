from rest_framework import serializers
from backend.models import Messages

class MessagesSerializer(serializers.ModelSerializer):

	created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

	class Meta:
		model = Messages
		fields = ('id', 'name', 'content', 'status', 'created_at')