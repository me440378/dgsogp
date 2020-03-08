from backend.models import Metadata
from backend.serializers import MetadataSerializer
from backend.tools import reply

class MetadataService():

	def createOne(source, hashsum, hadoopsource_id, format, state, amount = None, feature = None):
		try:
			metadata = Metadata.objects.using('admin_db').create(
				source = source,
				amount = amount,
				feature = feature,
				hashsum = hashsum,
				hadoopsource_id = hadoopsource_id,
				format = format,
				state = state,
			)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def readAll():
		re = None
		try:
			re = Metadata.objects.using('admin_db').all()
			result = MetadataSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def readOne(id):
		re = None
		try:
			re = Metadata.objects.using('admin_db').get(pk = id)
			result = MetadataSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data

	def updateOne(id, kvdict):
		try:
			Metadata.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Metadata.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def finishOne(id):
		kvdict = {"state":2}
		try:
			Metadata.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def countAll():
		re = None
		try:
			re = Metadata.objects.using('admin_db').count()
		except Exception as e:
			return reply(1, str(e))
		return re
