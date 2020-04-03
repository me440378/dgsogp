from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.models import Datainterfaces
from backend.serializers import DatainterfacesSerializer
from backend.tools import reply, dtReply
from backend.tools import getDBCursor
from backend.tools import readTable
from backend.tools import getMongoDB
from backend.tools import readCollection

class DatainterfacesService():
	
	def createOne(type, name, metadata_id):
		try:
			datainterface = Datainterfaces.objects.using('admin_db').create(
				type = type,
				name = name,
				metadata_id = metadata_id,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)
	
	def readAll():
		try:
			re = Datainterfaces.objects.using('admin_db').all()
			result = DatainterfacesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readPage(pageIndex, pageSize):
		try:
			re = Datainterfaces.objects.using('admin_db').all()
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = DatainterfacesSerializer(page, many = True)
		total = Datainterfaces.objects.using('admin_db').count()
		return dtReply(result.data, total)

	def readPageByCondition(pageIndex, pageSize, select, key):
		try:
			kvdict = {select: key}
			re = Datainterfaces.objects.using('admin_db').filter(**kvdict)
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = DatainterfacesSerializer(page, many = True)
		total = re.count()
		return dtReply(result.data, total)

	def readOne(id):
		re = None
		try:
			re = Datainterfaces.objects.using('admin_db').get(pk = id)
			result = DatainterfacesSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def updateOne(id, kvdict):
		try:
			Datainterfaces.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Datainterfaces.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def countAll():
		re = None
		try:
			re = Datainterfaces.objects.using('admin_db').count()
		except Exception as e:
			return reply(1, str(e))
		return re
		
	def readData(id):
		json_data = None
		try:
			re = Datainterfaces.objects.using('admin_db').get(pk = id)
			type = re.type
			if type == 0:
				#mysql
				tablename = re.name
				cursor = getDBCursor()
				json_data = readTable(cursor, tablename)
			elif type == 1:
				#mongodb
				collectionname = re.name
				db = getMongoDB()
				json_data = readCollection(db, collectionname)
		except Exception as e:
			return reply(1, str(e))
		return json_data