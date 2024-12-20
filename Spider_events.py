from PyQt5.QtCore import QThread, pyqtSignal
import requests
class SpiderThread(QThread):
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(str)
    def __init__(self, url,Cookie=None):
        super().__init__()
        self.url = url
        self.Cookie=Cookie
        self.is_running = True
    def run(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Cookie':  self.Cookie
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

