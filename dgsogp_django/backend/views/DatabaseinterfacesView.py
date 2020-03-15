from rest_framework.views import APIView
from rest_framework.response import Response
import json
from dwebsocket.decorators import accept_websocket, require_websocket

from backend.services import DatabaseinterfacesService

##dbcli package
from backend.tools import DB
from backend.tools import MySql
import pymysql

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
			json_bytes = ws.wait()
			json_str = json_bytes.decode()
			json_dict = json.loads(json_str)
			print(json_dict)
			dbtype = json_dict['type']
			params = {
				'host':json_dict['wserver'],
				'port':json_dict['wport'],
				'dbname':json_dict['name'],
				'user':json_dict['username'],
				'passwd':json_dict['password']
			}

			# dir(request.websocket) # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_get_new_messages', '_message_queue', 'accept_connection', 'close', 'closed', 'count_messages', 'handle', 'has_messages', 'is_close', 'is_closed', 'protocol', 'read', 'send', 'wait']
			mydb = ""
			if dbtype == '0':
				mydb = MySql(**params)
				if isinstance(mydb.db, dict):
					message = "未能成功连接到数据库，报错信息：{}\n".format(mydb.db['detail']).encode('utf-8')
					# print(message.decode('utf-8'))
					ws.send(message)
					ws.send('bye')
					ws.wait()
				else:
					ws.send("已成功连接到数据库".encode('utf-8'))
					while True:
						ws.send("\n>")
						msg = ws.wait()
						if not msg:
							ws.close()
							return
						cmd = msg.decode()
						if cmd == "exit":
							break
						try:
							ws.send(mydb.exec(cmd))

						# mysql err
						except pymysql.err.InterfaceError as mysqlExitErr:
							break
						except pymysql.err.InternalError as mysqlInternalErr:
							ws.send(str(mysqlInternalErr))
							continue
						except pymysql.err.ProgrammingError as mysqlSyntaxErr:
							ws.send(str(mysqlSyntaxErr))
							continue
						except Exception as err:
						    ws.send(str(err))
					mydb.close()
					ws.send('bye')
					ws.wait()
		else:
			return Response({'error':1,'detail':'这是一个websocket接口'})
		