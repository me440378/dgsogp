from backend.services import DatasourcesService
from backend.services import HadoopsourcesService
from backend.services import MetadataService
from backend.services import DatainterfacesService

#hdfs
from backend.tools import getHadoopClient
from backend.tools import getAllFilesInHadoopDir
#local
from backend.tools import makeSureLocalFile
from backend.tools import makeLocalPath
from backend.tools import LOCAL_BASE
#db
from backend.tools import getDBCursor
from backend.tools import createTable
from backend.tools import checkTable
from backend.tools import countTableRow
from backend.tools import insertTable
#mongo
from backend.tools import getMongoDB
from backend.tools import checkCollection
from backend.tools import countCollection
from backend.tools import insertCollection
#cronjobtool
from backend.tools import getTableName
from backend.tools import getCollectionName

#扫描hadoop集群上的文件，入库
def scanMetadataPutInDB():
	MetadataList = MetadataService.readAll()
	for Metadata in MetadataList:
		mstate =  Metadata['state']
		if (mstate == 0) or (mstate == 1):
			#未处理
			metadata_id = Metadata['id']
			source = Metadata['source']
			#确认本地有该文件
			local = LOCAL_BASE + source
			if makeSureLocalFile(local):
				pass
			else:
				makeLocalPath(local[:local.rindex('/')])
				HadoopClient = getHadoopClient()
				HadoopClient.download(source, local, overwrite=True)
			#判断关系型
			hadoopsource_id = Metadata['hadoopsource_id']
			Hadoopsources = HadoopsourcesService.readOne(hadoopsource_id)
			datasource_id = Hadoopsources['datasource_id']
			Datasources = DatasourcesService.readOne(datasource_id)
			related = Datasources['related']
			if related == 0:
				#关系型
				#建表
				cursor = getDBCursor()
				tablename = getTableName(source)
				feature = Metadata['feature']
				#判断表是否已存在
				if checkTable(cursor, tablename):
					#已存在
					count = countTableRow(cursor, tablename)#表行数
					amount = Metadata['amount']#文件行数
					if count < amount:
						#有新增
						with open(local, 'r') as f:
							for _ in range(count):
								next(f)
							for line in f:
								if not line.strip():
									#空行
									pass
								else:
									insertTable(cursor, tablename, feature, line.strip())
							if mstate == 0:
								MetadataService.finishOne(metadata_id)
					else:
						#无新增
						if mstate == 0:
							MetadataService.finishOne(metadata_id)
				else:
					#不存在
					createTable(cursor, tablename, feature)
					#写入表
					with open(local, 'r') as f:
						for line in f:
							if not line.strip():
								#空行
								pass
							else:
								insertTable(cursor, tablename, feature, line.strip())
					datainterface = {
						'type':0,#关系型，一定是mysql
						'name':tablename,
						'metadata_id':metadata_id,
					}
					DatainterfacesService.createOne(**datainterface)
					if mstate == 0:
						MetadataService.finishOne(metadata_id)
			elif related == 1:
				#非关系型
				#建表
				mdatadb = getMongoDB()
				collectionname = getCollectionName(source)
				feature = Metadata['feature']
				#判断表是否已存在
				if checkCollection(mdatadb, collectionname):
					#已存在
					count = countCollection(mdatadb, collectionname)#表行数
					amount = Metadata['amount']#文件行数
					if count < amount:
						#有新增
						with open(local, 'r') as f:
							for _ in range(count):
								next(f)
							for line in f:
								if not line.strip():
									#空行
									pass
								else:
									insertCollection(mdatadb, collectionname, line.strip())
							if mstate == 0:
								MetadataService.finishOne(metadata_id)
					else:
						#无新增
						if mstate == 0:
							MetadataService.finishOne(metadata_id)
				else:
					#不存在
					#写入表
					with open(local,'r') as f:
						for line in f:
							if not line.strip():
								#空行
								pass
							else:
								insertCollection(mdatadb, collectionname,  line.strip())
					datainterface = {
						'type':1,#非关系型，一定是mongodb
						'name':collectionname,
						'metadata_id':metadata_id,
					}
					DatainterfacesService.createOne(**datainterface)
					if mstate == 0:
						MetadataService.finishOne(metadata_id)
		elif mstate == 2:
			#已完成
			pass

