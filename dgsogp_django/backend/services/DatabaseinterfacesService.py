from backend.models import Databaseinterfaces
from backend.serializers import DatabaseinterfacesSerializer
from backend.tools import reply
from backend.tools import countReply

class DatabaseinterfacesService():
	
	def createOne(type, wserver, wport, name, datasource_id):
		try:
			databaseinterface = Databaseinterfaces.objects.using('admin_db').create(
				type = type,
				wserver = wserver,
				wport = wport,
				name = name,
				datasource_id = datasource_id,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def readAll():
		re = None
		try:
			re = Databaseinterfaces.objects.using('admin_db').all()
			result = DatabaseinterfacesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readByCondition(select, key):
		re = None
		kvdict = {select: key}
		try:
			re = Databaseinterfaces.objects.using('admin_db').filter(**kvdict)
			result = DatabaseinterfacesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readOne(id):
		re = None
		try:
			re = Databaseinterfaces.objects.using('admin_db').get(pk = id)
			result = DatabaseinterfacesSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def updateOne(id, kvdict):
		try:
			Databaseinterfaces.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Databaseinterfaces.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def countAll():
		re = None
		try:
			re = Databaseinterfaces.objects.using('admin_db').count()
		except Exception as e:
			return reply(1, str(e))
		return re
		