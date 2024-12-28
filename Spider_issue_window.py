from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QFileDialog,QMessageBox
import sys

from matplotlib import pyplot as plt
from wordcloud import WordCloud

import Spider_events as SP
from Spider_issue import Ui_MainWindow
class Spider_issue_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_spider = Ui_MainWindow()  # 初始化为None
        self.ui_spider.setupUi(self)
        self.ui_spider.progressBar.setValue(0)
        self.ui_spider.stop.setEnabled(False)
        # 连接信号
        self.ui_spider.back.clicked.connect(self.return_to_home)
        self.ui_spider.start.clicked.connect(self.show_results)
        self.ui_spider.stop.clicked.connect(self.stop_spi)
        self.ui_spider.introduction.triggered.connect(self.show_spider_help)
        self.ui_spider.generate_cloud.clicked.connect(self.generate_wordcloud)
        self.ui_spider.generate.clicked.connect(self.generate_pie_chart)
        self.results=None

    def show_results(self):
        try:
            self.ui_spider.progressBar.setValue(0)
            self.ui_spider.listWidget.clear()
            # 创建并启动爬虫线程
            self.spider_thread = SP.SpiderThread2(self.ui_spider.username.text(), self.ui_spider.repo.text(),self.ui_spider.token.text())
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
    def generate_wordcloud(self):
        def extract_labels(issues):
            label_counts = {}
            for issue in issues:
                for label in issue['labels']['nodes']:
                    label_name = label['name']
                    if label_name in label_counts:
                        label_counts[label_name] += 1
                    else:
                        label_counts[label_name] = 1
            return label_counts
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(extract_labels(self.results))
        # 显示词云图
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title("The word cloud generated for issues based on labels")
        plt.axis('off')
        plt.show()
        # plt.savefig('pie_chart.png', format='png')

    def generate_pie_chart(self):
        def calculate_time_diff_and_classify(issues):
            categories = {
                '0-1 days': 0,
                '1-3 days': 0,
                '3-7 days': 0,
                '7+ days': 0
            }

            for issue in issues:
                created_at = datetime.strptime(issue['createdAt'], "%Y-%m-%dT%H:%M:%SZ")
                closed_at = datetime.strptime(issue['closedAt'], "%Y-%m-%dT%H:%M:%SZ")

                # 计算时间差
                time_diff = (closed_at - created_at).days

                # 分类
                if time_diff <= 1:
                    categories['0-1 days'] += 1
                elif 1 < time_diff <= 3:
                    categories['1-3 days'] += 1
                elif 3 < time_diff <= 7:
                    categories['3-7 days'] += 1
                else:
                    categories['7+ days'] += 1

            return categories

        categories=calculate_time_diff_and_classify(self.results)
        labels = categories.keys()
        sizes = categories.values()

        # 画饼状图
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
        plt.title('Time to Resolve Issues')
        plt.axis('equal')  # 让饼图为圆形
        plt.show()
        # plt.savefig('bing.png', format='png')

    def handle_results(self, results):
        try:
            self.results=results
            self.ui_spider.listWidget.clear()
            for issue in results:
                self.ui_spider.listWidget.addItem(f"Title: {issue['title']}")
                self.ui_spider.listWidget.addItem(f"Number: #{issue['number']}")
                self.ui_spider.listWidget.addItem(f"Created At: {issue['createdAt']}")
                self.ui_spider.listWidget.addItem(f"Closed At: {issue['closedAt']}")
                self.ui_spider.listWidget.addItem(f"Body: {issue['body'][:200]}...")  # 仅显示前200个字符
                self.ui_spider.listWidget.addItem("-" * 80)
                labels = [label['name'] for label in issue['labels']['nodes']]
                if labels:
                    self.ui_spider.listWidget.addItem(f"Labels: {', '.join(labels)}")
                else:
                    self.ui_spider.listWidget.addItem("Labels: None")
                self.ui_spider.listWidget.addItem("-" * 80)
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

