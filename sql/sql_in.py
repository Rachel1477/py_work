import pymysql
import json
import os

# 数据库配置（按需修改）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rachel1211',
    'database': 'internship_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def write_in(keyword):
    """将JSON数据强制写入指定名称的数据库表（覆盖旧表）"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # 无论表是否存在都强制删除（如果存在）
        cursor.execute(f"DROP TABLE IF EXISTS {keyword}")  # 关键修改点

        # 创建新表（保证结构一致）
        create_sql = f"""
        CREATE TABLE {keyword} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            岗位名称 VARCHAR(255) NOT NULL,
            薪资范围 VARCHAR(100),
            企业名称 VARCHAR(255),
            工作地点 VARCHAR(100),
            学历要求 VARCHAR(100),
            福利 TEXT,
            工作要求 TEXT,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        cursor.execute(create_sql)

        # 读取JSON数据
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '../data', '实习岗位数据.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        if not json_data:
            print("JSON文件为空")
            return

        # 批量插入数据
        insert_sql = f"""
        INSERT INTO {keyword} (
            岗位名称, 薪资范围, 企业名称, 
            工作地点, 学历要求, 福利, 工作要求
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        batch_data = [
            (
                item['岗位名称'], item['薪资范围'], item['企业名称'],
                item['工作地点'], item['学历要求'], item['福利'], item['工作要求']
            )
            for item in json_data
        ]
        cursor.executemany(insert_sql, batch_data)
        connection.commit()
        print(f"数据已强制写入 {keyword} 表（覆盖旧表）")

    except Exception as e:
        print(f"操作失败: {str(e)}")
        if 'connection' in locals() and connection.open:
            connection.rollback()  # 出错时回滚
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

# 测试代码
if __name__ == "__main__":
    write_in("计算机")