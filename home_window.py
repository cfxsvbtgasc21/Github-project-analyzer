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
        self.ui_home.spider_issues.clicked.connect(self.show_spider_issues_window)
        self.ui_home.spider_commits.clicked.connect(self.show_spider_commits_window)
        self.ui_home.exit.clicked.connect(self.quit)
    def show_spider_issues_window(self):
        from Spider_issue_window import Spider_issue_window
        self.Spider_window=Spider_issue_window()
        self.Spider_window.show()
        self.close()
    def show_spider_commits_window(self):
        from Spider_commit_window import Spider_commit_window
        self.Spider_window = Spider_commit_window()
        self.Spider_window.show()
        self.close()
    def quit(self):
        exit(0)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    M = MainApp()
    app.exec_()