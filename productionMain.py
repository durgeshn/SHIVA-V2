import sys

from PySide import QtGui

from ui import production
from utils.dbHelper import ConnectDB


class ProductionWin(QtGui.QMainWindow, production.Ui_Form):
    def __init__(self):
        super(ProductionWin, self).__init__()
        self.setupUi(self)
        self.project_cb.addItems(['Select', 'badgers_and_foxes'])
        self.dept_cb.addItems(['Select', 'Layout', 'Animation'])
        self.makeConnections()

    def makeConnections(self):
        self.project_cb.currentIndexChanged.connect(self.updateEpisode)
        self.episode_cb.currentIndexChanged.connect(self.updateDept)
        self.dept_cb.currentIndexChanged.connect(self.updateTable)

    def updateEpisode(self):
        projectName = self.project_cb.currentText()
        self.episode_cb.clear()
        if projectName == 'Select':
            return False
        self.episode_cb.addItem('Select')
        with ConnectDB(project=projectName) as dbCur:
            dbCur.execute('SHOW TABLES')
            for eachEpisode in dbCur:
                self.episode_cb.addItem(eachEpisode[0])

    def updateDept(self):
        self.dept_cb.setCurrentIndex(0)

    def updateTable(self):
        print self.project_cb.currentText()
        self.populateArtists()
        dept = self.dept_cb.currentText()
        if dept == 'Select':
            return False
        dept = 'anim' if dept == 'Animation' else 'lay'
        print dept, '<----------------------------------'
        dbQuerry = 'SELECT `shots`, `%s_artist_name`, `%s_status`, `Start_Frame`, `End_Frame`, `Session_Status`, ' \
                   '`%s_startdate`, `%s_enddate`, `%s_publishdate` FROM `bdg100` ORDER BY `bdg100`.`shots` ASC' \
                   % (dept, dept, dept, dept, dept)
        with ConnectDB(self.project_cb.currentText()) as dbCur:
            dbCur.execute(dbQuerry)

            print dbCur.fetchall()


    def populateArtists(self):
        dept = self.dept_cb.currentText()
        dept = 'ani' if dept == 'Animation' else 'lay'
        artistList = list()
        with ConnectDB('users') as dbCur:
            dbCur.execute('SELECT `empname` FROM `emp` WHERE `empdepts` LIKE "%{0}%" ORDER BY `empid` ASC'.format(dept))
            for eachArtist in dbCur.fetchall():
                artistList.append(eachArtist[0])


if __name__ == '__main__':
    qApp = QtGui.QApplication(sys.argv)
    win = ProductionWin()
    win.show()
    qApp.exec_()
