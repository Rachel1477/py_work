# internship_analysis_enhanced.py
# 增强版数据分析及可视化脚本

import json
import re
import os
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 必须在导入 pyplot 之前设置
from matplotlib import pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# --- 全局配置 ---
warnings.filterwarnings("ignore")


plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']   # 指定默认中文字体
plt.rcParams['axes.unicode_minus'] = False               # 解决负号 ‘−’ 显示为方块
#sns.set_theme(style="whitegrid", palette="pastel")  # 设置Seaborn主题

# 1. 数据预处理（优化版）
def load_data(filepath: str) -> pd.DataFrame:
    """加载并初步处理数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df

def parse_salary(s: str):
    """增强型薪资解析，处理更多格式"""
    patterns = [
        r"(\d+)-?(\d+)?/?天",      # 原有格式
        r"(\d+)元/?天",            # 新增格式处理
        r"([一二三四五六七八九十]+)千?/天"  # 中文数字处理
    ]
    for pattern in patterns:
        m = re.match(pattern, s)
        if m:
            if pattern == patterns[2]:  # 中文数字处理
                cn_num = {'一':1, '二':2, '三':3, '四':4, '五':5,
                         '六':6, '七':7, '八':8, '九':9, '十':10}
                num = cn_num.get(m.group(1), 0)*1000
                return num, num, num
            else:
                lo = int(m.group(1))
                hi = int(m.group(2)) if m.group(2) else lo
                return lo, hi, (lo+hi)/2
    return np.nan, np.nan, np.nan

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """增强型数据清洗"""
    # 薪资处理
    df[['sal_min','sal_max','sal_avg']] = df['薪资范围'].apply(
        lambda x: pd.Series(parse_salary(x))
    )
    df = df.dropna(subset=['sal_avg']).reset_index(drop=True)
    
    # 学历处理
    LEVEL_MAP = {"不限":"不限", "本科":"本科", "大专":"大专", 
                "硕士":"硕士", "博士":"博士", "无要求":"不限"}
    df['学历要求'] = df['学历要求'].str.extract(r'(\w{2})')[0].map(LEVEL_MAP).fillna('不限')
    
    # 文本处理
    def clean_text(text):
        text = re.sub(r'[^\u4e00-\u9fa5A-Za-z0-9]', ' ', text)
        return ' '.join([w for w in text.split() if len(w) > 1])
    
    df['福利_clean'] = df['福利'].apply(clean_text)
    df['要求_clean'] = df['工作要求'].apply(clean_text)
    df['要求_clean'] = df['要求_clean'].str.slice(start=4)
    df['城市'] = df['工作地点'].str.split().str[0].str.replace('市','')
    return df

# 2. 可视化模块（新增多种图表类型）
def create_combined_plot(df: pd.DataFrame, outdir='static/figures'):
    """将分析图分别保存为四张图"""
    os.makedirs(outdir, exist_ok=True)

    # 1. 薪资分布小提琴图
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.violinplot(x='sal_avg', data=df, ax=ax, inner="quartile", palette="YlOrRd")
    ax.set_title('日薪分布小提琴图', fontsize=12)
    ax.set_xlabel('日薪（元）')
    plt.tight_layout()
    plt.savefig(f'{outdir}/plot_violin.png', dpi=300)
    plt.close()

    # 2. 学历-薪资关系箱型图
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='学历要求', y='sal_avg', data=df, 
                order=['大专', '本科', '硕士', '博士'], palette="Set2", ax=ax)
    ax.set_title('不同学历薪资对比', fontsize=12)
    ax.set_xlabel('')
    ax.set_ylabel('日薪（元）')
    plt.tight_layout()
    plt.savefig(f'{outdir}/plot_box.png', dpi=300)
    plt.close()

    # 3. 城市岗位数TOP10（带数据标签）
    top_cities = df['城市'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=top_cities.values, y=top_cities.index, palette="Blues_d", ax=ax)
    ax.set_title('热门城市岗位分布TOP10', fontsize=12)
    ax.set_xlabel('岗位数量')
    label_offset = max(top_cities.values) * 0.02  # 设置为柱子长度的2%
    for i, v in enumerate(top_cities.values):
        ax.text(v + label_offset, i, str(v), color='blue', va='center')
    plt.tight_layout()
    plt.savefig(f'{outdir}/plot_top_cities.png', dpi=300)
    plt.close()

    # 4. 城市-学历薪资热力图
    heat_df = df.groupby(['城市', '学历要求'])['sal_avg'].mean().unstack().fillna(0)
    heat_df = heat_df.loc[top_cities.index].dropna(how='all')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heat_df, annot=True, fmt=".0f", cmap="YlGnBu", 
                ax=ax, cbar_kws={'label': '平均日薪（元）'})
    ax.set_title('城市-学历薪资热力图', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'{outdir}/plot_heatmap.png', dpi=300)
    plt.close()

def generate_wordcloud(text_series: pd.Series, title: str, outdir='static/figures'):
    """生成词云图"""
    os.makedirs(outdir, exist_ok=True)
    text = ' '.join(text_series.tolist())
    
    wc = WordCloud(
        font_path='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # 确保中文字体路径正确
        width=800,
        height=600,
        background_color='white',
        max_words=200,
        collocations=False
    ).generate(text)
    
    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.title(f'"{title}"关键词词云', fontsize=14)
    plt.axis('off')
    plt.savefig(f'{outdir}/{title}_wordcloud.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. 增强型聚类分析
def enhanced_clustering(df: pd.DataFrame, n_clusters=4):
    """带可视化效果的聚类分析"""
    vec = TfidfVectorizer(max_features=500, stop_words=['具有','具备','优先','相关'])
    X = vec.fit_transform(df['要求_clean'])
    km = KMeans(n_clusters=n_clusters, random_state=42).fit(X)
    df['cluster'] = km.labels_
    
    # 可视化每个簇的关键词
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    for idx, ax in enumerate(axes.flatten()):
        if idx >= n_clusters:
            break
        # 提取每个簇的关键词
        cluster_text = ' '.join(df[df['cluster']==idx]['要求_clean'])
        wc = WordCloud(
            font_path='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            width=400,
            height=300,
            background_color='white',
            max_words=50
        ).generate(cluster_text)
        ax.imshow(wc)
        ax.set_title(f'Cluster {idx} 关键词词云', fontsize=10)
        ax.axis('off')
    plt.savefig('static/figures/cluster_wordclouds.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 各簇薪资对比
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='cluster', y='sal_avg', data=df, palette="Set3")
    plt.title('各能力簇薪资对比')
    plt.xlabel('能力簇')
    plt.ylabel('日薪（元）')
    plt.savefig('static/figures/cluster_salary.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return df, vec, km

# 4. 增强型预测模型（带特征重要性分析）
def enhanced_modeling(df: pd.DataFrame):
    """带可视化的建模分析"""
    enc = OneHotEncoder(sparse_output=False)
    X_meta = enc.fit_transform(df[['城市','学历要求','cluster']])
    y = df['sal_avg'].values
    
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_meta, y)
    
    # 特征重要性可视化
    features = []
    categories = enc.categories_
    for i, cat in enumerate(['城市','学历','能力簇']):
        features.extend([f"{cat}_{name}" for name in categories[i]])
    
    importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False).head(15)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=importance, palette="viridis")
    plt.title('薪资影响因素TOP15')
    plt.xlabel('特征重要性')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('static/figures/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return model, enc

# 5. 主流程
def main():
    # 数据准备
    df = load_data('/packages/py_work/FlaskProject/data/实习岗位数据.json')
    df = preprocess(df)
    
    # 可视化分析
    create_combined_plot(df)
    generate_wordcloud(df['要求_clean'], '职位要求')
    generate_wordcloud(df['福利_clean'], '福利待遇')
    
    # 聚类分析
    df, vec, km = enhanced_clustering(df, n_clusters=4)
    
    # 建模分析
    model, enc = enhanced_modeling(df)
    
    print("分析完成，结果已保存至 figures/ 目录")

if __name__ == '__main__':
    main()