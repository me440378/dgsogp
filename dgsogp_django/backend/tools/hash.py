import hashlib

def md5hash(message):
	m = hashlib.md5(message.encode(encoding='UTF-8'))
	return m.hexdigest()