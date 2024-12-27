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

# 设置GitHub的 GraphQL API 端点
graphql_url = "https://api.github.com/graphql"


# 设置请求头
headers = {
    "Authorization": f"Bearer tok",
    "Content-Type": "application/json"
}

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


# 分页请求的函数
def fetch_issues(owner, repo, first=100):
    issues = []
    after_cursor = None

    while True:
        # GraphQL 查询变量
        variables = {
            "owner": owner,
            "repo": repo,
            "first": first,
            "after": after_cursor
        }

        response = requests.post(graphql_url, json={'query': query, 'variables': variables}, headers=headers,verify=False)

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
            break

    return issues

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

# 生成词云图
def generate_wordcloud(label_counts):
    # 创建词云对象
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(label_counts)

    # 显示词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('pie_chart.png', format='png')
    print("词云图绘制完毕")
# 打印结果
def print_issues(issues):
    for issue in issues:
        print(f"Title: {issue['title']}")
        print(f"Number: #{issue['number']}")
        print(f"Created At: {issue['createdAt']}")
        print(f"Closed At: {issue['closedAt']}")
        print(f"Body: {issue['body'][:200]}...")  # 仅显示前200个字符
        print("-" * 80)
        labels = [label['name'] for label in issue['labels']['nodes']]
        if labels:
            print(f"Labels: {', '.join(labels)}")
        else:
            print("Labels: None")
        print("-" * 80)


# 计算时间差并分类
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


# 生成饼状图
def generate_pie_chart(categories):
    labels = categories.keys()
    sizes = categories.values()

    # 画饼状图
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    plt.title('Time to Resolve Issues')
    plt.axis('equal')  # 让饼图为圆形
    plt.savefig('bing.png', format='png')


# 主函数
if __name__ == "__main__":
    # 设置目标仓库的 owner 和 repo 名称
    owner = "ultralytics"  # GitHub 用户名或组织名
    repo = "ultralytics"  # 仓库名
    issues = fetch_issues(owner, repo)

    # 打印获取到的 issues 信息
    print_issues(issues)
    # 提取标签并统计频率
    label_counts = extract_labels(issues)

    # 生成并显示词云图
    generate_wordcloud(label_counts)
    # 计算时间差并分类
    categories = calculate_time_diff_and_classify(issues)

    # 生成饼状图
    generate_pie_chart(categories)
