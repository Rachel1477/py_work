import pymysql
import json
import os 
# 数据库配置（与sql_in.py保持一致）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rachel1211',
    'database': 'internship_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def show_list():
    """获取所有表名列表"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        # 执行 SHOW TABLES 并动态获取列名
        cursor.execute("SHOW TABLES")
        
        # 获取结果中的列名（例如 "Tables_in_internship_db"）
        column_name = cursor.description[0][0] if cursor.description else ''
        
        # 提取表名列表
        tables = [table[column_name] for table in cursor.fetchall()]
        return tables
        
    except Exception as e:
        print(f"获取表列表失败: {str(e)}")
        return []
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()
    
    
def read_out(keyword):
    """从指定表恢复数据到JSON文件"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 获取表数据
        cursor.execute(f"""
            SELECT 岗位名称,薪资范围,企业名称,
                   工作地点,学历要求,福利,工作要求 
            FROM {keyword}
        """)
        results = cursor.fetchall()

        # 转换数据结构
        json_data = [
            {
                "岗位名称": item["岗位名称"],
                "薪资范围": item["薪资范围"],
                "企业名称": item["企业名称"],
                "工作地点": item["工作地点"],
                "学历要求": item["学历要求"],
                "福利": item["福利"],
                "工作要求": item["工作要求"]
            }
            for item in results
        ]
        current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前py文件目录
        json_path = os.path.join(current_dir, '../data', '实习岗位数据.json') 
        # 写入JSON文件
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        print(f"数据已从 {keyword} 表恢复")

    except Exception as e:
        print(f"恢复数据失败: {str(e)}")
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

# 测试代码
if __name__ == "__main__":
    print("当前所有表:", show_list())
    read_out("test_jobs")