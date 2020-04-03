from backend.services import DatasourcesService
from backend.services import HadoopsourcesService
from backend.services import DatabaseinterfacesService

#sftp
from backend.tools import getSftpClient
from backend.tools import getAllFilesInRemoteDir
#hdfs
from backend.tools import getHadoopClient
from backend.tools import makeHdfsPath
#local
from backend.tools import deleteFileOrDir
from backend.tools import makeLocalPath
from backend.tools import LOCAL_BASE

#从工作服务器采集到hadoop集群
def collectDataFromServers():
	DatasourcesList = DatasourcesService.readAll()
	for Datasources in DatasourcesList:
		# 判断状态是什么
		state = Datasources['state']#0 未处理、1 处理中、2 已完成
		if (state == 0) or (state == 1):
			# 未处理、处理中
			datasource_id = Datasources['id']
			wgroup = Datasources['wgroup']
			wserver = Datasources['wserver']
			localGaS = ''.join([LOCAL_BASE, '/', wgroup, '/', wserver])#./tmp/group/server
			hadoopGaS = ''.join(['/', wgroup, '/', wserver])#/group/server
			source = Datasources['source']
			target = Datasources['target']
			#获取sftp客户端
			SftpClint = getSftpClient(wserver)
			#获取Hadoop客户端
			HadoopClient = getHadoopClient()
			# 判断是否为文件、目录
			type = Datasources['type']#0 文件、1 目录、2 数据库
			if type == 0:
				# 文件
				# 将文件写入本地
				remote = source
				local = localGaS + target
				makeLocalPath(local[:local.rindex('/')])
				try:
					SftpClint.get(remote, local)#下载
					SftpClint.close()
				except Exception as e:
					SftpClint.close()
					print(str(e))
					DatasourcesService.exceptOne(datasource_id)
					continue
				# 从本地上传到hadoop
				hpath = hadoopGaS + target#/dev/server/iris.data
				makeHdfsPath(HadoopClient, hpath[:hpath.rindex('/')])#/dev/server
				HadoopClient.upload(hpath, local, overwrite=True)
				#完成远程到本地到Hadoop集群的流程了
				#之后要生成HadoopSource
				#查找datasource_id对应的hadoopsource是否存在
				hadoopsource = HadoopsourcesService.readByCondition('datasource_id',datasource_id)
				if hadoopsource:
					#存在
					pass
				else:
					#不存在
					hadoopsource = {
						"state":state,
						"source":hadoopGaS + target,
						"datasource_id":datasource_id,
					}
					HadoopsourcesService.createOne(**hadoopsource)
				#将状态为未处理的Datasources改为已完成
				if state == 0:
					DatasourcesService.finishOne(datasource_id)
			elif type == 1:
				# 目录
				localRootDir = localGaS + target#./tmp/ops/server/python
				remoteDir = source
				# 将目录所有文件递归列出列表
				remoteList = []
				try:
					remoteList = getAllFilesInRemoteDir(SftpClint, remoteDir)
				except Exception as e:
					SftpClint.close()
					print(str(e))
					DatasourcesService.exceptOne(datasource_id)
					continue
				# 将列表中的全部文件写入本地
				for remote in remoteList:
					local = localRootDir + remote[len(remoteDir):]
					makeLocalPath(local[:local.rindex('/')])
					SftpClint.get(remote, local)#下载
					# 将本地文件上传到hadoop
					hpath = hadoopGaS + target + remote[len(remoteDir):]
					makeHdfsPath(HadoopClient, hpath[:hpath.rindex('/')])
					HadoopClient.upload(hpath, local, overwrite=True)
				SftpClint.close()
				#完成远程到本地到Hadoop集群的流程了
				#之后要生成HadoopSource
				#查找datasource_id对应的hadoopsource是否存在
				hadoopsource = HadoopsourcesService.readByCondition('datasource_id',datasource_id)
				if hadoopsource:
					#存在
					pass
				else:
					#不存在
					hadoopsource = {
						"state":state,
						"source":hadoopGaS + target,
						"datasource_id":datasource_id,
					}
					HadoopsourcesService.createOne(**hadoopsource)
					#将状态为未处理的Datasources改为已完成
				if state == 0:
					DatasourcesService.finishOne(datasource_id)
			elif type == 2:
				# 数据库，生成 Databaseinterface
				# source格式： type:wport/name
				# wserver、datasource_id 从 Datasource 获取
				databaseinterface = {
					'type':0 if source[: source.index(':')]=='mysql' else 1 if source[: source.index(':')]=='mongodb' else 2,
					'wserver':wserver,
					'wport':source[source.index(':')+1 : source.index('/')],
					'name':source[source.index('/')+1 :],
					'datasource_id':datasource_id,
				}
				DatabaseinterfacesService.createOne(**databaseinterface)
				DatasourcesService.finishOne(datasource_id)
		elif state == 2:
			# 已完成，不用管
			pass

