from rest_framework.views import APIView
from rest_framework.response import Response
import json
from dwebsocket.decorators import accept_websocket, require_websocket

from backend.services import DatabaseinterfacesService

##dbcli package
from backend.tools import DB
from backend.tools import MySql

class DatabaseinterfacesView(APIView):

	def get(self, request):
		result = DatabaseinterfacesService.readAll()
		return Response(result)

	def post(self, request):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = DatabaseinterfacesService.createOne(**json_dict)
		return Response(result)

class DatabaseinterfacesDetailView(APIView):

	def get(self, request, id):
		result = DatabaseinterfacesService.readOne(id)
		return Response(result)

	def put(self, request, id):
		json_bytes = request.body
		json_str = json_bytes.decode()
		json_dict = json.loads(json_str)
		result = DatabaseinterfacesService.updateOne(id, json_dict)
		return Response(result)

	def delete(self, request, id):
		result = DatabaseinterfacesService.deleteOne(id)
		return Response(result)

class DatabaseCommandLine():

	@accept_websocket
	def dbcli(request):
		if request.is_websocket():
			ws = request.websocket
			ws.send('hello world')
			json_bytes = ws.wait()
			json_str = json_bytes.decode()
			json_dict = json.loads(json_str)
			print(json_dict)
			# json_dict = json.loads(json_str)
			# json_str = json_bytes.decode()
			# print(json_dict)
			# request.websocket.wait()
			# print(dir(request.websocket)) # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_get_new_messages', '_message_queue', 'accept_connection', 'close', 'closed', 'count_messages', 'handle', 'has_messages', 'is_close', 'is_closed', 'protocol', 'read', 'send', 'wait']
			# mydb = ""
		 #    if dbtype == 'mysql':
		 #        mydb = MySql(host, port, dbname, user, pwd)

		 #    mydb.close()
			ws.wait()
		else:
			return Response({'error':1,'detail':'这是一个websocket接口'})
		