from collections import defaultdict
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QFileDialog,QMessageBox
from PyQt5.QtGui import QIntValidator
import sys
import Spider_events as SP
import matplotlib.pyplot as plt
from Spider_commit import Ui_MainWindow
class Spider_commit_window(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.spider_window = QMainWindow()
        self.ui_spider = Ui_MainWindow()  # 初始化为None
        self.ui_spider.setupUi(self)
        self.ui_spider.progressBar.setValue(0)
        self.ui_spider.stop.setEnabled(False)

        # self.ui_spider.generate.setEnabled(False)
        max_value = 2000
        # 创建 QIntValidator，限制输入为大于0的整数且小于max_value
        validator = QIntValidator(1, max_value, self.ui_spider.count)
        self.ui_spider.count.setValidator(validator)
        # 连接信号
        self.ui_spider.summary.clicked.connect(self.analyze_author)
        self.ui_spider.generate.clicked.connect(self.generate_author)
        self.ui_spider.back.clicked.connect(self.return_to_home)
        self.ui_spider.start.clicked.connect(self.show_results)
        self.ui_spider.stop.clicked.connect(self.stop_spi)
        self.ui_spider.actiontoken.triggered.connect(self.show_spider_help)
        self.ui_spider.generate.setEnabled(False)
        self.ui_spider.summary.setEnabled(False)
        self.results=None
    def handle_results(self, all_commits):
        # 处理结果
        self.ui_spider.listWidget.clear()
        self.results = all_commits
        try:
            commit_count = 0
            for commit in self.results:
                commit_count += 1
                self.ui_spider.listWidget.addItem(f"Commit{commit_count}:")
                self.ui_spider.listWidget.addItem(f"Commit Message: {commit['node']['messageHeadline']}")
                self.ui_spider.listWidget.addItem(f"Author Avatar: {commit['node']['author']['avatarUrl']}")
                self.ui_spider.listWidget.addItem(f"Commit Date: {commit['node']['committedDate']}")
                self.ui_spider.listWidget.addItem(f"Commit URL: {commit['node']['commitUrl']}")
            self.ui_spider.summary.setEnabled(True)
        except Exception as e:
            self.ui_spider.listWidget.addItem(f"显示结果时出错：{str(e)}")
        finally:
            # 重新启用开始按钮
            self.ui_spider.start.setEnabled(True)
            self.ui_spider.stop.setEnabled(False)
    def analyze_author(self):
        if self.ui_spider.comboBox.currentText()=="author":
            try:
                # 尝试构建每个作者的提交计数字典
                self.commit_counts_dir = {author: sum(1 for c in self.results if c['node']['author']['name'] == author)
                                          for author in set([c['node']['author']['name'] for c in self.results])}

                # 过滤出提交数大于等于指定值的作者
                self.ui_spider.count.text()  # 确保这里 self.ui_spider.count 是一个 QLineEdit 对象，并且有 text() 方法
                self.commit_counts_dir_filtered = {author: count for author, count in self.commit_counts_dir.items() if
                                                   count >= int(self.ui_spider.count.text())}

                # 清除列表控件并添加过滤后的作者和提交数
                self.ui_spider.listWidget.clear()
                for author, count in self.commit_counts_dir_filtered.items():
                    self.ui_spider.listWidget.addItem(f"Author: {author}, Commit Count: {count}")
                self.ui_spider.generate.setEnabled(True)
            except AttributeError as e:
                QMessageBox.critical(None, "Attribute Error", f"属性错误：{str(e)}")
            except ValueError as e:
                QMessageBox.critical(None, "Value Error", f"值错误，可能是转换整数失败：{str(e)}")
            except Exception as e:
                QMessageBox.critical(None, "Unknown Error", f"分析作者时出现未知错误：{str(e)}")
        else:
            try:
                commits_by_date = defaultdict(int)
                # 遍历所有提交，按日期分组并计数
                for commit in self.results:
                    # 提取提交日期并转换为年月日格式
                    commit_date = datetime.strptime(commit['node']['committedDate'], '%Y-%m-%dT%H:%M:%SZ').strftime(
                        '%Y-%m-%d')
                    # 对每个日期的提交进行计数
                    commits_by_date[commit_date] += 1
                threshold = int(self.ui_spider.count.text())
                # 过滤出提交数大于等于指定值的日期
                self.commit_counts_dir_filtered= {date: count for date, count in commits_by_date.items() if
                                            count >= threshold}
                # 清除列表控件并添加过滤后的日期和提交数
                self.ui_spider.listWidget.clear()
                for date, count in sorted(self.commit_counts_dir_filtered.items()):
                    self.ui_spider.listWidget.addItem(f"Date: {date}, Commit Count: {count}")
                self.ui_spider.generate.setEnabled(True)
            except AttributeError as e:
                QMessageBox.critical(None, "Attribute Error", f"属性错误：{str(e)}")
            except ValueError as e:
                QMessageBox.critical(None, "Value Error", f"值错误，可能是转换整数失败：{str(e)}")
            except Exception as e:
                QMessageBox.critical(None, "Unknown Error", f"分析日期时出现未知错误：{str(e)}")
    def generate_author(self):
        try:
            plt.bar(self.commit_counts_dir_filtered.keys(), self.commit_counts_dir_filtered.values())
            plt.ylabel('Commit Count')
            plt.show()
        except Exception as e:
            # 弹出错误窗口
            QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
    def show_results(self):
        try:
            self.ui_spider.count.clear()
            self.ui_spider.listWidget.clear()
            self.ui_spider.progressBar.setValue(0)
            self.spider_thread = SP.SpiderThread(self.ui_spider.username.text(), self.ui_spider.repo.text(), self.ui_spider.token.text())
            # self.spider_thread.is_running=True
            self.spider_thread.result_ready.connect(self.handle_results)
            # 禁用开始按钮
            self.ui_spider.start.setEnabled(False)
            self.ui_spider.stop.setEnabled(True)
            self.spider_thread.progress_updated.connect(self.update_progress)
            self.spider_thread.error_occurred.connect(self.show_error_message)
            self.spider_thread.start()
            # 禁用开始按钮
        except Exception as e:
            self.ui_spider.listWidget.addItem(f"启动爬虫时出错：{str(e)}")
            self.ui_spider.start.setEnabled(True)
            self.ui_spider.stop.setEnabled(False)
    # 连接信号
    def update_progress(self, value):
        try:
            self.ui_spider.progressBar.setValue(value)
        except Exception as e:
            print(f"更新进度条时出错：{str(e)}")

    def show_spider_help(self):
        self.message_help = QMessageBox()
        self.message_help.setWindowTitle("帮助")
        self.message_help.setText(
            "创建个人访问令牌（Personal Access Token, PAT）：\n登录你的GitHub账户。访问设置页面，\n找到“Developer settings”部分。\n在“Personal access tokens”中，点击“Generate new token”。\n给令牌命名，并选择你希望授权的权限范围（scopes）。对于基本的仓库访问，你可能需要勾选repo。\n生成令牌后，请确保复制并保存该令牌，因为它不会再次显示。")
        self.message_help.show()

    def show_error_message(self, message):
        QMessageBox.critical(self, "错误", message)
        self.results = None
        self.ui_spider.start.setEnabled(True)
        self.ui_spider.stop.setEnabled(False)
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
                self.spider_thread.terminate()
                # 重置进度条
                self.ui_spider.progressBar.setValue(0)
                # 重新启用开始按钮
                self.ui_spider.start.setEnabled(True)
                self.ui_spider.stop.setEnabled(False)
                self.ui_spider.generate.setEnabled(False)
                self.ui_spider.summary.setEnabled(False)
                # 在列表中显示取消信息
                self.ui_spider.listWidget.clear()
                self.ui_spider.listWidget.addItem("爬取已取消")
        except Exception as e:
            print(f"停止爬虫时出错：{str(e)}")
