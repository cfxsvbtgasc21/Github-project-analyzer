import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QLabel)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from crawler import GitHubCrawler


class CrawlerThread(QThread):
    # 定义信号，用于线程完成时传递数据和发生错误时传递错误信息
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        
    def run(self):
        try:
            # 创建GitHub爬虫实例
            crawler = GitHubCrawler()
            # 调用爬虫获取仓库信息
            repo = crawler.get_repository_info(self.url)
            # 发射finished信号，并将仓库信息传递给主线程
            self.finished.emit(repo)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GitHub项目分析器')
        self.setMinimumSize(800, 600)
        
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()    # 创建URL输入框
        self.url_input.setPlaceholderText('输入GitHub仓库URL')
        self.analyze_btn = QPushButton('分析')      # 创建分析按钮
        self.analyze_btn.clicked.connect(self.start_analysis)
        
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.analyze_btn)
        
        # 创建结果显示区域
        self.result_label = QLabel('在此显示分析结果')
        self.result_label.setAlignment(Qt.AlignCenter)
        
        # 添加到主布局
        layout.addLayout(input_layout)
        layout.addWidget(self.result_label)
        
    def start_analysis(self):
        # 获取用户输入的GitHub仓库URL
        url = self.url_input.text().strip()
        if not url:
            self.result_label.setText('请输入有效的GitHub仓库URL')
            return
        if not url.startswith('https://github.com/'):
            self.result_label.setText('请输入有效的GitHub仓库URL\n例如：https://github.com/username/repo')
            return
        self.analyze_btn.setEnabled(False)  # 禁用分析按钮，防止重复点击
        self.result_label.setText('正在分析...')
        
        self.thread = CrawlerThread(url)
        self.thread.finished.connect(self.show_results)
        self.thread.error.connect(self.show_error)
        self.thread.start()
        
    def show_results(self, repo):
        self.analyze_btn.setEnabled(True)       #启用分析按钮
        result_text = f"""
        仓库名称: {repo.name}
        作者: {repo.owner}
        Star数: {repo.stars}
        Fork数: {repo.forks}
        """
        print(result_text)
        self.result_label.setText(result_text)
        
    def show_error(self, error_msg):
        self.analyze_btn.setEnabled(True)
        print("错误：",error_msg)
        self.result_label.setText(f'错误: {error_msg}')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 