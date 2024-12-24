from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
import requests
import re
import certifi
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
def spider_issues():
    headers={
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }
    page=1
    tip_dic = {}
    while page <= 100:
        url=f'https://github.com/ultralytics/ultralytics/issues?page={page}&q=is%3Aissue+is%3Aopen'
        try:
        # certificate_path = certifi.where()
            response = requests.get(url=url,verify=False)
            response.raise_for_status()
            html= response.text
            soup = BeautifulSoup(html, 'html.parser')
            # id_divs =soup.find_all('div', id=lambda x: x and x.startswith('issue_'))
            labels = []
            a_tags = soup.find_all('a', id=lambda x: x and x.startswith('label-'))
            for a_tag in a_tags:
                labels.append(a_tag.get_text(strip=True))
            if len(labels) == 0:
                print(page)
                break
            for label in labels:
                if label in tip_dic:
                    tip_dic[label] += 1
                else:
                    tip_dic[label] = 1
            page+=1
        except requests.exceptions.HTTPError as e:
            print(f"HTTP错误：{e}",page)
            break
        except requests.exceptions.Timeout:
            print("请求超时")
            break
        except requests.exceptions.ConnectionError:
            print("连接失败")
            break
        except Exception as e:
            print(f"未知错误：{e}")
            break
    print(tip_dic)
def generate_cloud(text):
    headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }
    page = 2
    labels = []
    url = f'https://github.com/vercel/ai/issues'
    response = requests.get(url=url, verify=False)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # id_divs =soup.find_all('div', id=lambda x: x and x.startswith('issue_'))
    a_tags = soup.find_all('a', id=lambda x: x and x.startswith('issue_'))
    for a_tag in a_tags:
        labels.append(a_tag.get_text(strip=True))
    print(labels)
    while page <= 30:
        url = f'https://github.com/vercel/ai/issues?page={page}&q=is%3Aissue+is%3Aopen'
        try:
            # certificate_path = certifi.where()
            response = requests.get(url=url, verify=False)
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            a_tags = soup.find_all('a', id=lambda x: x and x.startswith('issue_'))
            for a_tag in a_tags:
                labels.append(a_tag.get_text(strip=True))
            page += 1
        except requests.exceptions.HTTPError as e:
            print(f"HTTP错误：{e}", page)
            break
        except requests.exceptions.Timeout:
            print("请求超时")
            break
        except requests.exceptions.ConnectionError:
            print("连接失败")
            break
        except Exception as e:
            print(f"未知错误：{e}")
            break
        page +=1

    text = ' '.join(labels)
    print(text)

    # 创建WordCloud对象
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    # 显示生成的词云图像
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    plt.show()

def generate_time_seq():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }
    page = 1
    tip_dic = {}
    url = 'https://github.com/ultralytics/ultralytics/commits/main/'
    # print(certifi.where())
    response = requests.get(url=url, headers=headers,verify=False)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    h3_tags = soup.find_all('h3',class_='text-normal f5 py-1 prc-Heading-Heading-6CmGO')

    # 遍历找到的<h3>标签
    for tag in h3_tags:
        # 打印<h3>标签的文本内容
        print(tag.get_text())
    ul_tags = soup.find_all('ul',class_='Box-sc-g0xbh4-0 ListView-module__ul--vMLEZ')
    for ul_tag in ul_tags:
        # 提取<ul>标签下的所有<li>标签
        li_tags = ul_tag.find_all('li')
        # 遍历<li>标签并打印它们的文本内容
        for li in li_tags:
            print(li.get_text())
    # print(html)
if __name__ == "__main__":
    # generate_cloud("s")
    # spider_issues()
    generate_time_seq()
