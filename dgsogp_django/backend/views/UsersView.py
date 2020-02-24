from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import UsersService

class UsersView(APIView):

	def get(self, request):
		result = UsersService.getAll()
		return Response(result)

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = UsersService.register(**json_dict)
		return Response(result)


class UsersDetailView(APIView):
	pass

class PasswordView(APIView):

	def get(self, request):
		return HttpResponse(md5hash("password!"))


class ForcePasswordView(APIView):

	def get(self, request):
		return HttpResponse("forcepassword!")
