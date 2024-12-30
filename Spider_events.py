from collections import defaultdict
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
import requests
import json
from PyQt5.QtCore import QThread, pyqtSignal

class SpiderThread(QThread):
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)  # 添加错误信号

    def __init__(self, owner, repo, token):
        super().__init__()
        self.is_running = True
        self.owner = owner
        self.repo = repo
        self.token = token

    def run(self):
        try:
            headers = {
                'Authorization': f'bearer {self.token}',
                'Content-Type': 'application/json'
            }
            graphql_url = 'https://api.github.com/graphql'
            first_count = 100
            after = None
            all_commits = []

            # 获取总提交数的查询
            total_query = """
                          query($repoName: String!, $owner: String!) {
                            repository(owner: $owner, name: $repoName) {
                              defaultBranchRef {
                                target {
                                  ... on Commit {
                                    history(first: 1) {
                                      totalCount
                                    }
                                  }
                                }
                              }
                            }
                          }
                        """

            total_variables = {
                'repoName': self.repo,
                'owner': self.owner,
            }

            # 发送查询以获取总提交数
            total_response = requests.post(graphql_url, headers=headers,
                                           data=json.dumps({'query': total_query, 'variables': total_variables}),
                                           verify=False)
            if total_response.status_code == 401:
                self.error_occurred.emit("Token验证失败，请检查您的访问令牌是否正确")
                return


            if total_response.status_code != 200:
                self.error_occurred.emit(f"请求失败: {total_response.status_code}\n{total_response.text}")
                return
            total_data = total_response.json()
            if total_data.get('data') and total_data['data'].get('repository')==None:
                self.error_occurred.emit("未找到仓库数据，请检查仓库名称和所有者是否正确")
                return

            total_commits = total_data['data']['repository']['defaultBranchRef']['target']['history']['totalCount']

            # GraphQL查询
            while self.is_running:
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
                    'repoName': self.repo,
                    'owner': self.owner,
                    'after': after
                }

                response = requests.post(graphql_url, headers=headers,
                                         data=json.dumps({'query': query, 'variables': variables}), verify=False)

                if response.status_code == 401:
                    self.error_occurred.emit("Token验证失败，请检查您的访问令牌是否正确")
                    break

                if response.status_code != 200:
                    self.error_occurred.emit(f"请求失败: {response.status_code}\n{response.text}")
                    break

                data = response.json()
                if data.get('data') and data['data'].get('repository')==None:
                    self.error_occurred.emit("未找到仓库数据，请检查仓库名称和所有者是否正确")
                    break
                commits = data['data']['repository']['defaultBranchRef']['target']['history']['edges']
                all_commits.extend(commits)  # 添加到总列表
                pageInfo = data['data']['repository']['defaultBranchRef']['target']['history']['pageInfo']

                if pageInfo['hasNextPage']:
                    self.progress_updated.emit(int((len(all_commits) + first_count) / total_commits * 100))  # 发送进度更新信号
                    after = pageInfo['endCursor']  # 更新游标
                else:
                    self.progress_updated.emit(100)
                    break
                    # 没有下一页，退出循环
            self.result_ready.emit(all_commits)

        except requests.exceptions.Timeout:
            self.error_occurred.emit("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            self.error_occurred.emit("网络连接错误，请检查网络状态")
        except Exception as e:
            self.error_occurred.emit(f"发生未知错误: {str(e)}")




class SpiderThread2(QThread):
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)  # 添加错误信号

    def __init__(self, owner, repo, token):
        super().__init__()
        self.is_running = True
        self.owner = owner
        self.repo = repo
        self.token = token
    def run(self):
        try:
            graphql_url = "https://api.github.com/graphql"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            query = """
                     query ($owner: String!, $repo: String!) {
                       repository(owner: $owner, name: $repo) {
                         issues(states: CLOSED) {
                           totalCount
                         }
                       }
                     }
                     """

            variables = {
                "owner": self.owner,
                "repo": self.repo
            }

            # 验证token
            try:
                response = requests.post(graphql_url, json={'query': query, 'variables': variables}, 
                                      headers=headers, verify=False, timeout=10)  # 添加超时设置

                if response.status_code == 401:
                    self.error_occurred.emit("Token验证失败，请检查您的访问令牌是否正确")
                    return
                    
                if response.status_code != 200:
                    self.error_occurred.emit(f"请求失败: {response.status_code}\n{response.text}")
                    return
                data = response.json()
                if data.get('data') and data['data'].get('repository') == None:
                    self.error_occurred.emit("未找到仓库数据，请检查仓库名称和所有者是否正确")
                    return
            except requests.exceptions.Timeout:
                self.error_occurred.emit("请求超时，请检查网络连接")
                return
            except requests.exceptions.ConnectionError:
                self.error_occurred.emit("网络连接错误，请检查网络状态")
                return



            issues_count = data.get("data", {}).get("repository", {}).get("issues", {}).get("totalCount", 0)
            # GraphQL 查询语句：获取仓库中的已关闭的 Issues
            query = """
                    query ($owner: String!, $repo: String!, $first: Int!, $after: String) {
                      repository(owner: $owner, name: $repo) {
                        issues(first: $first, after: $after, states: CLOSED) {
                          nodes {
                            title
                            number
                            createdAt
                            closedAt
                            body
                            labels(first: 10) {
                              nodes {
                                name
                              }
                            }
                          }
                          pageInfo {
                            hasNextPage
                            endCursor
                          }
                        }
                      }
                    }
                    """

            issues = []
            after_cursor = None

            while self.is_running==True:
                # GraphQL 查询变量
                variables = {
                    "owner": self.owner,
                    "repo": self.repo,
                    "first": 100,
                    "after": after_cursor
                }

                try:
                    response = requests.post(graphql_url, json={'query': query, 'variables': variables}, 
                                          headers=headers, verify=False, timeout=10)
                    
                    if response.status_code != 200:
                        self.error_occurred.emit(f"获取数据失败: {response.status_code}\n{response.text}")
                        break

                    data = response.json()
                    if data.get('data') and data['data'].get('repository') == None:
                        self.error_occurred.emit("未找到仓库数据，请检查仓库名称和所有者是否正确")
                        return

                    # 获取当前页的issues
                    issues_data = data.get("data", {}).get("repository", {}).get("issues", {}).get("nodes", [])

                    if not issues_data:
                        print("No issues found.")
                        break

                    # 将当前页的 issues 添加到 issues 列表
                    issues.extend(issues_data)

                    # 获取分页信息
                    page_info = data.get("data", {}).get("repository", {}).get("issues", {}).get("pageInfo", {})
                    has_next_page = page_info.get("hasNextPage", False)
                    after_cursor = page_info.get("endCursor", None)

                    # 如果没有下一页，退出循环
                    if not has_next_page:
                        self.progress_updated.emit(100)
                        break
                    else :
                        self.progress_updated.emit(int((len(issues) + 100) /issues_count * 100))  # 发送进度更新信号

                except requests.exceptions.Timeout:
                    self.error_occurred.emit("请求超时，请检查网络连接")
                    break
                except requests.exceptions.ConnectionError:
                    self.error_occurred.emit("网络连接错误，请检查网络状态")
                    break

            self.result_ready.emit(issues)
        except Exception as e:
            self.error_occurred.emit(f"发生未知错误: {str(e)}")
    # 分页请求的函数



