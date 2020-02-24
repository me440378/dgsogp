from rest_framework import serializers
from backend.models import Users

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = ('id','username','nickname')