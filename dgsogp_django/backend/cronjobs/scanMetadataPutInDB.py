from hdfs import InsecureClient

from django.db import connection, connections

from backend.services import DatasourcesService
from backend.services import HadoopsourcesService
from backend.services import MetadataService
from backend.tools import makeSureLocalFile

#扫描hadoop集群上的文件，入库
def scanMetadataPutInDB():
	MetadataList = MetadataService.readAll()
	for Metadata in MetadataList:
		mstate =  Metadata['state']
		if (mstate == 0) or (mstate == 1):
			#未处理
			metadata_id = Metadata['id']
			hadoopsource_id = Metadata['hadoopsource_id']
			Hadoopsources = HadoopsourcesService.readOne(hadoopsource_id)
			datasource_id = Hadoopsources['datasource_id']
			Datasources = DatasourcesService.readOne(datasource_id)
			related = Datasources['related']
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
				cursor = connections['data_db'].cursor()
				tablename = getTableName(source)
				feature = Metadata['feature']
				checkTableSQL = """SHOW TABLES LIKE \"{tablename}\"""".format(tablename=tablename)
				#判断表是否已存在
				if cursor.execute(checkTableSQL):
					#已存在
					countTableSQL = """SELECT COUNT(1) FROM `{tablename}`""".format(tablename=tablename)
					cursor.execute(countTableSQL)
					count = list(cursor.fetchone())[0]
					amount = Metadata['amount']
					if count < amount:
						#有新增
						with open(local, 'r') as f:
							for _ in range(count):
								_ = next(f)
							for line in f:
								if not line.strip():
									#空行
									pass
								else:
									insertSQL="""INSERT INTO `{tablename}` (""".format(tablename=tablename)
									insertSQL+=",".join(["col{col}".format(col=i+1) for i in range(feature)])
									insertSQL+=""") VALUES ("""
									insertSQL+=','.join(["""\"{col}\"""".format(col=i) for i in line.split(',')])
									insertSQL+=""")"""
									cursor.execute(insertSQL)
							if mstate == 0:
								kvdict = {"state":2}
								MetadataService.updateOne(metadata_id, kvdict)
					else:
						#无新增
						if mstate == 0:
							kvdict = {"state":2}
							MetadataService.updateOne(metadata_id, kvdict)
				else:
					#不存在
					createTableSQL = """CREATE TABLE `{tablename}` (id INT  NOT NULL AUTO_INCREMENT,""".format(tablename=tablename)
					for i in range(feature):
						createTableSQL += """col{col} varchar(255),""".format(col=i+1)
					createTableSQL += """PRIMARY KEY (id))"""
					cursor.execute(createTableSQL)
					#写入表
					with open(local,'r') as f:
						for line in f:
							if not line.strip():
								#空行
								pass
							else:
								insertSQL="""INSERT INTO `{tablename}` (""".format(tablename=tablename)
								insertSQL+=",".join(["col{col}".format(col=i+1) for i in range(feature)])
								insertSQL+=""") VALUES ("""
								insertSQL+=','.join(["""\"{col}\"""".format(col=i) for i in line.split(',')])
								insertSQL+=""")"""
								cursor.execute(insertSQL)
					if mstate == 0:
						kvdict = {"state":2}
						MetadataService.updateOne(metadata_id, kvdict)
			elif related == 1:
				#非关系型
				#建表
				#写入库表
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
	return source.replace('/', '.')[1:]