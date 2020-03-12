from django.db import connection, connections

def getDBCursor():
	return connections['data_db'].cursor()

def checkTable(cursor, tablename):
	checkTableSQL = """SHOW TABLES LIKE \"{tablename}\"""".format(tablename=tablename)
				#判断表是否已存在
	if cursor.execute(checkTableSQL):
		return True
	else:
		return False

def createTable(cursor, tablename, feature):
	createTableSQL = """CREATE TABLE `{tablename}` (id INT  NOT NULL AUTO_INCREMENT,""".format(tablename=tablename)
	for i in range(feature):
		createTableSQL += """col{col} varchar(255),""".format(col=i+1)
	createTableSQL += """PRIMARY KEY (id))"""
	cursor.execute(createTableSQL)

def countTableRow(cursor, tablename):
	countTableSQL = """SELECT COUNT(1) FROM `{tablename}`""".format(tablename=tablename)
	cursor.execute(countTableSQL)
	return list(cursor.fetchone())[0]

def insertTable(cursor, tablename, feature, line):
	insertSQL="""INSERT INTO `{tablename}` (""".format(tablename=tablename)
	insertSQL+=",".join(["col{col}".format(col=i+1) for i in range(feature)])
	insertSQL+=""") VALUES ("""
	insertSQL+=','.join(["""\"{col}\"""".format(col=i) for i in line.split(',')])
	insertSQL+=""")"""
	cursor.execute(insertSQL)

def readTable(cursor, tablename):
	selectSQL="""SELECT * FROM `{tablename}`""".format(tablename=tablename)
	cursor.execute(selectSQL)
	keys = []
	for column in cursor.description:
		keys.append(column[0])
	key_number = len(keys)
	json_data = []
	for row in cursor.fetchall():
		item = dict()
		for q in range(key_number):
			item[keys[q]] = row[q]
		json_data.append(item)
	return json_data