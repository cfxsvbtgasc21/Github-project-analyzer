from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import home
import PyQt5.QtCore as QtCore
import sys
import  Spider as S


def on_spider_clicked(s):
    mainwindow = QMainWindow()
    # mainwindow.setParent(s)
    ui = S.Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    # mainwindow.exec_()
    s.close()

if __name__=="__main__":

    app=QApplication(sys.argv)
    mainwindow=QWidget()
    spider_window = QMainWindow()
    ui=home.Ui_home()
    ui.setupUi(mainwindow)
    mainwindow.show()
    ui.spider.clicked.connect(lambda: on_spider_clicked(mainwindow))

    sys.exit(app.exec_())
