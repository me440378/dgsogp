from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.models import Datasources
from backend.serializers import DatasourcesSerializer
from backend.tools import reply, dtReply, countReply

class DatasourcesService():
	
	def createOne(wgroup, wserver, type, source, related, putindb = None, pattern = None, target = None, content = None):
		try:
			state = 0
			if pattern == "1":
				state = 1
			datasource = Datasources.objects.using('admin_db').create(
				wgroup = wgroup,
				wserver = wserver,
				type = type,
				source = source,
				putindb = putindb,
				related = related,
				pattern = pattern,
				target = target,
				state = state,
				content = content,
				excepted = 0,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def readAll():
		try:
			re = Datasources.objects.using('admin_db').all()
			result = DatasourcesSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readPage(pageIndex, pageSize):
		try:
			re = Datasources.objects.using('admin_db').all()
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = DatasourcesSerializer(page, many = True)
		total = Datasources.objects.using('admin_db').count()
		return dtReply(result.data, total)

	def readByCondition(pageIndex, pageSize, select, key):
		try:
			kvdict = {select: key}
			re = Datasources.objects.using('admin_db').filter(**kvdict)
			paginator = Paginator(re, pageSize)
			page = paginator.page(pageIndex)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_page)
		except Exception as e:
			return reply(1, str(e))
		result = DatasourcesSerializer(page, many = True)
		total = re.count()
		return dtReply(result.data, total)

	def readOne(id):
		re = None
		try:
			re = Datasources.objects.using('admin_db').get(pk = id)
			result = DatasourcesSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def updateOne(id, kvdict):
		try:
			Datasources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Datasources.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def prefinishOne(id):
		kvdict = {"state":0}
		try:
			Datasources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def finishOne(id):
		kvdict = {"state":2}
		try:
			Datasources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def exceptOne(id):
		kvdict = {"excepted":1}
		try:
			Datasources.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def countAll():
		re = None
		try:
			re = Datasources.objects.using('admin_db').count()
		except Exception as e:
			return reply(1, str(e))
		return re
		