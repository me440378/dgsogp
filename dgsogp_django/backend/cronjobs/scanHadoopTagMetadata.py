#扫描hadoop集群上的文件，标记
def scanHadoopTagMetadata():
	pass
	# 判断hadoopsources的state
	# 已标记
	# 	不用管
	# 未标记
	# 	记录hadoopsources的source，datasourceid
	# 		datasource为文件还是目录
	# 			文件
	# 				是否关系型数据
	# 					是
	# 						记录amount、feature
	# 					否
	# 			目录
	# 				扫描目录，新建source列表
	# 					是否关系型数据
	# 						是
	# 							记录amount、feature
	# 						否