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
        self.ui_home.help.clicked.connect(self.show_helps)
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
    def show_helps(self):
        self.message_help = QMessageBox()
        self.message_help.setWindowTitle("帮助")
        self.message_help.setText("这是个Github项目的分析器，里面包括对象的issues分析和commmits分析。issues分析可以得到主要问题的信息和解决时间对比。\ncommmits分析是对该项目提交记录基于作者和日期的分析。")
        self.message_help.show()
    def quit(self):
        exit(0)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    M = MainApp()
    app.exec_()