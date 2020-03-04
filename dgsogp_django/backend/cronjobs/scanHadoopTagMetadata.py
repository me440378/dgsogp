import os
from hdfs import InsecureClient

from backend.services import DatasourcesService
from backend.services import HadoopsourcesService
from backend.services import MetadataService
from backend.tools import filemd5hash
from backend.tools import get_all_files_in_hadoop_dir
from backend.tools import makeSureLocalFile

#扫描hadoop集群上的文件，标记
def scanHadoopTagMetadata():
	HadoopsourcesList = HadoopsourcesService.readAll()
	for Hadoopsources in HadoopsourcesList:
		# 判断hadoopsources的state
		hadoopsource_id = Hadoopsources['id']
		hstate = Hadoopsources['state']
		if (hstate == 0) or (hstate == 1):
			#未处理、处理中
			# 记录hadoopsources的source，datasourceid
			source = Hadoopsources['source']
			datasource_id = Hadoopsources['datasource_id']
			# datasource为文件还是目录
			Datasources = DatasourcesService.readOne(datasource_id)
			dstate = Datasources['state']
			putindb = Datasources['putindb']
			related = Datasources['related']
			type = Datasources['type']
			localBase = r'./tmp'
			if type == 0:
				#文件
				local = localBase + source
				client = InsecureClient('http://hadoop-server-test:50070', user='hadoop', root='/')
				if makeSureLocalFile(local):
					pass
				else:
					client.download(source, local)
				if related == 0:
					#关系型
					amount = getMetadataAmount(local)
					feature = getMetadataFeature(local, ',')
					hashsum = filemd5hash(local)
					format = getMetadataFormat(local)
					mstate = getMetadataState(dstate, putindb)
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
						kvdict = {"state":2}
						HadoopsourcesService.updateOne(hadoopsource_id, kvdict)
				elif related == 1:
					hashsum = filemd5hash(local)
					format = getMetadataFormat(local)
					mstate = getMetadataState(dstate, putindb)
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
						kvdict = {"state":2}
						HadoopsourcesService.updateOne(hadoopsource_id, kvdict)
			elif type == 1:
				#目录
				#扫描文件
				client = InsecureClient('http://hadoop-server-test:50070', user='hadoop', root='/')
				hdfsList = get_all_files_in_hadoop_dir(client, source)
				for hdfsfile in hdfsList:
					local = localBase + hdfsfile
					if makeSureLocalFile(local):
						pass
					else:
						client.download(hdfsfile, local)
					if related == 0:
						#关系型
						amount = getMetadataAmount(local)
						feature = getMetadataFeature(local, ',')
						hashsum = filemd5hash(local)
						format = getMetadataFormat(local)
						mstate = getMetadataState(dstate, putindb)
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
						#将状态为未处理的Datasources改为已完成
						if hstate == 0:
							kvdict = {"state":2}
							HadoopsourcesService.updateOne(hadoopsource_id, kvdict)
					elif related == 1:
						hashsum = filemd5hash(local)
						format = getMetadataFormat(local)
						mstate = getMetadataState(dstate, putindb)
						metadata = {
							"source":hdfsfile,
							"hashsum":hashsum,
							"hadoopsource_id":hadoopsource_id,
							"format":format,
							"state":mstate,
						}
						MetadataService.createOne(**metadata)
						#将状态为未处理的Datasources改为已完成
						if hstate == 0:
							kvdict = {"state":2}
							HadoopsourcesService.updateOne(hadoopsource_id, kvdict)
		elif hstate == 2:
			#已完成，不用管
			pass


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
