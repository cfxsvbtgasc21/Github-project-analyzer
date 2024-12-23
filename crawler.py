import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from models import Commit, Repository

class GitHubCrawler:
    def __init__(self):
        self.session = requests.Session()           # 初始化requests会话，用于保持会话状态
        self.headers = {                            # 设置HTTP请求头，模拟浏览器访问
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
    
    def parse_number(self, text: str) -> int:
        """解析包含k、m等单位的数字"""
        try:
            # 移除所有空白字符和'stars'等文本
            text = (text.strip()
                      .lower()
                      .replace('stars', '')
                      .replace(',', '')
                      .replace('\n', '')
                      .strip())
            multiplier = 1
            if 'k' in text:
                multiplier = 1000
                text = text.replace('k', '')
            elif 'm' in text:
                multiplier = 1000000
                text = text.replace('m', '')
            return int(float(text) * multiplier)
        except Exception as e:
            print(f"数字解析错误: {text} - {str(e)}")
            return 0
    
    def get_repository_info(self, repo_url: str) -> Repository:
        try:
            print("执行url分析")
            if not repo_url.startswith('https://github.com/'):
                raise ValueError('请输入有效的GitHub仓库URL')
                
            response = self.session.get(repo_url, headers=self.headers)
            if response.status_code != 200:
                raise Exception(f'HTTP错误: {response.status_code}')
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            file_path = 'repository_page.html'  # 你可以修改文件路径和文件名

            if isinstance(response.text, bytes):
                response.text = response.text.decode('utf-8')
            # 打开文件并写入 HTML 内容
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)

            print(f"HTML内容已保存到 {file_path}")
            print(response.text)
            try:
                # 获取仓库名称
                full_name = soup.select_one('strong[itemprop="name"] a').text.strip()
                name = full_name.split('/')[-1] if '/' in full_name else full_name
                print("获取仓库名称：",name)
                
                # 获取作者名称
                owner = repo_url.split('/')[-2]
                
                stars = 0
                forks = 0
                
                # 方法1：通过新的ID选择器
                stars_element = soup.select_one('#repo-stars-counter-star')
                forks_element = soup.select_one('#repo-network-counter')
                
                if stars_element and forks_element:
                    #forks = self.parse_number(forks_element.text)
                    print("方法一：ID选择器输出")
                    #stars_element = soup.find('span', id='repo-stars-counter-star')
                    # 检查是否找到了元素，并提取aria-label属性中的数字
                    if stars_element and 'title' in stars_element.attrs:
                        stars= stars_element['title']
                        print("提取的数字:", stars)
                    if forks_element and 'title' in forks_element.attrs:
                        forks = forks_element['title']
                        print("提取的数字:", forks)
                else:
                    # 方法2：通过社交计数器类
                    social_counts = soup.select('span.Counter')
                    if social_counts:
                        stars = self.parse_number(social_counts[0].text if len(social_counts) > 0 else '0')
                        forks = self.parse_number(social_counts[1].text if len(social_counts) > 1 else '0')
                        print("方法二：社交计数器类输出")
                    else:
                        # 方法3：通过链接文本
                        stars_link = soup.select_one('a[href$="/stargazers"]')
                        forks_link = soup.select_one('a[href$="/forks"]')
                        if stars_link:
                            stars = self.parse_number(stars_link.text)
                        if forks_link:
                            forks = self.parse_number(forks_link.text)
                        print("方法三：链接文本输出")

                print(f"解析结果: {stars,forks}")
                
            except Exception as e:
                print(f"解析错误: {str(e)}")
                stars = 0
                forks = 0
            
            return Repository(
                name=name,
                owner=owner,
                stars=stars,
                forks=forks,
                commits=[],
                contributors=[]
            )
            
        except Exception as e:
            raise Exception(f"获取仓库信息失败: {str(e)}")