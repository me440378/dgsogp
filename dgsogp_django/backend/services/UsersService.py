from backend.models import Users
from backend.serializers import UsersSerializer
from backend.tools import reply
from backend.tools import md5hash

class UsersService():
	
	def register(username, password, nickname):
		re = None
		try:
			re = Users.objects.using('admin_db').filter(username = username)
		except Exception as e:
			return reply(1, str(e))

		if re:
			return reply(1, '该用户名已存在')
		else:
			try:
				user = Users.objects.using('admin_db').create(
					username = username,
					nickname = nickname,
					password = md5hash(password),
				)
			except Exception as e:
				return reply(1, str(e))
		return reply(0)

	def readAll():
		re = None
		try:
			re = Users.objects.using('admin_db').all()
			result = UsersSerializer(re, many = True)
		except Exception as e:
			return reply(1, str(e))
		return result.data
		
	def readOne(id):
		re = None
		try:
			re = Users.objects.using('admin_db').get(pk = id)
			result = UsersSerializer(re)
		except Exception as e:
			return reply(1, str(e))
		return result.data
	
	def updateOne(id, kvdict):
		try:
			Users.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def deleteOne(id):
		try:
			Users.objects.using('admin_db').filter(pk = id).delete()
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def updatePassword(id, oldpassword, newpassword):
		re = None
		try:
			re = Users.objects.using('admin_db').get(pk = id)
		except Exception as e:
			return reply(1, str(e))
		password = re.password
		if not password == md5hash(oldpassword):
			return reply(1, '旧密码错误')
		kvdict = {"password": md5hash(newpassword)}
		try:
			Users.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def updateForcePassword(id, newpassword):
		kvdict = {"password": md5hash(newpassword)}
		try:
			Users.objects.using('admin_db').filter(pk = id).update(**kvdict)
		except Exception as e:
			return reply(1, str(e))
		return reply(0)

	def login(username, password):
		re = None
		try:
			re = Users.objects.using('admin_db').get(username = username)
		except Exception as e:
			return reply(1, '该用户不存在或数据库繁忙中')

		userid = re.id
		dbpassword = re.password
		if not dbpassword == md5hash(password):
			return reply(1, '密码不正确')
		else:
			return {"error": 0, "userid": userid}
