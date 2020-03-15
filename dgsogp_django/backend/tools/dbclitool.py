import pymysql
from prettytable import PrettyTable


class DB:
    def __init__(self, host, port, dbname, user, passwd):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.passwd = passwd

        self.db = self.conn()

    def conn(self):
        pass
    
    def exec(self, sql):
        table = PrettyTable()
        self.cursor = self.db.cursor()
        rows = self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for result in results:
            table.add_row(result)
        if not table.get_string() == '++\n||\n++\n++':
            return str(table)

    def close(self):
        self.db.close()


class MySql(DB):

    def __init__(self, host, port, dbname, user, passwd):
        super().__init__(host, port, dbname, user, passwd)

    def conn(self):
        try:
            db = pymysql.connect(host=self.host, port=int(self.port), database=self.dbname, user=self.user, password=self.passwd, charset='utf8')
        except Exception as e:
            db = {'error':1, 'detail':str(e)}
        return db

