from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QFileDialog,QMessageBox
from home import Ui_home
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.spider_window = None  # 初始化为None
        self.ui_home = Ui_home()
        self.ui_home.setupUi(self)
        self.show()
        # 连接信号
        self.ui_home.spider.clicked.connect(self.show_spider_window)
    def show_spider_window(self):
        from Spider_window import Spider_window
        self.Spider_window=Spider_window()
        self.Spider_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    M = MainApp()
    app.exec_()