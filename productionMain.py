import sys
import datetime
import commentMain

from PySide import QtGui

from ui import production
from utils.dbHelper import ConnectDB
from utils import mailing
from utils.switch import Switch, case
reload(production)

reload(commentMain)


class ProductionWin(QtGui.QMainWindow, production.Ui_MainWindow):
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
        self.getArtistList(model)
        self.comment = None
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setSortingEnabled(True)

        # variable for the adding artists.
        self.allArtists = list()

        # variables for the mailing system.
        self.comment_dict = dict()
        self.sender = ''
        self.receivers = list()

        self.makeConnections()

    def makeConnections(self):
        self.project_cb.currentIndexChanged.connect(self.updateEpisode)
        self.episode_cb.currentIndexChanged.connect(self.updateDept)
        self.dept_cb.currentIndexChanged.connect(self.updateTable)
        self.assign_pb.clicked.connect(self.assignShots)
        self.reassign_pb.clicked.connect(self.reassignShots)
        self.approve_pb.clicked.connect(self.approoveShot)
        # self.retake_pb.clicked.connect(self.makeShotsNew)
        # self.retake_pb.clicked.connect(self.SFAShot)
        self.retake_pb.clicked.connect(self.retakeShots)

    def refreshTable(self):
        self.updateTable()

    def getSelectedRows(self):
        rows = list()
        for each in self.tableWidget.selectedIndexes():
            if each.row() not in rows:
                rows.append(each.row())
        return rows

    def retakeShots(self):
        self.comment_dict = dict()
        project = self.project_cb.currentText()
        episode = self.episode_cb.currentText()
        dept = 'anim' if self.dept_cb.currentText() == 'Animation' else 'lay'

        errorMessage = list()
        commentError = list()
        for eachRow in self.getSelectedRows():
            shotName = self.tableWidget.item(eachRow, 0).text()
            for eachLine in self.dbData:
                if shotName not in eachLine:
                    continue
                if eachLine[4] != 'SFA':
                    errorMessage.append(shotName)
                    break
            else:
                commentBox = commentMain.CommentMain(commentFor=shotName, prnt=self)
                commentBox.exec_()
                if self.comment is None or self.comment == '':
                    commentError.append(shotName)
                    continue
                now = datetime.datetime.now()
                finalComment = '{0}:{1}~'.format(now.strftime('%m-%d-%Y %H:%M'), self.comment)
                self.comment_dict[shotName] = self.comment
                with ConnectDB(project) as newdBcONN:
                    msg = 'UPDATE `{0}` SET `{1}_status`="TWIP", `{2}_comments`="{3}" WHERE `shots` = "{4}"'.format(
                        episode, dept, dept, finalComment, shotName)
                    newdBcONN.execute(msg)

        self.refreshTable()

        if errorMessage:
            msgBody = 'There is a problem while approoving the shot(s)'
            detail = ''
            for e in errorMessage:
                detail += 'Shot {0} is not in SFA stage..\n'.format(e)

            detail += 'Can\'t add retake to a shot which is not in SFA stage'
            self.showMessageBox(msgBody=msgBody, msgDetail=detail, header='Error', msgType='error')

    def makeShotsNew(self):
        project = self.project_cb.currentText()
        episode = self.episode_cb.currentText()
        dept = 'anim' if self.dept_cb.currentText() == 'Animation' else 'lay'

        for eachRow in self.getSelectedRows():
            shotName = self.tableWidget.item(eachRow, 0).text()
            print 'Wiping the database for {}'.format(shotName)
            with ConnectDB(project) as newDBConn:
                msg = 'UPDATE `{0}` SET `{1}_status`=NULL, `{2}_artist_name`=NULL, `{3}_comments`=NULL WHERE `shots`' \
                      ' = "{4}"'.format(episode, dept, dept, dept, shotName)
                # print msg
                newDBConn.execute(msg)
        self.refreshTable()

    def SFAShot(self):
        project = self.project_cb.currentText()
        episode = self.episode_cb.currentText()
        dept = 'anim' if self.dept_cb.currentText() == 'Animation' else 'lay'
        # errorMessage = dict()
        # colCount = self.tableWidget.columnCount()

        # get the selected rows.
        rows = list()
        for e in self.tableWidget.selectedIndexes():
            if e.row() not in rows:
                rows.append(e.row())

        for eachRow in rows:
            shotName = self.tableWidget.item(eachRow, 0).text()
            # print shotName, '<----------------------------'
            with ConnectDB(project) as newDBConn:
                msg = 'UPDATE `{0}` SET `{1}_status`="SFA" WHERE `shots` = "{2}"'.format(episode, dept, shotName)
                newDBConn.execute(msg)
        self.refreshTable()

    def approoveShot(self):
        project = self.project_cb.currentText()
        episode = self.episode_cb.currentText()
        dept = 'anim' if self.dept_cb.currentText() == 'Animation' else 'lay'

        errorMessage = list()

        for eachRow in self.getSelectedRows():
            shotName = self.tableWidget.item(eachRow, 0).text()
            print [shotName], '<----------------------'
            for eachLine in self.dbData:
                if shotName not in eachLine:
                    continue
                if eachLine[4] != 'SFA':
                    errorMessage.append(shotName)
                    break
            else:
                with ConnectDB(project) as newdBcONN:
                    msg = 'UPDATE `{0}` SET `{1}_status`="APP" WHERE `shots` = "{2}"'.format(episode, dept, shotName)
                    newdBcONN.execute(msg)

            self.refreshTable()

            if errorMessage:
                msgBody = 'There is a problem while approoving the shot(s)'
                detail = ''
                for e in errorMessage:
                    detail += 'Shot {0} is not in SFA stage..\n'.format(e)

                detail += 'Can\'t approove a shot which is not in SFA stage'
                self.showMessageBox(msgBody=msgBody, msgDetail=detail, header='Error', msgType='error')

    def assignShots(self):
        project = self.project_cb.currentText()
        episode = self.episode_cb.currentText()
        dept = 'anim' if self.dept_cb.currentText() == 'Animation' else 'lay'
        artistName = self.emplyee_le.text()
        if not artistName:
            self.showMessageBox(msgBody='No artist selected, please select an artist for assignment.',
                                header='Error', msgType='error')
            return False

        errorMessage = dict()
        rows = self.getSelectedRows()
        for e in rows:
            shotName = self.tableWidget.item(e, 0).text()
            # check in the fetched cached database for the shot entries for status, if it's not yet assigned then only
            # assign them else put them in the errorMessage.
            for eachLine in self.dbData:
                if shotName in eachLine:
                    if eachLine[4] not in ['NAY', None]:
                        errorMessage[shotName] = eachLine[3]
                        break
            else:
                with ConnectDB(project) as newdBcONN:
                    msg = 'UPDATE `{0}` SET `{1}_artist_name`="{2}",`{3}_status`="NYS" WHERE `shots` = "{4}"'.format(
                        episode, dept, artistName, dept, shotName)
                    newdBcONN.execute(msg)

        self.refreshTable()
        #
        if errorMessage:
            msgBody = 'One or more shot(s) are been assigned to other artist(s)'
            detail = ''
            for e in errorMessage.keys():
                detail += 'Shot {0} is already assigned to {1}, please use Re-assign option for this.\n'. \
                    format(e, errorMessage[e])
            self.showMessageBox(msgBody=msgBody, msgDetail=detail, header='Error', msgType='error')

    def reassignShots(self):
        self.comment_dict = dict()
        project = self.project_cb.currentText()
        episode = self.episode_cb.currentText()
        dept = 'anim' if self.dept_cb.currentText() == 'Animation' else 'lay'
        artistName = self.emplyee_le.text()
        if not artistName:
            self.showMessageBox(msgBody='No artist selected, please select an artist for assignment.',
                                header='Error', msgType='error')
            return False

        errorMessage = dict()
        commentError = list()
        artistError = list()
        rows = self.getSelectedRows()
        for e in rows:
            shotName = self.tableWidget.item(e, 0).text()
            # check in the fetched cached database for the shot entries for status, if it's not yet assigned then only
            # assign them else put them in the errorMessage.
            for eachLine in self.dbData:
                if shotName in eachLine:
                    print eachLine[4], '<------------------------------'
                    if eachLine[4] == '' or eachLine[4] is None:
                        # dict with shot name as key and dept.status and session.status as values list.
                        errorMessage[shotName] = eachLine[3], eachLine[4]
                        break
                    if eachLine[3] == artistName:
                        artistError.append(shotName)
                        break
            else:
                commentBox = commentMain.CommentMain(commentFor=shotName, prnt=self)
                commentBox.exec_()
                if self.comment is None or self.comment == '':
                    commentError.append(shotName)
                    continue
                now = datetime.datetime.now()
                finalComment = '{0}:{1}~'.format(now.strftime('%m-%d-%Y %H:%M'), self.comment)
                self.comment_dict[shotName] = self.comment
                with ConnectDB(project) as newdBcONN:
                    msg = 'UPDATE `{0}` SET `{1}_artist_name`="{2}", `{3}_comments`=CONCAT(COALESCE({4}_comments,' \
                          ' ""), "{5}"), `{7}_status`="TWIP" WHERE `shots` = "{6}"'.format(episode, dept, artistName,
                                                                                           dept, dept, finalComment,
                                                                                           shotName, dept)
                    newdBcONN.execute(msg)

        self.refreshTable()

        if errorMessage or commentError or artistError:
            msgBody = 'One or more shot(s) can\'t be reassigned, please check details for addition info.'
            detail = ''
            for e in errorMessage.keys():
                detail += 'Shot {0} departmen status is {1} and the session status is {2}.\n'.format(e,
                                                                                                     errorMessage[e][0],
                                                                                                     errorMessage[e][1])
            for each in commentError:
                detail += 'No comment received for shot {}.\n'.format(each)

            detail += '\n--------------------------------\n'

            for each in artistError:
                detail += '{} already assigned to same artist\n'.format(each)

            detail += '\n\nSession needs to be CLOSED for the shot to be reassigned.\n'
            detail += 'If the Shot is not yet assigned then use assign instead of reassign.\n'
            self.showMessageBox(msgBody=msgBody, msgDetail=detail, header='Error', msgType='error')

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
        self.allArtists = list()
        dept = 'ani' if self.dept_cb.currentText() == 'Animation' else 'lay'
        with ConnectDB('users') as dbConn:
            dbConn.execute('SELECT empname FROM `emp` WHERE `empdepts` LIKE "%{0}%" ORDER BY `empid` ASC'.format(dept))
            for eachArtist in dbConn.fetchall():
                artistList.append(eachArtist[0])
        self.allArtists = artistList
        model.setStringList(artistList)

    def updateDept(self):
        self.dept_cb.setCurrentIndex(0)

    def updateTable(self):
        # print self.project_cb.currentText()
        self.populateArtists()
        dept = self.dept_cb.currentText()
        episode = self.episode_cb.currentText()
        if dept == 'Select':
            return False
        dept = 'anim' if dept == 'Animation' else 'lay'
        dbQuerry = 'SELECT `shots`, `Start_Frame`, `End_Frame`, `%s_artist_name`, `%s_status`,  `Session_Status`, ' \
                   '`%s_startdate`, `%s_enddate`, `%s_publishdate`, `%s_comments` FROM `%s` ORDER BY `%s`.`shots` ASC' \
                   % (dept, dept, dept, dept, dept, dept, episode, episode)
        # dbData = None
        with ConnectDB(self.project_cb.currentText()) as dbCur:
            dbCur.execute(dbQuerry)

            self.dbData = dbCur.fetchall()

            headers = ['shots', 'Start_Frame', 'End_Frame', '%s_artist_name' % dept, '%s_status' % dept,
                       'Session_Status', '%s_startdate' % dept, '%s_enddate' % dept, '%s_publishdate' % dept,
                       '%s_comments' % dept]

        self.tableWidget.setRowCount(len(self.dbData))
        self.tableWidget.setColumnCount(len(self.dbData[0]))
        for i, each in enumerate(headers):
            itm = QtGui.QTableWidgetItem(each)
            self.tableWidget.setHorizontalHeaderItem(i, itm)

        for row, eachRow in enumerate(self.dbData):
            for col, eachCol in enumerate(eachRow):
                # print eachCol, row, col
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

    @staticmethod
    def showMessageBox(header='', msgBody='', msgDetail='', msgType='NoIcon'):
        msgBox = QtGui.QMessageBox()
        ico = msgBox.NoIcon
        if msgType in ['Critical', 'Error', 'ERROR']:
            ico = msgBox.Critical
        if msgType in ['Warning', 'WARNING']:
            ico = msgBox.Warning
        msgBox.setIcon(ico)
        if header:
            msgBox.setWindowTitle(header)
        if msgBody:
            msgBox.setText(msgBody)
        if msgDetail:
            msgBox.setDetailedText(msgDetail)
        msgBox.exec_()

    def mail_all_scenarios(self, scenario):
        mailSubject = ''
        messageToSend = ''
        while Switch(scenario):
            if case('Reassign'):
                print 'Reassigning shot(s)'
                mailSubject = ''
                messageToSend = ''
                break
            if case('Retake'):
                print 'Retake for shot(s)'
                mailSubject = ''
                messageToSend = ''
                break
            if case('Assign'):
                print 'Assigning shot(s)'
                mailSubject = ''
                messageToSend = ''
                break
            break

        # send_mail(mail_sub='', mail_body='', sender='', receivers=list()):
        mailing.send_mail(mail_sub=mailSubject, mail_body=messageToSend, sender=self.sender, receivers=self.receivers)


if __name__ == '__main__':
    qApp = QtGui.QApplication(sys.argv)
    win = ProductionWin()
    win.show()
    qApp.exec_()
