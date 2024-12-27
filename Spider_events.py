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

