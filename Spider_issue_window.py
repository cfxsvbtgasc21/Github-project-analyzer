from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QFileDialog,QMessageBox

import sys
import Spider_events as SP
from Spider import Ui_MainWindow
class Spider_issue_window(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.spider_window = QMainWindow()
        self.ui_spider = Ui_MainWindow()  # 初始化为None
        self.ui_spider.setupUi(self)

        self.ui_spider.progressBar.setValue(0)
        self.ui_spider.stop.setEnabled(False)
        # 连接信号
        self.ui_spider.back.clicked.connect(self.return_to_home)
        self.ui_spider.start.clicked.connect(self.show_results)
        self.ui_spider.stop.clicked.connect(self.stop_spi)
        self.ui_spider.save_address.setReadOnly(True)
        self.ui_spider.browse.clicked.connect(self.open_file_dialog)
        self.ui_spider.introduction.triggered.connect(self.show_spider_help)
        # self.spider_window.show()
        # self.home_window.hide()
    def show_results(self):
        try:
            self.ui_spider.progressBar.setValue(0)
            url = self.ui_spider.address.text().strip()
            if not url:
                self.ui_spider.listWidget.addItem("请输入URL地址")
                return
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'http://' + url
            # 创建并启动爬虫线程
            co = self.ui_spider.Cookie.text()
            self.spider_thread = SP.SpiderThread(url, co)
            self.ui_spider.stop.setEnabled(True)
            self.spider_thread.progress_updated.connect(self.update_progress)
            self.spider_thread.result_ready.connect(self.handle_results)
            # 禁用开始按钮
            self.ui_spider.start.setEnabled(False)
            self.spider_thread.start()
        except Exception as e:
            self.ui_spider.listWidget.addItem(f"启动爬虫时出错：{str(e)}")
            self.ui_spider.start.setEnabled(True)
            self.ui_spider.stop.setEnabled(False)

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
            if hasattr(self, 'spider_thread')and self.spider_thread.isRunning():
                # 设置停止标志
                self.spider_thread.is_running = False
                # 等待线程结束
                self.spider_thread.terminate()
                # 重置进度条
                self.ui_spider.progressBar.setValue(0)
                # 重新启用开始按钮
                self.ui_spider.start.setEnabled(True)
                # 在列表中显示取消信息
                self.ui_spider.listWidget.clear()
                self.ui_spider.listWidget.addItem("爬取已取消")
        except Exception as e:
            print(f"停止爬虫时出错：{str(e)}")

    def open_file_dialog(self):
        directory = QFileDialog.getExistingDirectory(
            self,  # 使用spider_window作为父窗口
            "选择目录",
            "",
            QFileDialog.ShowDirsOnly
        )
        if directory:  # 添加检查，确保用户选择了目录
            self.ui_spider.save_address.setText(directory)

