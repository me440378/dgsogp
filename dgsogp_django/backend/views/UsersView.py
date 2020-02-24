# # from django.shortcuts import render
from django.http import HttpResponse

# # from rest_framework import viewsets
from rest_framework.views import APIView

# # from backend.serializers import UsersSerializer
# # from backend.models import Users

# # class UsersView(viewsets.ModelViewSet):
class UsersView(APIView):
# # 	"""
# # 	API endpoint that allows users to be viewed or edited.
# # 	"""
# # 	queryset = Users.objects.all().order_by('-date_joined')
# # 	serializer_class = UsersSerializer

	def get(self, request):
		return HttpResponse("Helworld. Yo're at the polls index.")


class PasswordView(UsersView):

	def get(self, request):
		return HttpResponse("password!")

class ForcePasswordView(UsersView):

	def get(self, request):
		return HttpResponse("forcepassword!")
