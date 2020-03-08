from rest_framework import serializers
from backend.models import Users

class UsersSerializer(serializers.ModelSerializer):

	created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

	class Meta:
		model = Users
		fields = ('id', 'username', 'nickname', 'created_at')