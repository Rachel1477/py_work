第四版 5月5日 余洋 flaskproject
-----------我完成了什么--------------
1.对爬取的数据进行清洗，包括多格式薪资解析（区间／单值／中文数字），并计算平均薪资；文本清洗：剔除特殊字符、低长度词；提取“福利”“要求”“城市”等字段。

2.数据分析和可视化
2-1.“职位要求”和“福利待遇”关键词词云图（文字越大表示该词汇出现的越频繁）
2-2.城市×学历  的平均薪资热力图，表示两者之间的相关性
2-3.统计了城市x岗位数量的关系，并用柱状图（带数据标签）可视化
2-4.计算和分析了不同学历下薪资对比，并用箱形图的方式可视化
2-5.绘制日薪分布小提琴图

3.增强型聚类分析 (enhanced_clustering)
TF‑IDF 向量化“要求_clean”，KMeans 分 4 类；每簇词云可视化；各簇薪资箱型图对比。
这一步的目的是分析多个影响因子对于薪资的关系，而上面的2部分都是单因子分析

4.薪资预测建模
对于每个类别特征独热编码；
使用随机森林回归算法拟合薪资；
输出前 15 个最重要特征并可视化。

5.本地部署了大语言模型（本地部署的意思是没有使用第三方API，模型完完全全保存在本地），支持上下文，同时使用了RAG“Retrieval‑Augmented Generation”（检索增强生成）
把爬虫数据输入到大语言模型中，模型被设置为严格按照爬虫数据回答。经测试已经能够正常对话


-----------用到了什么python库--------------
（下面的点与上述分点一一对应）
1.Python 标准库 re  |   numpy   |   pandas

2.
绘图部分采用的都是matplotlib.pyplot
2-1.wordcloud：生成词云图，展示文本中高频关键词
2-2.matplotlib.pyplot
2-3.matplotlib.pyplot
2-4.matplotlib.pyplot
2-5.matplotlib.pyplot

3.（下面的sklearn是是一个基于Python 的开源机器学习库，提供了丰富、统一、易用的工具来完成从数据预处理到模型训练、评估和预测的全流程。下面是用到的内部函数）
sklearn.cluster.KMeans：K‑Means 聚类算法，实现文本特征的无监督分组。
sklearn.feature_extraction.text.TfidfVectorizer：TF‑IDF 文本向量化，将“职位要求”转为数值特征。
wordcloud：生成词云图，展示文本中高频关键词。

4.
sklearn.preprocessing.OneHotEncoder：对“城市”“学历”“聚类标签”等类别特征做独热编码。
sklearn.ensemble.RandomForestRegressor：随机森林回归模型，用于薪资预测与特征重要性评估。
sklearn.metrics.r2_score, mean_squared_error：模型评估指标，计算 R² 和均方误差。

5.text2vec 是一个开源的 Python 库，旨在简化将文本转换为数值向量的过程，方便在下游的机器学习、深度学习或相似度检索任务中使用。它封装了多种预训练的文本嵌入（embedding）模型，以及常用的相似度计算函数。
text2vec.SentenceModel	加载并使用多语言句向量模型，将文本编码为向量
text2vec.cos_sim	计算向量之间的余弦相似度，用于衡量查询与岗位描述的语义相似度
Ollama                  是一个本地化／私有化部署的“聊天式大模型”推理引擎与管理工具，用于向LLM发送问题和接收LLM的回复

大语言模型采用的是qwen:7b
