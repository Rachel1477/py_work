import random
import requests
from bs4 import BeautifulSoup
import json
import time
import os
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


def detail_url(url, job_data):
    try:
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        title = soup.title.text
        job = title.split("招聘")[0]
        company_name = soup.select('.com_intro .com-name')[0].text.strip()
        address = soup.select('.job_position')[0].text.strip()
        academic = soup.select('.job_academic')[0].text.strip()
        good_list = soup.select('.job_good_list')[0].text.strip()
        salary = soup.select(".job_money.cutom_font")[0].text.encode("utf-8")
        salary = salary.replace(b'\xee\x8b\x92', b"0")
        salary = salary.replace(b'\xee\x9e\x88', b"1")
        salary = salary.replace(b'\xef\x81\xa1', b"2")
        salary = salary.replace(b'\xee\x85\xbc', b"3")
        salary = salary.replace(b'\xef\x84\xa2', b"4")
        salary = salary.replace(b'\xee\x87\x99', b"5")
        salary = salary.replace(b'\xee\x9b\x91', b"6")
        salary = salary.replace(b'\xee\x94\x9d', b"7")
        salary = salary.replace(b'\xee\xb1\x8a', b"8")
        salary = salary.replace(b'\xef\x86\xbf', b"9")
        salary = salary.decode()

        job_detail = soup.select('.job_detail')[0].text.strip() if soup.select('.job_detail') else "无工作细节"

        job_data.append({
            '岗位名称': job,
            '薪资范围': salary,
            '企业名称': company_name,
            '工作地点': address,
            '学历要求': academic,
            '福利': good_list,
            '工作要求': job_detail
        })

    except Exception as e:
        print(f"处理URL {url} 时出错: {str(e)}")


def job_url(keyword=""):
    job_data = []  # 用于存储所有职位数据的列表
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '../data/实习岗位数据.json')
    for i in range(1, 10):  # 控制爬几页
        try:
            delay = random.uniform(1, 3)  # 生成1到3秒之间的随机浮点数
            time.sleep(delay)  # 添加延迟防止被封
            if keyword=="":
                req = requests.get(
                    f'https://www.shixiseng.com/interns?page={i}&type=intern&keyword=&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=全国&internExtend=',
                    headers=headers)
            else:
                                req = requests.get(
                    f'https://www.shixiseng.com/interns?page={i}&type=intern&keyword={keyword}&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=全国&internExtend=',
                    headers=headers)
            html = req.text
            soup = BeautifulSoup(html, 'lxml')
            offers = soup.select('.intern-wrap.intern-item') or []
            for offer in offers:
                url = offer.select(" .f-l.intern-detail__job a")[0]['href']
                detail_url(url, job_data)

            print(f"第{i}页抓取完成")
        except Exception as e:
            print(f"第{i}页抓取失败: {str(e)}")
            continue

    # 将数据保存到JSON文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(job_data, file, ensure_ascii=False, indent=4)

if __name__=='__main__':
    job_url("化学")
    print("数据已成功保存到 实习岗位数据.json 文件中")