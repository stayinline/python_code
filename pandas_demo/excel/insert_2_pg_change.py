import random
import time
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2 import OperationalError, IntegrityError


def excel_to_postgresql_insert(excel_file, protocol_step_id, initial_sample_id):
    # 读取Excel文件
    df = pd.read_excel(excel_file, sheet_name='sheet0')

    # 默认值设置
    project_no = 'QL2025092001'
    project_id = '1971420898546688002'
    start_id = generate_random_long_like_timestamp()

    # 生成INSERT语句
    insert_statements = []

    for index, row in df.iterrows():
        # 构建INSERT语句
        insert_sql = f"""
INSERT INTO sl_change_liquid (
    id, project_id, project_no, initial_sample_id, protocol_step_id, 
    plate_barcode, operation_time, change_liquid_count, report_time, _source_type
) VALUES (
    {start_id}, 
    '{project_id}', 
    '{project_no}', 
    '{initial_sample_id}', 
    '{protocol_step_id}', 
    '{row['培养板ID']}', 
    '{row['完成时间']}', 
    '{row['第几次换液']}', 
    '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', 
    2
);"""
        insert_statements.append(insert_sql)

    return insert_statements, len(insert_statements)


def generate_random_long_like_timestamp():
    # 创建随机数生成器实例
    rand = random.Random()

    # 获取当前毫秒级时间戳（作为基础值，类似时间戳特性）
    current_millis = int(time.time() * 1000)

    # 定义随机偏移范围（例如：±1天的毫秒数，可根据需求调整）
    one_day_millis = 24 * 60 * 60 * 1000  # 86400000毫秒
    min_offset = -one_day_millis  # 最小偏移：-1天
    max_offset = one_day_millis  # 最大偏移：+1天

    # 生成指定范围内的随机偏移量（整数）
    offset = rand.randint(min_offset, max_offset)

    # 计算最终结果（确保为正数，符合时间戳特性）
    result = current_millis + offset
    return result if result >= 0 else -result  # 避免负数


def execute_sql_in_postgres(sql, db_config):
    """
    连接到PostgreSQL数据库并执行SQL语句

    参数:
        sql: 要执行的SQL语句
        db_config: 数据库配置字典，包含host, port, database, user, password
    """
    connection = None
    try:
        # 连接到数据库
        connection = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )

        # 创建游标对象
        cursor = connection.cursor()

        # 执行SQL语句
        print("开始执行SQL插入操作...")
        start_time = time.time()

        cursor.execute(sql)

        # 提交事务
        connection.commit()

        end_time = time.time()
        print(f"SQL插入操作执行成功，耗时: {end_time - start_time:.2f}秒")
        print(f"影响的行数: {cursor.rowcount}")

        return True, cursor.rowcount

    except OperationalError as e:
        print(f"数据库连接错误: {e}")
        if connection:
            connection.rollback()
        return False, 0
    except IntegrityError as e:
        print(f"数据完整性错误: {e}")
        if connection:
            connection.rollback()
        return False, 0
    except Exception as e:
        print(f"执行SQL时发生错误: {e}")
        if connection:
            connection.rollback()
        return False, 0
    finally:
        # 关闭数据库连接
        if connection:
            cursor.close()
            connection.close()
            print("数据库连接已关闭")


# 使用示例
if __name__ == "__main__":
    # 数据库配置 - 请根据实际情况修改这些参数
    db_config_suzhou = {
        'host': '192.168.3.134',
        'port': '15432',
        'database': 'megaflux',
        'user': 'megaflux',
        'password': 'megaflux'
    }
    db_config_win = {
        'host': '192.168.254.23',
        'port': '5432',
        'database': 'megaflux',
        'user': 'megaflux',
        'password': 'megaflux'
    }

    # initial_sample_id = 'FD001001-1703251661554048'
    # initial_sample_id = 'FD001002-1703417177178496'
    # initial_sample_id = 'FD001003-1703422682202496'
    initial_sample_id = 'FD001005-1703429609095552'
    # initial_sample_id = 'FD001004-1703426394161536'
    #
    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选5\6样本换液记录1-原代.xlsx"
    # protocol_step_id = 'qilin_organoid_03_02'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选5\15样本换液记录1-传代.xlsx"
    # protocol_step_id = 'qilin_organoid_04_02'

    excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选5\26样本换液记录1-药敏加药前.xlsx"
    protocol_step_id = 'qilin_organoid_07_03'



    try:

        # 生成SQL语句
        inserts, record_count = excel_to_postgresql_insert(excel_file, protocol_step_id, initial_sample_id)
        print(f"生成的INSERT语句（共{record_count}条记录）")

        # 验证条数一致性
        df = pd.read_excel(excel_file)
        print(f"\nExcel中的记录条数: {len(df)}")
        print(f"生成的SQL记录条数: {record_count}")
        print(f"条数是否一致: {len(df) == record_count}")
        # print(inserts)

        # 如果记录数一致且大于0，则执行插入操作
        if len(df) == record_count and record_count > 0:
            for i, sql in enumerate(inserts, 1):
                success, rows_affected = execute_sql_in_postgres(sql, db_config_win)

    except Exception as e:
        print(f"处理文件时出错: {e}")
