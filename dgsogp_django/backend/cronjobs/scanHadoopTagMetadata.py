from backend.services import DatasourcesService
from backend.services import HadoopsourcesService
from backend.services import MetadataService

#hash
from backend.tools import filemd5hash
#hdfs
from backend.tools import getHadoopClient
from backend.tools import getAllFilesInHadoopDir
#local
from backend.tools import makeSureLocalFile
from backend.tools import makeLocalPath
from backend.tools import LOCAL_BASE
#cronjobtool
from backend.tools import getMetadataFormat
from backend.tools import getMetadataState
from backend.tools import getMetadataAmount
from backend.tools import getMetadataFeature

#扫描hadoop集群上的文件，标记
def scanHadoopTagMetadata():
	HadoopsourcesList = HadoopsourcesService.readAll()
	for Hadoopsources in HadoopsourcesList:
		# 判断hadoopsources的state
		hstate = Hadoopsources['state']
		if (hstate == 0) or (hstate == 1):
			# 未处理、处理中
			# 记录hadoopsources的source，datasourceid
			hadoopsource_id = Hadoopsources['id']
			source = Hadoopsources['source']
			datasource_id = Hadoopsources['datasource_id']
			# datasource为文件还是目录
			Datasources = DatasourcesService.readOne(datasource_id)
			dstate = Datasources['state']
			putindb = Datasources['putindb']
			related = Datasources['related']
			type = Datasources['type']
			if type == 0:
				#文件
				local = LOCAL_BASE + source
				if makeSureLocalFile(local):
					pass
				else:
					makeLocalPath(local[:local.rindex('/')])
					HadoopClient = getHadoopClient()
					HadoopClient.download(source, local, overwrite=True)
				hashsum = filemd5hash(local)
				format = getMetadataFormat(local)
				mstate = getMetadataState(dstate, putindb)
				if related == 0:
					#关系型
					amount = getMetadataAmount(local)
					feature = getMetadataFeature(local, ',')
					metadata = {
						"source":source,
						"amount":amount,
						"feature":feature,
						"hashsum":hashsum,
						"hadoopsource_id":hadoopsource_id,
						"format":format,
						"state":mstate,
					}
					MetadataService.createOne(**metadata)
					#将状态为未处理的Datasources改为已完成
					if hstate == 0:
						HadoopsourcesService.finishOne(hadoopsource_id)
				elif related == 1:
					metadata = {
						"source":source,
						"hashsum":hashsum,
						"hadoopsource_id":hadoopsource_id,
						"format":format,
						"state":mstate,
					}
					MetadataService.createOne(**metadata)
					#将状态为未处理的Datasources改为已完成
					if hstate == 0:
						HadoopsourcesService.finishOne(hadoopsource_id)
			elif type == 1:
				#目录
				#扫描文件
				HadoopClient = getHadoopClient()
				hdfsList = getAllFilesInHadoopDir(HadoopClient, source)
				for hdfsfile in hdfsList:
					local = LOCAL_BASE + hdfsfile
					if makeSureLocalFile(local):
						pass
					else:
						makeLocalPath(local[:local.rindex('/')])
						HadoopClient.download(hdfsfile, local, overwrite=True)
					hashsum = filemd5hash(local)
					format = getMetadataFormat(local)
					mstate = getMetadataState(dstate, putindb)
					if related == 0:
						#关系型
						amount = getMetadataAmount(local)
						feature = getMetadataFeature(local, ',')
						metadata = {
							"source":hdfsfile,
							"amount":amount,
							"feature":feature,
							"hashsum":hashsum,
							"hadoopsource_id":hadoopsource_id,
							"format":format,
							"state":mstate,
						}
						MetadataService.createOne(**metadata)
						#将状态为未处理的Hadoopsources改为已完成
						if hstate == 0:
							HadoopsourcesService.finishOne(hadoopsource_id)
					elif related == 1:
						metadata = {
							"source":hdfsfile,
							"hashsum":hashsum,
							"hadoopsource_id":hadoopsource_id,
							"format":format,
							"state":mstate,
						}
						MetadataService.createOne(**metadata)
						#将状态为未处理的Hadoopsources改为已完成
						if hstate == 0:
							HadoopsourcesService.finishOne(hadoopsource_id)
		elif hstate == 2:
			# 已完成，不用管
			pass

