# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\user\durgesh.n\workspace\SHIVA-V2\ui\saveNextUI.ui'
#
# Created: Mon Jun 12 12:36:00 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(318, 105)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(60, 20))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.version_sb = QtGui.QSpinBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.version_sb.sizePolicy().hasHeightForWidth())
        self.version_sb.setSizePolicy(sizePolicy)
        self.version_sb.setMinimumSize(QtCore.QSize(50, 20))
        self.version_sb.setObjectName("version_sb")
        self.horizontalLayout.addWidget(self.version_sb)
        self.useNextVersion_cb = QtGui.QCheckBox(self.centralwidget)
        self.useNextVersion_cb.setEnabled(False)
        self.useNextVersion_cb.setCheckable(True)
        self.useNextVersion_cb.setChecked(True)
        self.useNextVersion_cb.setObjectName("useNextVersion_cb")
        self.horizontalLayout.addWidget(self.useNextVersion_cb)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.fileNamePre_l = QtGui.QLabel(self.centralwidget)
        self.fileNamePre_l.setObjectName("fileNamePre_l")
        self.horizontalLayout_2.addWidget(self.fileNamePre_l)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.workAreaPath_l = QtGui.QLabel(self.centralwidget)
        self.workAreaPath_l.setObjectName("workAreaPath_l")
        self.horizontalLayout_3.addWidget(self.workAreaPath_l)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtGui.QSpacerItem(138, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.cancel_pb = QtGui.QPushButton(self.centralwidget)
        self.cancel_pb.setObjectName("cancel_pb")
        self.horizontalLayout_4.addWidget(self.cancel_pb)
        self.save_pb = QtGui.QPushButton(self.centralwidget)
        self.save_pb.setObjectName("save_pb")
        self.horizontalLayout_4.addWidget(self.save_pb)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Version :", None, QtGui.QApplication.UnicodeUTF8))
        self.useNextVersion_cb.setText(QtGui.QApplication.translate("MainWindow", "Use Next Available Version Number", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "File Name Preview :", None, QtGui.QApplication.UnicodeUTF8))
        self.fileNamePre_l.setText(QtGui.QApplication.translate("MainWindow", "..............................", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "   Work Area Path :", None, QtGui.QApplication.UnicodeUTF8))
        self.workAreaPath_l.setText(QtGui.QApplication.translate("MainWindow", ".................................", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_pb.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.save_pb.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))

