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
            print(table)

    def close(self):
        self.db.close()


class MySql(DB):

    def __init__(self, host, port, user, passwd, dbname):
        super().__init__(host, port, user, passwd, dbname)

    def conn(self):
        db = pymysql.connect(host=self.host, port=int(self.port), database=self.dbname, user=self.user, password=self.passwd, charset='utf8')
        return db


def cli(dbtype, host, port, dbname, user, pwd):

    mydb = ""
    if dbtype == 'mysql':
        mydb = MySql(host, port, dbname, user, pwd)

    # elif dbtype == 'redis':
    #     mydb = Redis(args.host, args.port, args.user, args.pwd)
    #     if args.pwd:
    #         mydb.exec("auth "+args.pwd)

    while True:
        cmd = input(">")
        if cmd == "exit":
            break

        try:
            mydb.exec(cmd)

        # mysql err
        except pymysql.err.InterfaceError as mysqlExitErr:
            break
        except pymysql.err.InternalError as mysqlInternalErr:
            print(mysqlInternalErr)
            continue
        except pymysql.err.ProgrammingError as mysqlSyntaxErr:
            print(mysqlSyntaxErr)
            continue
        except Exception as err:
            print(err)
    
    mydb.close()
    print('\n\tByeBye ~~\n')


if __name__ == "__main__":    
    cli('mysql','hadoop-server-test','3306','xxx_db','root','123456')