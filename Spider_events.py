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
class SpiderThread(QThread):
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(list)
    def __init__(self,owner,repo,token):
        super().__init__()
        self.is_running = True
        self.owner=owner
        self.repo=repo
        self.token=token
    def run(self):
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
        total_response.raise_for_status()
        total_data = total_response.json()
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
                self.progress_updated.emit(int((len(all_commits) + first_count) / total_commits * 100))  # 发送进度更新信号
                after = pageInfo['endCursor']  # 更新游标
            else:
                self.progress_updated.emit(100)
                break
                # 没有下一页，退出循环
        # 打印所有提交信息
        if self.is_running:
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
            self.result_ready.emit(all_commits)



class SpiderThread2(QThread):
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(list)
    def __init__(self, owner, repo, token):
        super().__init__()
        self.is_running = True
        self.owner = owner
        self.repo = repo
        self.token = token
    def run(self):
        graphql_url = "https://api.github.com/graphql"
        # 设置请求头
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

        response = requests.post(graphql_url, json={'query': query, 'variables': variables}, headers=headers,
                                 verify=False)

        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            print("Response text:", response.text)
            return None

        data = response.json()
        if 'data' not in data or not data['data']:
            print("No data found in the response.")
            print("Response JSON:", json.dumps(data, indent=2))
            return None

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

            response = requests.post(graphql_url, json={'query': query, 'variables': variables}, headers=headers,
                                     verify=False)

            if response.status_code != 200:
                print(f"Error fetching data: {response.status_code}")
                print("Response text:", response.text)  # 打印错误响应的内容
                break
            data = response.json()
            if 'data' not in data or not data['data']:
                print("No data found in the response.")
                print("Response JSON:", json.dumps(data, indent=2))  # 打印返回的完整 JSON 数据
                break

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

        self.result_ready.emit(issues)
    # 分页请求的函数


