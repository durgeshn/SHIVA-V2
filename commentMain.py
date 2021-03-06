import sys

from PySide import QtGui

from ui import commentUI


class CommentMain(QtGui.QDialog, commentUI.Ui_Dialog):
    def __init__(self, commentFor, prnt=None):
        super(CommentMain, self).__init__(prnt)
        self.commentFor = commentFor
        self.prnt = prnt
        self.setupUi(self)
        self.setWindowTitle('Commaent for {0}'.format(self.commentFor))
        self.makeConnection()
        # self.show()
        # self.exec_()

    def makeConnection(self):
        self.cancel_pb.clicked.connect(self.close)
        self.ok_pb.clicked.connect(self.commentIt)

    def commentIt(self):
        if self.comment_te.toPlainText() == '':
            return False
        self.close()
        if self.prnt:
            self.prnt.comment = self.comment_te.toPlainText().replace('\\', '/')
        print self.comment_te.toPlainText().replace('\\', '/')
        return self.comment_te.toPlainText().replace('\\', '/')

    def getvslue(self):
        return self.prnt.comment

    def __repr__(self):
        # return self.commentIt()
        return self.comment_te.toPlainText().replace('\\', '/')


def main(commentFor, prnt=None):
    qApp = QtGui.QApplication(sys.argv)
    commentWin = CommentMain(commentFor=commentFor, prnt=prnt)
    commentWin.exec_()
    qApp.exec_()

if __name__ == '__main__':
    main('sh001')
    print