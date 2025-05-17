import analysis.LLM
from flask import Flask, render_template, jsonify, redirect, url_for ,request
import pandas as pd
import os
import analysis.analysis
import analysis.LLM
import sql.sql_in
app = Flask(__name__)

# 配置文件上传
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    """首页路由"""
    return render_template('index.html')

@app.route('/start_crawling')
def start_crawling():
    """跳转到爬取页面"""
    global keyword 
    keyword = request.args.get('keyword', default='', type=str)
    return render_template('crawling.html')

@app.route('/run_spider')
def run_spider():
    """触发爬虫程序"""
    try:
        from spider.spider import job_url
        job_url(keyword)
        print("keyword=",keyword)
        if keyword!='': sql.sql_in.write_in(keyword)
        return redirect(url_for('show_analysis'))
    except Exception as e:
        return render_template('crawling.html', error=str(e))

@app.route('/analysis')
def show_analysis():
    """显示分析页面"""
    analysis.analysis.main()
    return render_template('analysis.html')
@app.route('/history')
def show_history():
    """返回历史记录"""
    import sql.sql_out
    list=sql.sql_out.show_list()
    return render_template('history.html', table_list=list)
@app.route('/process_selection', methods=['POST'])
def process_selection():
    """处理用户选择"""
    selected_table = request.form.get('selected_table')
    if selected_table:
        import sql.sql_out
        sql.sql_out.read_out(str(selected_table))
        return redirect(url_for('show_analysis'))
    return redirect(url_for('show_history'))
    
@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    reply = analysis.LLM.ask_llm(user_msg)  # 复用ask_llm 函数
    return jsonify(reply=reply)
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True,port=3389)