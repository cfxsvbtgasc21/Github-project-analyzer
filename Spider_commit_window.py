from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QFileDialog,QMessageBox
from PyQt5.QtGui import QIntValidator
import sys
import Spider_events as SP
from Spider_commit import Ui_MainWindow
class Spider_commit_window(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.spider_window = QMainWindow()
        self.ui_spider = Ui_MainWindow()  # 初始化为None
        self.ui_spider.setupUi(self)
        self.ui_spider.progressBar.setValue(0)
        self.ui_spider.stop.setEnabled(False)
        max_value = 100

        # 创建 QIntValidator，限制输入为大于0的整数且小于max_value
        validator = QIntValidator(1, max_value, self.ui_spider.count)
        self.ui_spider.count.setValidator(validator)
        # 连接信号
        self.ui_spider.back.clicked.connect(self.return_to_home)
        self.ui_spider.start.clicked.connect(self.show_results)
        self.ui_spider.stop.clicked.connect(self.stop_spi)
        self.ui_spider.actiontoken.triggered.connect(self.show_spider_help)
    def show_results(self):
            self.ui_spider.progressBar.setValue(0)
    def handle_results(self, results):
        try:
            self.ui_spider.listWidget.clear()
            # 限制结果大小
            max_length = 1000000  # 限制显示的最大字符数
            if len(results) > max_length:
                results = results[:max_length] + "\n... (内容已截断)"
            # 分批添加内容
            lines = results.split('\n')
            for i, line in enumerate(lines):
                if line.strip():
                    self.ui_spider.listWidget.addItem(line)

        except Exception as e:
            self.ui_spider.listWidget.addItem(f"显示结果时出错：{str(e)}")
        finally:
            # 重新启用开始按钮
            self.ui_spider.start.setEnabled(True)
            self.ui_spider.stop.setEnabled(False)

    def update_progress(self, value):
        try:
            self.ui_spider.progressBar.setValue(value)
        except Exception as e:
            print(f"更新进度条时出错：{str(e)}")
    def show_spider_help(self):
        self.message_help = QMessageBox()
        self.message_help.setWindowTitle("帮助")
        self.message_help.setText("这是个爬虫工具")
        self.message_help.show()
    def return_to_home(self):
        # 如果爬虫线程正在运行，先停止它
        if hasattr(self, 'spider_thread') and self.spider_thread.isRunning():
            self.stop_spi()
        if self:
            self.close()
            from home_window import MainApp
            self.home_window = MainApp()
            self.home_window.show()
    def stop_spi(self):
        try:
            if hasattr(self, 'spider_thread'):
                # 设置停止标志
                self.spider_thread.is_running = False
                # 等待线程结束
                self.spider_thread.wait()
                # 重置进度条
                self.ui_spider.progressBar.setValue(0)
                # 重新启用开始按钮
                self.ui_spider.start.setEnabled(True)
                # 在列表中显示取消信息
                self.ui_spider.listWidget.clear()
                self.ui_spider.listWidget.addItem("爬取已取消")
        except Exception as e:
            print(f"停止爬虫时出错：{str(e)}")
