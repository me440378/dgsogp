from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.models import Databaseinterfaces
from backend.serializers import DatabaseinterfacesSerializer
from backend.tools import reply, dtReply

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

	def readAll(pageIndex, pageSize):
		try:
			re = Databaseinterfaces.objects.using('admin_db').all()
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = DatabaseinterfacesSerializer(page, many = True)
		total = Databaseinterfaces.objects.using('admin_db').count()
		return dtReply(result.data, total)

	def readByCondition(pageIndex, pageSize, select, key):
		try:
			kvdict = {select: key}
			re = Databaseinterfaces.objects.using('admin_db').filter(**kvdict)
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = DatabaseinterfacesSerializer(page, many = True)
		total = re.count()
		return dtReply(result.data, total)

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
		