import pymysql
import socket
import re
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


class Redis(DB):
    """Redis.
    """
    def __init__(self, host, port, dbname, user, passwd):
        super().__init__(host, port, dbname, user, passwd)

    def conn(self):
        try:
            sock = socket.socket()
            sock.connect((self.host, int(self.port)))
        except Exception as e:
            sock = {'error':1, 'detail':str(e)}
        return sock

    def exec(self, sql):
        if sql=='':
            return
        sql = self.makeCmd(sql)
        try:
            self.db.send(sql.encode())
            result = ''
            while True:
                recv = self.db.recv(1024)
                result += self.handleRecv(recv)
                if len(recv)<1024:  # 循环接收1024, 如果长度小于1024则默认后面已经无内容,break
                    break
            return result
        except Exception as err:
            return(err)

    @staticmethod
    def makeCmd(cmd):
        command = "*"
        cmd = cmd.split()
        command = command + str(len(cmd)) + '\r\n'
        for c in cmd:
            command = command + '$' + str(len(c)) + '\r\n' + c + '\r\n'
        return command

    @staticmethod
    def handleRecv(recvdate):
        recvdate = recvdate.decode()
        if recvdate.startswith('*'):
            recvdate=recvdate[2:].strip('\r\n')
        recvdate = re.sub('\$\d+\\r\\n', '', recvdate)
        return recvdate