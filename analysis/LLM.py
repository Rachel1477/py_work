import json
import sys
from text2vec import SentenceModel, cos_sim
import numpy as np
from ollama import chat

# 加载中文句向量模型
embedder = SentenceModel("shibing624/text2vec-base-multilingual")

# 加载岗位数据
DATA_PATH = '/packages/py_work/FlaskProject/data/实习岗位数据.json'
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    job_data = json.load(f)

# 为每条岗位构造一个简洁文本描述用于 embedding
job_texts = [
    rec.get("企业名称", "") + rec.get("岗位名称", "") + rec.get("工作要求", "")+rec.get("薪资范围","")
    for rec in job_data
]
job_embeddings = embedder.encode(job_texts, normalize_embeddings=True)

# 检索函数：找最相似的前 K 条
def semantic_search(query: str, top_k=10):
    query_emb = embedder.encode([query], normalize_embeddings=True)
    scores = cos_sim(query_emb, job_embeddings)[0]
    top_indices = np.argsort(-scores)[:top_k]
    return [job_data[i] for i in top_indices]

# System prompt 模板
SYSTEM_TEMPLATE = """你是一个职业咨询顾问，请根据以下实习岗位数据，帮助用户解答与岗位匹配相关的问题。
请严格基于以下信息进行回答：
{snippet}
"""

def ask_llm(query: str) -> str:
    relevant = semantic_search(query, top_k=3)
    snippet = json.dumps(relevant, ensure_ascii=False, indent=2)
    system_prompt = SYSTEM_TEMPLATE.format(snippet=snippet)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    response = chat(model="qwen:7b", messages=messages, stream=False)
    return response.message.content

if __name__ == '__main__':
    print("请输入问题（输入 exit 退出）：")
    while True:
        user_input = input("用户：").strip()
        if user_input.lower() in ('exit', 'quit'):
            break
        answer = ask_llm(user_input)
        print("助手：", answer)
