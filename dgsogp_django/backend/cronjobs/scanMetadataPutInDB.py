from hdfs import InsecureClient

from django.db import connection, connections

from backend.services import DatasourecesService
from backend.services import HadoopsourcesService
from backend.services import MetadataService
#扫描hadoop集群上的文件，入库
def scanMetadataPutInDB():
	MetadataList = MetadataService.readAll()
	for Metadata in MetadataList:
		mstate =  Metadata['state']
		if mstate == 0:
			#未处理
			hadoopsource_id = Metadata['hadoopsource_id']
			Hadoopsources = HadoopsourcesService.readOne(hadoopsource_id)
			datasourece_id = Hadoopsources['datasourece_id']
			Datasoureces = DatasourecesService.readOne(datasourece_id)
			related = Datasoureces['related']
			source = Metadata['source']
			#确认本地有该文件
			localBase = r'./tmp'
			local = localBase + source
			client = InsecureClient('http://hadoop-server-test:50070', user='hadoop', root='/')
			if makeSureLocalFile(local):
				pass
			else:
				client.download(source, local)
			#判断关系型
			if related == 0:
				#关系型
				#建表
				tablename = getTableName(source)
				feature = Metadata['feature']
				cursor = connections['data_db'].cursor()
				createTableSQL = """CREATE TABLE `{tablename}` (id INT  NOT NULL AUTO_INCREMENT,""".format(tablename=tablename)
				for i in range(feature):
					createTableSQL += """col{col} varchar(255),""".format(col=i+1)
				createTableSQL += """PRIMARY KEY (id))"""
				cursor.execute(createTableSQL)
				#写入表
				with open(local,'r') as f:
					for line in f.readlines():  
     					insertSQL="""INSERT INTO `{tablename}` (""".format(tablename=tablename)
     					insertSQL+=",".join(["col{col}".format(col=i+1) for i in range(feature)])
     					insertSQL+=""") VALUES ("""
     					insertSQL+=','.join(["""\"{col}\"""".format(col=i) for i in line.split(',')])
     					insertSQL+=""")"""
     					cursor.execute(insertSQL)
			elif related == 1:
				#非关系型
				#建表
				#写入库表
				pass
		elif mstate == 1:
			#处理中
			pass
		elif mstate == 2:
			#已完成
			pass
	# 未入库
	# 	判断对应datasource的hstate
	# 		未处理，处理中
	# 		已完成
	# 			入库
	# 				将dbstate改为已完成


def getTableName(source):
	return source.replace('/', '.')