# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Spider_issue.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 981)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.username = QtWidgets.QLineEdit(self.frame)
        self.username.setObjectName("username")
        self.horizontalLayout.addWidget(self.username)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(30)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.token = QtWidgets.QLineEdit(self.frame)
        self.token.setObjectName("token")
        self.horizontalLayout_2.addWidget(self.token)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(40)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.repo = QtWidgets.QLineEdit(self.frame)
        self.repo.setObjectName("repo")
        self.horizontalLayout_4.addWidget(self.repo)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addWidget(self.frame)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.start = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)
        self.start.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.start.setAcceptDrops(False)
        self.start.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.start.setObjectName("start")
        self.horizontalLayout_3.addWidget(self.start)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.stop = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop.sizePolicy().hasHeightForWidth())
        self.stop.setSizePolicy(sizePolicy)
        self.stop.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stop.setAcceptDrops(False)
        self.stop.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stop.setObjectName("stop")
        self.horizontalLayout_3.addWidget(self.stop)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.progressBar = QtWidgets.QProgressBar(self.frame_2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.listWidget = QtWidgets.QListWidget(self.frame_2)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.generate_cloud = QtWidgets.QPushButton(self.frame_2)
        self.generate_cloud.setObjectName("generate_cloud")
        self.horizontalLayout_6.addWidget(self.generate_cloud)
        self.generate = QtWidgets.QPushButton(self.frame_2)
        self.generate.setObjectName("generate")
        self.horizontalLayout_6.addWidget(self.generate)
        self.back = QtWidgets.QPushButton(self.frame_2)
        self.back.setObjectName("back")
        self.horizontalLayout_6.addWidget(self.back)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 30))
        self.menubar.setObjectName("menubar")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.introduction = QtWidgets.QAction(MainWindow)
        self.introduction.setObjectName("introduction")
        self.actions = QtWidgets.QAction(MainWindow)
        self.actions.setObjectName("actions")
        self.menu_2.addAction(self.introduction)
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "爬虫参数设置"))
        self.label_2.setText(_translate("MainWindow", "用户名称"))
        self.label_3.setText(_translate("MainWindow", "token设置"))
        self.label_6.setText(_translate("MainWindow", "仓库名称"))
        self.start.setText(_translate("MainWindow", "开始爬取"))
        self.stop.setText(_translate("MainWindow", "停止爬取"))
        self.label_4.setText(_translate("MainWindow", "爬取进度"))
        self.label_5.setText(_translate("MainWindow", "结果显示"))
        self.generate_cloud.setText(_translate("MainWindow", "生成词云"))
        self.generate.setText(_translate("MainWindow", "生成分析图"))
        self.back.setText(_translate("MainWindow", "返回主页面"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.introduction.setText(_translate("MainWindow", "token获取说明"))
        self.actions.setText(_translate("MainWindow", "保存"))
