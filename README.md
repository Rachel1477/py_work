# 大学生实习招聘市场分析系统

## 项目名称
**大学生实习招聘市场分析系统**  
**开发团队**：余洋、余俊豪、马兴元、骆凯、潘睿磊   

---
##  技术栈
- **数据爬取**：Requests + BeautifulSoup + 随机延迟反爬策略  
- **后端框架**：Flask + MySQL + pymysql  
- **数据分析**：Pandas + NumPy + Scikit-learn（KMeans聚类、随机森林回归）  
- **可视化**：Matplotlib + Seaborn + WordCloud  
- **前端界面**：HTML/CSS + Bootstrap4 + JavaScript  
- **智能助手**：本地部署Qwen-7B模型 + RAG技术 + text2vec  

---
##  核心功能
1. **数据爬取**  
   - 分页爬取岗位信息（薪资、技能要求、企业类型等）  
   - 反爬策略：随机延迟、User-Agent伪装、Unicode薪资解码  
   - 数据存储：JSON/CSV + MySQL数据库  

2. **数据分析与可视化**  
   - 多维度图表：词云图（高频技能/福利）、热力图（城市×学历薪资）、箱型图（薪资分布）  
   - 聚类分析：基于岗位要求划分技术类/运营类岗位簇  
   - 薪资预测：随机森林模型量化学历、城市对薪资的影响  

3. **智能分析助手**  
   - 自然语言查询 
   - RAG技术实现基于本地数据的精准回答  
   - 个性化推荐：结合用户背景生成实习建议  

4. **交互界面**  
   - 响应式前端：主界面/爬取页/分析页无缝切换  
   - 实时反馈：爬取加载动画、可视化图表动态展示  

# 部署
## ---本地部署
1.安装依赖

首先确保你已经安装了minconda，并可以正常使用。本项目提供了一个requirements.txt，你可以通过它安装相关的依赖
```
conda create -n py python=3.8
conda activate py
```
2.下载LLM的预训练权重

本项目使用的是Qwen-7B，你可以在huggingface上找到对应的权重并下载，下载链接在[这里](https://huggingface.co/Qwen/Qwen-7B)

3.下载ollama

Ollama 是一个轻量级的本地大语言模型（LLM）运行平台，它让你可以非常方便地在本地运行大语言模型

- for windows：
点击[这里](https://ollama.com/)下载 安装包，然后直接安装
- for linux：
运行以下指令
```
curl -fsSL https://ollama.com/install.sh | sh
```

下载好之后，你可以通过
```
ollama run qwen:7b
```
的方式检查预训练权重和ollama是否都正常工作

4.下载好mysql，并按如下设置
   - 'user': 'root',
   - 'password': 'rachel1211',
   - 'database': 'internship_db'

或者你可以手动修改sql目录里的内容
## --容器部署
如果你不想下载依赖，或者在部署时出了无法解决的问题，本项目也提供docker部署，对应的docker image已经上传到dockerhub

你可以运行下面的命令把项目的image 从dockerhub上pull到本地
```
docker pull shuanghua0912/python_work:v1
```
(注意：dockerhub需要翻墙才可以访问)

因为LLM需要使用GPU，所以确保你的docker支持nvidia，或者下载nvidia-docker

通过如下命令运行容器
```
docker run -it --gpus all --network host python_work:latest bash
```

# 启动
激活conda环境后运行
```
python app.py
```
在服务器开启之后，用浏览器打开 http://127.0.0.1:3389 即可访问