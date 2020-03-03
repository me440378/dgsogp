#扫描hadoop集群上的文件，入库
def scanMetadataPutInDB():
	pass
	# 判断hadoopsources的dbstate
	# 已完成
	# 	不用管
	# 未入库
	# 	判断对应datasource的hstate
	# 		未处理，处理中
	# 		已完成
	# 			入库
	# 				将dbstate改为已完成