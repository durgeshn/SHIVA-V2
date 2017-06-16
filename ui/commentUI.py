# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\user\durgesh.n\workspace\SHIVA-V2\ui\commentUI.ui'
#
# Created: Fri Jun 16 15:11:34 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(464, 185)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.comment_te = QtGui.QTextEdit(Dialog)
        self.comment_te.setObjectName("comment_te")
        self.verticalLayout.addWidget(self.comment_te)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_pb = QtGui.QPushButton(Dialog)
        self.ok_pb.setObjectName("ok_pb")
        self.horizontalLayout.addWidget(self.ok_pb)
        self.cancel_pb = QtGui.QPushButton(Dialog)
        self.cancel_pb.setObjectName("cancel_pb")
        self.horizontalLayout.addWidget(self.cancel_pb)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_pb.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_pb.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

