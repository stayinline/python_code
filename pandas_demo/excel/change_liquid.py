
import random
import time
import pandas as pd
from datetime import datetime

def excel_to_postgresql_insert(excel_file, protocol_step_id):
    # 读取Excel文件
    df = pd.read_excel(excel_file, sheet_name='sheet0')

    # 默认值设置
    project_no = 'QL2025092001'
    project_id = '1971420898546688002'
    initial_sample_id = 'FD001001-1703251661554048'
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

    return insert_statements




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



# 执行函数并输出结果
if __name__ == "__main__":

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\5样本移液信息1-原代.xlsx"
    # protocol_step_id = 'qilin_organoid_03_01'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\12样本移液信息1-传代.xlsx"
    # protocol_step_id = 'qilin_organoid_04_01'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\18冻存样本移液信息.xlsx"
    # protocol_step_id = 'qilin_organoid_05_01'

    # excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\23样本移液信息1-药敏加药前.xlsx"
    # protocol_step_id = 'qilin_organoid_07_01'

    excel_file = r"C:\Users\Mega\Documents\dingding_doc\麒麟项目demo数据-复旦大学肠癌类器官药物筛选1\6样本换液记录1-原代.xlsx"
    protocol_step_id = 'qilin_organoid_03_02'

    inserts = excel_to_postgresql_insert(excel_file, protocol_step_id)

    print(f"-- 共生成 {len(inserts)} 条INSERT语句")
    print("-- 开始生成INSERT语句...\n")

    for i, sql in enumerate(inserts, 1):
        print(sql)
        print()

    print(f"-- 总共生成 {len(inserts)} 条记录，与Excel中的 {len(inserts)} 条记录一致")
