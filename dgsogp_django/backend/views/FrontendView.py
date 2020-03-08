from rest_framework.views import APIView
from rest_framework.response import Response
import json

from backend.services import FrontendService

class FrontendView(APIView):
	pass

class DashboardView(APIView):

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		print(json_dict)
		result = FrontendService.getDashboardData(**json_dict)
		return Response(result)

class HeaderView(APIView):

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = FrontendService.getHeaderData(**json_dict)
		return Response(result)
		
	# def post(self, request):
	# 	json_bytes = request.body
	# 	json_str = json_bytes.decode()
	# 	json_dict = json.loads(json_str)
	# 	result = DatasourcesService.createOne(**json_dict)
	# 	return Response(result)

	# def get(self, request, id):
	# 	result = DatasourcesService.readOne(id)
	# 	return Response(result)