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
        self.dbData = None
        completer = QtGui.QCompleter()
        self.emplyee_le.setCompleter(completer)
        model = QtGui.QStringListModel()
        completer.setModel(model)
        # model.setStringList(['durgesh', 'dinesh'])
        self.getArtistList(model)

        self.makeConnections()

    def makeConnections(self):
        self.project_cb.currentIndexChanged.connect(self.updateEpisode)
        self.episode_cb.currentIndexChanged.connect(self.updateDept)
        self.dept_cb.currentIndexChanged.connect(self.updateTable)
        self.assign_pb.clicked.connect(self.assignShots)

    def assignShots(self):
        project = self.project_cb.currentText()
        episode = self.episode_cb.currentText()
        dept = 'anim' if self.dept_cb.currentText() == 'Animation' else 'lay'
        artistName = self.emplyee_le.text()
        shotStatus = None
        errorMessage = dict()
        for e in self.tableWidget.selectedItems():
            shotName = e.text()
            # check in the fetched cached database for the shot entries for status, if it's not yet assigned then only
            # assign them else put them in the errorMessage.
            for eachLine in self.dbData:
                if shotName in eachLine:
                    if eachLine[4] not in ['NAY', None]:
                        errorMessage[shotName] = eachLine[3]
                        break
            else:
                with ConnectDB(project) as newdBcONN:
                    msg = 'UPDATE `{0}` SET `{1}_artist_name`="{2}",`{3}_status`="NYS" WHERE `shots` = "{4}"'.format(episode, dept,  artistName, dept, shotName)
                    print msg, '<--------------------------------------------------'
                    newdBcONN.execute(msg)
        #
        if errorMessage:
            for e in errorMessage.keys():
                print 'Shot {0} is already assigned to {1}'.format(e, errorMessage[e])

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

    def getArtistList(self, model):
        artistList = list()
        dept = 'ani' if self.dept_cb.currentText() == 'Animation' else 'lay'
        with ConnectDB('users') as dbConn:
            dbConn.execute('SELECT empname FROM `emp` WHERE `empdepts` LIKE "%{0}%" ORDER BY `empid` ASC'.format(dept))
            for eachArtist in dbConn.fetchall():
                artistList.append(eachArtist[0])
        print artistList, '<----------------------------------------------'
        model.setStringList(artistList)

    def updateDept(self):
        self.dept_cb.setCurrentIndex(0)

    def updateTable(self):
        print self.project_cb.currentText()
        self.populateArtists()
        dept = self.dept_cb.currentText()
        episode = self.episode_cb.currentText()
        if dept == 'Select':
            return False
        dept = 'anim' if dept == 'Animation' else 'lay'
        print dept, '<----------------------------------'
        dbQuerry = 'SELECT `shots`, `Start_Frame`, `End_Frame`, `%s_artist_name`, `%s_status`,  `Session_Status`, ' \
                   '`%s_startdate`, `%s_enddate`, `%s_publishdate` FROM `%s` ORDER BY `%s`.`shots` ASC' \
                   % (dept, dept, dept, dept, dept, episode, episode)
        dbData = None
        with ConnectDB(self.project_cb.currentText()) as dbCur:
            dbCur.execute(dbQuerry)

            self.dbData = dbCur.fetchall()

        headers = ['shots', 'Start_Frame', 'End_Frame', '%s_artist_name' % dept, '%s_status' % dept,
                   'Session_Status', '%s_startdate' % dept, '%s_enddate' % dept, '%s_publishdate' % dept]

        self.tableWidget.setRowCount(len(self.dbData))
        self.tableWidget.setColumnCount(len(self.dbData[0]))
        for i, each in enumerate(headers):
            itm = QtGui.QTableWidgetItem(each)
            self.tableWidget.setHorizontalHeaderItem(i, itm)

        for row, eachRow in enumerate(self.dbData):
            for col, eachCol in enumerate(eachRow):
                print eachCol, row, col
                itm = QtGui.QTableWidgetItem(eachCol)
                self.tableWidget.setItem(row, col, itm)

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
