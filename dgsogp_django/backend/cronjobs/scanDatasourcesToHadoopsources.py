#扫描数据源以及hadoop集群，生成Hadoop数据源
def scanDatasourcesToHadoopsources():
	#从数据库读取处理中以及已完成的Datasources信息
	pass
	# 判断datasources的hstate
	# 	已完成
	# 		不用管
	# 	未处理
	# 		记录datasource的target、putindb、id
	# 			是否需要入库
	# 				是
	# 					dbstate为未入库
	# 				否
	# 					dbstate为已完成
	# 			state为未标记
	# 	处理中
	# 		记录datasource的target、putindb、id
	# 			是否需要入库
	# 				是
	# 					dbstate为未入库
	# 				否
	# 					dbstate为已完成
	# 			state为未标记