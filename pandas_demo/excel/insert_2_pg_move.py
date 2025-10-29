import time
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2 import OperationalError, IntegrityError

import my_tools as mt

type_map = {
    "FD001001P00C01": "24",
    "FD001001P00C02": "24",
    "FD001001P01S01": "96",
    "FD001001P01C01": "24",
    "FD001001P01C02": "24",
    "FD001001P02S01": "96",
    "FD001001P02F": "24",
    "FD001001P02S02": "96",
    "FD001001P02A01": "96",
    "FD001001P02D01": "96"
}


def excel_to_sql_insert(excel_file_path, protocol_step_id):
    # 读取Excel文件
    df = pd.read_excel(excel_file_path)

    # 默认值设置
    project_no = 'QL2025092001'
    project_id = '1971420898546688002'
    # initial_sample_id = 'FD001001-1703251661554048'


    # initial_sample_id = 'FD001002-1703417177178496'

    initial_sample_id = 'FD001003-1703422682202496'


    # initial_sample_id = 'FD001004-1703426394161536'

    # initial_sample_id = 'FD001005-1703429609095552'



    # 构建INSERT语句
    insert_statements = []

    start_id = mt.generate_random_long_like_timestamp()

    for index, row in df.iterrows():
        # 直接匹配字段
        source_plate_barcode = str(row['源板ID']).replace("'", "''")  # 处理单引号
        source_well = str(row['源孔位']).replace("'", "''")
        target_plate_barcode = str(row['目标板ID']).replace("'", "''")
        target_well = str(row['目标孔位']).replace("'", "''")
        completion_time = row['完成时间']

        # 处理时间字段
        if pd.notna(completion_time):
            if isinstance(completion_time, str):
                operation_time = completion_time
                completion_time_str = completion_time
            else:
                operation_time = completion_time.strftime('%Y-%m-%d %H:%M:%S')
                completion_time_str = str(completion_time)
        else:
            operation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            completion_time_str = 'NULL'

        report_time = operation_time

        # 生成当前记录的ID
        current_id = start_id + index

        s_type = type_map.get(source_plate_barcode)
        t_type = type_map.get(target_plate_barcode)

        # 构建VALUES部分
        values = f"""
(
    {current_id},  -- 在Python中生成的ID
    '{project_id}',
    '{project_no}',
    '{initial_sample_id}',
    '{protocol_step_id}', 
    '{source_plate_barcode}',
    '{s_type}',  
    '{source_well}',
    '{target_plate_barcode}',
    '{t_type}', 
    '{target_well}',
    '{operation_time}',
    NULL,  -- volume
    NULL,  -- generation
    NULL,  -- drug_info
    NULL,  -- change_liquid_count
    NULL,  -- digestion
    '{report_time}',
    '{completion_time_str if completion_time_str != 'NULL' else 'NULL'}',
    2,  -- _source_type
    timezone('Asia/Shanghai', now()),
    timezone('Asia/Shanghai', now()),
    false
)"""
        insert_statements.append(values)

    # 构建完整的INSERT语句
    insert_sql = f"""INSERT INTO public.sl_move_liquid (
    id, project_id, project_no, initial_sample_id, protocol_step_id,
    source_plate_barcode, source_barcode_type, source_well,
    target_plate_barcode, target_barcode_type, target_well,
    operation_time, volume, generation, drug_info, change_liquid_count, digestion,
    report_time, completion_time, _source_type, _create_time, _update_time, is_deleted
) VALUES {','.join(insert_statements)};"""

    return insert_sql, len(df)




def execute_sql_in_postgres(sql, db_config):

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

    excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选3\5样本移液信息1-原代.xlsx"
    protocol_step_id = 'qilin_organoid_03_01'
    #
    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选3\12样本移液信息1-传代.xlsx"
    # protocol_step_id = 'qilin_organoid_04_01'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选3\18冻存样本移液信息.xlsx"
    # protocol_step_id = 'qilin_organoid_05_01'
    #
    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选3\23样本移液信息1-药敏加药前.xlsx"
    # protocol_step_id = 'qilin_organoid_07_01'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选3\30药物板移液信息.xlsx"
    # protocol_step_id = 'qilin_organoid_08_01'

    try:
        # 生成SQL语句
        sql, record_count = excel_to_sql_insert(excel_file, protocol_step_id)
        print(f"生成的INSERT语句（共{record_count}条记录）")

        # 验证条数一致性
        df = pd.read_excel(excel_file)
        print(f"\nExcel中的记录条数: {len(df)}")
        print(f"生成的SQL记录条数: {record_count}")
        print(f"条数是否一致: {len(df) == record_count}")
        print(sql)

        # 如果记录数一致且大于0，则执行插入操作
        if len(df) == record_count and record_count > 0:
            success, rows_affected = execute_sql_in_postgres(sql, db_config_win)
            if success:
                print(f"成功插入 {rows_affected} 条记录")
            else:
                print("插入操作失败")
    except Exception as e:
        print(f"处理文件时出错: {e}")
