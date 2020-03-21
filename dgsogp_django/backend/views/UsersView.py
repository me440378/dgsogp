from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import UsersService

class UsersView(APIView):

	def get(self, request):
		select = request.GET.get('select')
		key = request.GET.get('key')
		if select and key:
			result = UsersService.readByCondition(select, key)
			return Response(result)
		else:
			result = UsersService.readAll()
			return Response(result)

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = UsersService.register(**json_dict)
		return Response(result)


class UsersDetailView(APIView):

	def get(self, request, id):
		result = UsersService.readOne(id)
		return Response(result)

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = UsersService.updateOne(id, json_dict)
		return Response(result)

	def delete(self, request, id):
		result = UsersService.deleteOne(id)
		return Response(result)


class PasswordView(APIView):

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = UsersService.updatePassword(id, **json_dict)
		return Response(result)


class ForcePasswordView(APIView):

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = UsersService.updateForcePassword(id, **json_dict)
		return Response(result)


class LoginView(APIView):

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = UsersService.login(**json_dict)
		return Response(result)

