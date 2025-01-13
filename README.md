# 开源软件基础大作业

这是一个对GitHub仓库中commit和issue信息的分析和展示的程序。
## Commit信息分析
Commit信息分析主要围绕该项目的提交记录进行分析，同时本项目封装了两种分析对象，分别是作者和日期。
- **选择作者为分析对象**：可以获得不同作者对该项目的提交记录次数关系，以此反映贡献度。
- **选择日期为分析对象**：可以获得不同日期和提交记录次数的关系，以此可以推测该项目的开发时间线且根据提交次数来确定关键时间轴。
与此同时，项目中封装了筛选功能，用户可以输入筛选的值来过滤爬取的值，只保留大于阈值的值用于分析。
## Issue信息分析
Issue信息分析主要围绕该项目的问题栏进行分析，包括对问题类别的归类以及对问题解决效率的分析。
- **问题类别归类**：爬取到问题后，对每个问题按照标签进行分类，获得对应频率并基于此生成词云，来得到该项目主要讨论问题的类别。
- **问题解决效率分析**：将爬取到的问题信息根据创建时间和关闭时间得到时间差，用于表示问题的解决时间，并以此按照预先设定不同时间长短来生成该项目所有问题解决时间的饼状图。
## 使用技术
在使用技术方面，本项目采用以下技术：
- **PyQt5**：用于搭建GUI。
- **Matplotlib**：用于生成图表。
- **WordCloud**：用于生成词云。
# 项目依赖
以下是本项目所使用的Python依赖：
## 标准库
- `collections`：用于`defaultdict`。
- `datetime`：用于日期和时间相关操作。
## 第三方库
- `json`：用于处理JSON数据。
- `PyQt5`：
    - `PyQt5.QtCore`：包含`QThread`和`pyqtSignal`，用于多线程和信号槽机制。
    - `PyQt5.QtWidgets`：包含`QApplication`、`QWidget`、`QMainWindow`、`QFileDialog`、`QMessageBox`等，用于构建图形用户界面。
    - `PyQt5.QtGui`：包含`QIntValidator`，用于输入验证。
- `bs4`：包含`BeautifulSoup`，用于HTML和XML文件的解析。
- `requests`：用于发送HTTP请求。
- `re`：用于正则表达式操作。
- `certifi`：提供证书数据，用于验证HTTPS请求。
- `matplotlib`：
    - `matplotlib.pyplot`：用于绘制图表。
    - `matplotlib`：基础绘图库。
- `wordcloud`：包含`WordCloud`，用于生成词云。
- `home`：包含`Ui_home`，可能是项目中自定义的界面模块。
