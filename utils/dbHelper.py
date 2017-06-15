import pymysql

# import the config file
from config import config


class ConnectDB(object):
    def __init__(self, project):
        self.project = project
        self.host = config.hostId
        self.user = config.userName
        self.password = config.password

    def __enter__(self):
        self.conn = pymysql.connect(host=self.host, db=self.project, user=self.user, passwd=self.password)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    with ConnectDB('badgers_and_foxes') as tt:
        tt.execute("SHOW TABLES")
    print tt.fetchall()
