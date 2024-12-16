from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QFileDialog
from home import Ui_home
import sys
from Spider import Ui_MainWindow
import requests
from PyQt5.QtCore import QThread, pyqtSignal

class SpiderThread(QThread):
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(str)
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.is_running = True
    def run(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(
                self.url,
                stream=True,
                headers=headers,
                timeout=10
            )
            if response.status_code != 200:
                self.result_ready.emit(f"错误：HTTP状态码 {response.status_code}")
                return
            encoding = response.encoding or 'utf-8'
            # 先获取完整内容的大小
            content = response.content
            total_size = len(content)
            # 分块处理内容
            block_size = 1024
            processed = 0
            result = []
            while processed < total_size:
                if not self.is_running:
                    self.result_ready.emit("爬取已取消")
                    return

                chunk = content[processed:processed + block_size]
                try:
                    result.append(chunk.decode(encoding))
                except UnicodeDecodeError:
                    result.append(chunk.decode('utf-8', errors='ignore'))

                processed += len(chunk)
                progress = int((processed / total_size) * 100)
                print(f"进度：{progress}%")
                self.progress_updated.emit(progress)

            final_content = ''.join(result)
            self.result_ready.emit(final_content)
        except requests.exceptions.Timeout:
            self.result_ready.emit("错误：请求超时")
        except requests.exceptions.ConnectionError:
            self.result_ready.emit("错误：连接失败")
        except Exception as e:
            self.result_ready.emit(f"未知错误：{str(e)}")



class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.home_window = QWidget()
        self.spider_window = None  # 初始化为None
        self.setup_home()

    def show_results(self):
        try:
            url = self.ui_spider.address.text().strip()
            if not url:
                self.ui_spider.listWidget.addItem("请输入URL地址")
                return
            
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'http://' + url
            # 创建并启动爬虫线程
            self.spider_thread = SpiderThread(url)
            self.ui_spider.stop.setEnabled(True)
            self.spider_thread.progress_updated.connect(self.update_progress)
            self.spider_thread.result_ready.connect(self.handle_results)
            # 禁用开始按钮
            self.ui_spider.start.setEnabled(False)
            # 重置进度条
            # self.ui_spider.progressBar.setValue(0)

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

    def setup_home(self):
        self.ui_home = Ui_home()
        self.ui_home.setupUi(self.home_window)
        self.home_window.show()
        # 连接信号
        self.ui_home.spider.clicked.connect(self.show_spider_window)

    def show_spider_window(self):
        # 创建新窗口
        self.spider_window = QMainWindow()
        self.ui_spider = Ui_MainWindow()
        self.ui_spider.setupUi(self.spider_window)
        self.ui_spider.progressBar.setValue(0)

        self.spider_window.show()
        self.home_window.hide()
        self.ui_spider.stop.setEnabled(False)
        # 连接信号
        self.ui_spider.back.clicked.connect(self.return_to_home)
        self.ui_spider.start.clicked.connect(self.show_results)
        self.ui_spider.stop.clicked.connect(self.stop_spi)
        self.ui_spider.save_address.setReadOnly(True)
        self.ui_spider.browse.clicked.connect(self.open_file_dialog)
    def return_to_home(self):
        # 如果爬虫线程正在运行，先停止它
        if hasattr(self, 'spider_thread') and self.spider_thread.isRunning():
            self.stop_spi()

        if self.spider_window:
            self.spider_window.close()
            self.spider_window = None
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

    def open_file_dialog(self):
        # 修改为使用spider_window作为父窗口
        directory = QFileDialog.getExistingDirectory(
            self.spider_window,  # 使用spider_window作为父窗口
            "选择目录",
            "",
            QFileDialog.ShowDirsOnly
        )
        if directory:  # 添加检查，确保用户选择了目录
            self.ui_spider.save_address.setText(directory)
    def run(self):
        return self.app.exec_()


if __name__ == "__main__":
    app = MainApp()
    sys.exit(app.run())