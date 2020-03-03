import hashlib

def md5hash(message):
	m = hashlib.md5(message.encode(encoding='UTF-8'))
	return m.hexdigest()

def filemd5hash(filename):
	# 对文件做hash算法
	# 用sha256方法计算
	m = hashlib.md5()
	# 将文件按照4096k大小读出，
	with open(filename, "rb") as f:
		content = f.read(4096)
		m.update(content)
	# 返回值就是hash文件后的值
	return m.hexdigest()