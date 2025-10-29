import random
import time
import pandas as pd
from datetime import datetime


def excel_to_sql_insert(excel_file_path,protocol_step_id):
    # 读取Excel文件
    df = pd.read_excel(excel_file_path)

    # 默认值设置
    project_no = 'QL2025092001'
    project_id = '1971420898546688002'
    initial_sample_id = 'FD001001-1703251661554048'

    # 构建INSERT语句
    insert_statements = []

    start_id = generate_random_long_like_timestamp()

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

        # 构建VALUES部分
        values = f"""
(
    {current_id},  -- 在Python中生成的ID
    '{project_id}',
    '{project_no}',
    '{initial_sample_id}',
    '{protocol_step_id}', 
    '{source_plate_barcode}',
    '96',  -- 源板类型，根据实际情况填写
    '{source_well}',
    '{target_plate_barcode}',
    '96',  -- 目标板类型，根据实际情况填写
    '{target_well}',
    '{operation_time}',
    NULL,  -- volume
    NULL,  -- generation
    NULL,  -- drug_info
    NULL,  -- change_liquid_count
    NULL,  -- digestion
    '{report_time}',
    '{completion_time_str}',
    2,  -- _source_type
    timezone('Asia/Shanghai', now()),
    timezone('Asia/Shanghai', now()),
    false
)"""
        insert_statements.append(values)

    # 构建完整的INSERT语句
    insert_sql = f"""INSERT INTO sl_move_liquid (
    id, project_id, project_no, initial_sample_id, protocol_step_id,
    source_plate_barcode, source_barcode_type, source_well,
    target_plate_barcode, target_barcode_type, target_well,
    operation_time, volume, generation, drug_info, change_liquid_count, digestion,
    report_time, completion_time, _source_type, _create_time, _update_time, is_deleted
) VALUES {','.join(insert_statements)};"""

    return insert_sql, len(df)


def generate_random_long_like_timestamp():
    # 创建随机数生成器实例（对应Python中的random.Random()）
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


# 使用示例
if __name__ == "__main__":
    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\5样本移液信息1-原代.xlsx"
    # protocol_step_id = 'qilin_organoid_03_01'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\12样本移液信息1-传代.xlsx"
    # protocol_step_id = 'qilin_organoid_04_01'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\18冻存样本移液信息.xlsx"
    # protocol_step_id = 'qilin_organoid_05_01'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\23样本移液信息1-药敏加药前.xlsx"
    # protocol_step_id = 'qilin_organoid_07_01'

    excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\30药物板移液信息.xlsx"
    protocol_step_id = 'qilin_organoid_08_01'



    try:
        sql, record_count = excel_to_sql_insert(excel_file,protocol_step_id)
        print(f"生成的INSERT语句（共{record_count}条记录）：")
        print(sql)

        # 验证条数一致性
        df = pd.read_excel(excel_file)
        print(f"\nExcel中的记录条数: {len(df)}")
        print(f"生成的SQL记录条数: {record_count}")
        print(f"条数是否一致: {len(df) == record_count}")

    except Exception as e:
        print(f"处理文件时出错: {e}")
