
def getMetadataAmount(File):
	count = 0
	with open(File, 'r') as f:
		for index, line in enumerate(f):
			if not line.strip():
				#空行
				pass
			else:
				count += 1
	return(count)

def getMetadataFeature(File, Sep):
	with open(File, 'r') as f:
		line = f.readline()
		return len(line.split(Sep))

def getMetadataFormat(File):
	filename = File.split('/')[-1]
	if not filename.find('.') == -1:
		#有后缀
		return filename.split('.')[-1]
	else:
		#无后缀
		return 'unknown'

def getMetadataState(dstate, putindb):
	if putindb == 1:
		return 2
	if  dstate == 1:
		return 1
	else :
		return 0

def getTableName(source):
	return source.replace('/', '.')[1:]

def getCollectionName(source):
	return source.replace('/', '.')[1:]