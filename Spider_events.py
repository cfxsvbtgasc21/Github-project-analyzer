import json

from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
import requests
import re
import certifi
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime

# 设置全局字体
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号
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
def spider_issues():
    headers={
        # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Cookie':'_octo=GH1.1.117660236.1704097656; _device_id=22c6c1235a4fe7962feab7582cdd87ef; saved_user_sessions=164596506%3A1ZcRB2B86n1QryR0uawQxK9gPNU19iSbqSA_JnGxt42QMdi7; user_session=1ZcRB2B86n1QryR0uawQxK9gPNU19iSbqSA_JnGxt42QMdi7; __Host-user_session_same_site=1ZcRB2B86n1QryR0uawQxK9gPNU19iSbqSA_JnGxt42QMdi7; logged_in=yes; dotcom_user=cfxsvbtgasc21; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai; _gh_sess=YNSP1MCxc2C%2BOIQSyzNQPAg0CXgGd9NIHygQp1WhtX1GHqfa0uflls9MIB4l0AVzrtHgq4XXeIBU403EkFUyBFX4W%2Bv291ghaeFZvs%2FH3Z9S%2BLvahIKxsTSD3%2F3wMDveT8d8iaeynapsxF0QGhmcQtMq2EoonkCOb7MmJT9V3xGXRXCyjJYV2WBb4%2Bx6w4JmxkX3HGsn4I6ei6cjTx%2FwSDxae307fULElAhFUUQyJn9VSenQj5LoqJJC0rQIN93UDJ9OQOOjdEUoZF4s1vFx9pQdxXnQVaLyIRSpIs7DFNhEKddwKUioXc%2F3jdsKauunGM%2Fq6Rw1HRWymwBSbggG%2FXbPUSYSJoH7Hr39jZ3UlRuehuOLmQZmbDndw6fuaDtq--QubxNrIrwFywBl80--27XuIPNf%2F9AGfkVs%2BrCvXg%3D%3D'
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
        # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Cookie': '_octo=GH1.1.117660236.1704097656; _device_id=22c6c1235a4fe7962feab7582cdd87ef; saved_user_sessions=164596506%3A1ZcRB2B86n1QryR0uawQxK9gPNU19iSbqSA_JnGxt42QMdi7; user_session=1ZcRB2B86n1QryR0uawQxK9gPNU19iSbqSA_JnGxt42QMdi7; __Host-user_session_same_site=1ZcRB2B86n1QryR0uawQxK9gPNU19iSbqSA_JnGxt42QMdi7; logged_in=yes; dotcom_user=cfxsvbtgasc21; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai; _gh_sess=YNSP1MCxc2C%2BOIQSyzNQPAg0CXgGd9NIHygQp1WhtX1GHqfa0uflls9MIB4l0AVzrtHgq4XXeIBU403EkFUyBFX4W%2Bv291ghaeFZvs%2FH3Z9S%2BLvahIKxsTSD3%2F3wMDveT8d8iaeynapsxF0QGhmcQtMq2EoonkCOb7MmJT9V3xGXRXCyjJYV2WBb4%2Bx6w4JmxkX3HGsn4I6ei6cjTx%2FwSDxae307fULElAhFUUQyJn9VSenQj5LoqJJC0rQIN93UDJ9OQOOjdEUoZF4s1vFx9pQdxXnQVaLyIRSpIs7DFNhEKddwKUioXc%2F3jdsKauunGM%2Fq6Rw1HRWymwBSbggG%2FXbPUSYSJoH7Hr39jZ3UlRuehuOLmQZmbDndw6fuaDtq--QubxNrIrwFywBl80--27XuIPNf%2F9AGfkVs%2BrCvXg%3D%3D'
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
    owner = 'ultralytics'
    repo = 'ultralytics'

    # GitHub GraphQL API URL
    graphql_url = 'https://api.github.com/graphql'
    # 设置请求头，包括认证信息和内容类型
    headers = {
        'Authorization': f'bearer {token}',
        'Content-Type': 'application/json'
    }
    first_count = 100
    after = None
    all_commits = []

    # GraphQL查询
    while True:
        query = """
        query($repoName: String!, $owner: String!, $after: String) {
          repository(owner: $owner, name: $repoName) {
            defaultBranchRef {
              target {
                ... on Commit {
                  history(first: %d, after: $after) {
                    edges {
                      node {
                        commitUrl
                        messageHeadline
                        author {
                          avatarUrl
                          name
                        }
                        committedDate
                      }
                    }
                    pageInfo {
                      endCursor
                      hasNextPage
                    }
                  }
                }
              }
            }
          }
        }
        """ % first_count

        variables = {
            'repoName': repo,
            'owner': owner,
            'after': after
        }
        response = requests.post(graphql_url, headers=headers,
                                 data=json.dumps({'query': query, 'variables': variables}))

        # 检查响应状态码
        response.raise_for_status()

        # 解析响应内容
        data = response.json()

        # 获取当前页面的提交
        commits = data['data']['repository']['defaultBranchRef']['target']['history']['edges']
        all_commits.extend(commits)  # 添加到总列表

        # 获取分页信息
        pageInfo = data['data']['repository']['defaultBranchRef']['target']['history']['pageInfo']

        # 检查是否有下一页
        if pageInfo['hasNextPage']:
            after = pageInfo['endCursor']  # 更新游标
        else:
            break  # 没有下一页，退出循环
    # 打印所有提交信息
    commit_count = 0
    for commit in all_commits:
        commit_count += 1
        print(f"Commit{commit_count}:")
        print(f"Commit Message: {commit['node']['messageHeadline']}")
        print(f"Commit Author: {commit['node']['author']['name']}")
        print(f"Author Avatar: {commit['node']['author']['avatarUrl']}")
        print(f"Commit Date: {commit['node']['committedDate']}")
        print(f"Commit URL: {commit['node']['commitUrl']}")
        print('------')
    commit_counts_dir = {author: sum(1 for c in all_commits if c['node']['author']['name'] == author) for author in
                     set([c['node']['author']['name'] for c in all_commits])}
    plt.bar(commit_counts_dir.keys(), commit_counts_dir.values())
    plt.xlabel('Author')
    plt.ylabel('Commit Count')
    plt.title('Commits by Author')
    plt.show()
    # # 解析响应内容
    # data = response.json()
    #
    # # 打印提交记录信息
    # commits = data['data']['repository']['defaultBranchRef']['target']['history']['edges']
    # for commit in commits:
    #     print(f"Commit Message: {commit['node']['messageHeadline']}")
    #     print(f"Commit Author: {commit['node']['author']['name']}")
    #     print(f"Author Avatar: {commit['node']['author']['avatarUrl']}")
    #     print(f"Commit Date: {commit['node']['committedDate']}")
    #     print(f"Commit URL: {commit['node']['commitUrl']}")
    #     print('------')


    # query
    # {
    #     user(login: "username") {
    #     name
    #     login
    #     avatarUrl
    # }
    # }
    # response = requests.post(url, headers=headers, data=json.dumps(query))
    # user_info = response.json()

    # print(user_info)
    # response = requests.get(url=url, headers=headers)
    # response.raise_for_status()
    # html = response.text
    # print(html)
    # soup = BeautifulSoup(html, 'html.parser')

    # h3_tags = soup.find_all('h3',class_="text-normal f5 py-1 prc-Heading-Heading-6CmGO")
    # h3_tags_content=[]
    # for tag in h3_tags:
    #     # 打印<h3>标签的文本内容
    #     h3_tags_content.append(tag.get_text())
    #     print(tag.get_text())
    #     print('\n')
    #
    # # 遍历h3_tags_content列表，提取日期并转换
    # print(h3_tags_content)
    # time_commit_map={}
    # for item in h3_tags_content:
    #     # 使用字符串方法split()来分割字符串，并提取日期部分
    #     # _,parts = item.split('on ')
    # # 如果这个日期已经在字典中，增加其计数，否则添加到字典中，并设置计数为1
    #     if item in time_commit_map:
    #        pass
    #     else:
    #         time_commit_map[item] = 0
    #
    # ul_tags = soup.find_all('div',class_='ListView-module__container--zF6wW')
    # i = 0
    # for ul_tag in ul_tags:
    #     # 提取<ul>标签下的所有<li>标签
    #     li_tags = ul_tag.find_all('h4')
    #     # 遍历<li>标签并打印它们的文本内容
    #     for li in li_tags:
    #         time_commit_map[h3_tags_content[i]]+=1
    #         print(li.get_text())
    #     print('\n')
    #     i+=1
    # print(time_commit_map)

    # print(html)
def parse_date(date_str):
    # 定义月份的映射关系
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    # 分割字符串，提取日期部分
    parts = date_str.split()
    # 提取月份名称和日期数字，并去除逗号
    month_name = parts[0]
    day = int(parts[1].replace(',', ''))
    year = parts[2]
    # 将月份名称转换为数字
    month_num = month_map[month_name]
    # 将日期字符串转换为datetime对象
    return datetime(int(year), month_num, day)


if __name__ == "__main__":
    # generate_cloud("s")
    # spider_issues()
    generate_time_seq()
