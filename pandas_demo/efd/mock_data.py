import os
import re
import logging
import pandas as pd
import clickhouse_connect

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='efd_data_processing.log'
)
logger = logging.getLogger('parse_excel_data')

# 获取脚本所在目录的父目录（项目根目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ClickHouse 连接配置
CLICKHOUSE_CONFIG = {
    'host': '192.168.1.33',
    'user': 'default',
    'password': 'h6TWgrz227Fubhmb',
    'database': 'rptdw'
}

# 文件路径配置
SQL_FILE_PATH = os.path.join(BASE_DIR, 'efd', 'rptdw', 'rptdw_v2.sql')
ORIGIN_DATA_DIR = os.path.join(BASE_DIR, 'efd', 'origin_data')
EXCEL_FILE_PATH = os.path.join(ORIGIN_DATA_DIR, '日报涉及表结构与数据样例.xlsx')
TABLE_SHEET_MAP_FILE = os.path.join(ORIGIN_DATA_DIR, 'table_name_sheet_map')


class DataProcessor:
    def __init__(self):
        self.client = None
        self.excel_data = {}
        self.table_metadata = {}
        self.processed_data = {}

    def connect_clickhouse(self):
        """连接到 ClickHouse 数据库"""
        try:
            self.client = clickhouse_connect.get_client(**CLICKHOUSE_CONFIG)
            logger.info('成功连接到 ClickHouse 数据库')
            return True
        except Exception as e:
            logger.error(f'连接 ClickHouse 失败: {e}')
            return False

    def execute_sql_file(self, sql_file):
        """执行 SQL 文件创建数据库和表"""
        try:
            if not os.path.exists(sql_file):
                logger.error(f'SQL 文件不存在: {sql_file}')
                return False

            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            # 分割 SQL 语句并执行
            sql_statements = sql_content.split(';')
            for stmt in sql_statements:
                stmt = stmt.strip()
                if stmt and not stmt.startswith('--'):
                    self.client.command(stmt)
                    logger.info(f'执行 SQL 语句成功: {stmt[:100]}...')
            return True
        except Exception as e:
            logger.error(f'执行 SQL 文件失败: {e}')
            return False

    def parse_table_metadata_from_mapping_file(self):
        """从 table_name_sheet_map 文件中解析表元数据
        
        文件格式：
        sheet名称(第 xxx（表头） 到 yyy 行)
        
        规则：
        - 所有表名统一转为小写，以匹配 ClickHouse 表结构
        """
        try:
            logger.info('开始从 table_name_sheet_map 文件解析表元数据')
            
            if not os.path.exists(TABLE_SHEET_MAP_FILE):
                logger.error(f'映射文件不存在: {TABLE_SHEET_MAP_FILE}')
                return False
            
            with open(TABLE_SHEET_MAP_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 正则表达式匹配格式：sheet名称(第 xxx（表头） 到 yyy 行)
            pattern = r'^(.+?)\(第\s*(\d+)\s*（表头）\s*到\s*(\d+)\s*行\)'
            
            parsed_count = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(pattern, line)
                if match:
                    sheet_name = match.group(1).strip()
                    header_row = int(match.group(2))
                    end_row = int(match.group(3))
                    
                    # 所有表名统一转为小写，以匹配 ClickHouse 表结构
                    table_name = sheet_name.lower()
                    
                    # 计算数据行数
                    data_start_row = header_row + 1
                    data_row_count = end_row - header_row
                    
                    self.table_metadata[table_name] = {
                        'sheet_name': sheet_name,
                        'header_row': header_row,
                        'data_start_row': data_start_row,
                        'end_row': end_row,
                        'data_row_count': data_row_count
                    }
                    
                    parsed_count += 1
                    logger.info(f'✓ 解析表 {table_name}:')
                    logger.info(f'    Sheet名称: {sheet_name}')
                    logger.info(f'    表头行: {header_row}, 数据行: {data_start_row}-{end_row} (共{data_row_count}行)')
                else:
                    logger.warning(f'✗ 无法解析行: {line}')
            
            logger.info(f'\n表元数据解析完成，共解析 {parsed_count} 个表')
            return parsed_count > 0
        except Exception as e:
            logger.error(f'解析表元数据失败: {e}')
            import traceback
            logger.error(traceback.format_exc())
            return False

    def load_data_from_excel(self):
        """根据元数据从 Excel 文件加载数据"""
        try:
            logger.info('开始从 Excel 文件加载数据')
            
            if not os.path.exists(EXCEL_FILE_PATH):
                logger.error(f'Excel 文件不存在: {EXCEL_FILE_PATH}')
                return False
            
            # 使用 ExcelFile 对象，避免重复打开文件
            excel_file = pd.ExcelFile(EXCEL_FILE_PATH)
            
            loaded_count = 0
            failed_count = 0
            
            for table_name, metadata in self.table_metadata.items():
                try:
                    sheet_name = metadata['sheet_name']
                    header_row = metadata['header_row']      # 表头行号（从1开始）
                    end_row = metadata['end_row']                # 数据结束行
                    expected_rows = metadata['data_row_count']   # 预期数据行数
                    
                    # 检查 sheet 是否存在
                    if sheet_name not in excel_file.sheet_names:
                        logger.warning(f'✗ Sheet "{sheet_name}" 在 Excel 文件中不存在，跳过表 {table_name}')
                        failed_count += 1
                        continue
                    
                    # pandas 读取 Excel 的参数说明：
                    # header: 表头所在的行索引（从0开始计数），所以 header_row - 1
                    # nrows: 读取的数据行数（不包括表头）
                    
                    header_index = header_row - 1  # 转换为从0开始的索引
                    data_rows = end_row - header_row  # 数据行数
                    
                    # 读取数据
                    df = pd.read_excel(
                        excel_file,
                        sheet_name=sheet_name,
                        header=header_index,  # 表头行索引
                        nrows=data_rows       # 数据行数
                    )
                    
                    self.excel_data[table_name] = df
                    loaded_count += 1
                    
                    # 验证行数
                    if len(df) == expected_rows:
                        logger.info(f'✓ 表 {table_name}: 成功加载 {len(df)} 行数据 (列数: {len(df.columns)})')
                    else:
                        logger.warning(f'⚠ 表 {table_name}: 加载 {len(df)} 行数据，但预期 {expected_rows} 行')
                        logger.info(f'    列名: {list(df.columns)[:5]}...' if len(df.columns) > 5 else f'    列名: {list(df.columns)}')
                    
                except Exception as e:
                    logger.error(f'✗ 加载表 {table_name} 的数据失败: {e}')
                    import traceback
                    logger.error(traceback.format_exc())
                    failed_count += 1
                    continue
            
            excel_file.close()
            logger.info(f'\nExcel 数据加载完成: 成功 {loaded_count} 个表，失败 {failed_count} 个表')
            return loaded_count > 0
        except Exception as e:
            logger.error(f'从 Excel 加载数据失败: {e}')
            import traceback
            logger.error(traceback.format_exc())
            return False

    def compare_data(self):
        """比对 Excel 数据和 SQL 文件中的数据"""
        try:
            logger.info('开始比对数据一致性')
            
            consistent_count = 0
            inconsistent_count = 0
            
            for table_name, df in self.excel_data.items():
                metadata = self.table_metadata.get(table_name, {})
                expected_rows = metadata.get('data_row_count', 0)
                sql_file = metadata.get('sql_file', '')
                
                logger.info(f'\n表 {table_name}:')
                logger.info(f'  Excel 实际行数: {len(df)}')
                logger.info(f'  预期行数: {expected_rows}')
                logger.info(f'  列数: {len(df.columns)}')
                
                is_consistent = True
                
                # 检查行数是否一致
                if len(df) != expected_rows:
                    logger.warning(f'  ⚠ 警告: 数据行数不一致! 预期 {expected_rows} 行，实际 {len(df)} 行')
                    is_consistent = False
                else:
                    logger.info(f'  ✓ 行数一致')
                
                # 如果有 SQL 文件，检查其中的手动复制数据
                if sql_file:
                    sql_file_path = os.path.join(ORIGIN_DATA_DIR, sql_file)
                    if os.path.exists(sql_file_path):
                        with open(sql_file_path, 'r', encoding='utf-8') as f:
                            sql_content = f.read()
                        
                        # 统计 SQL 文件中的数据行数（从注释后的数据部分）
                        if '--下面是手动复制Excel表格中的数据' in sql_content:
                            data_section = sql_content.split('--下面是手动复制Excel表格中的数据')[1]
                            # 过滤掉空行和表头行
                            lines = [line.strip() for line in data_section.strip().split('\n') 
                                   if line.strip() and not line.strip().startswith('OBJECT_RRN')]
                            sql_row_count = len(lines)
                            
                            logger.info(f'  SQL 文件中手动复制的数据行数: {sql_row_count}')
                            
                            if len(df) != sql_row_count:
                                logger.warning(f'  ⚠ 与 SQL 文件中的数据行数不一致!')
                                is_consistent = False
                            else:
                                logger.info(f'  ✓ 与 SQL 文件数据一致')
                
                if is_consistent:
                    consistent_count += 1
                else:
                    inconsistent_count += 1
            
            logger.info(f'\n数据比对总结: {consistent_count} 个表一致, {inconsistent_count} 个表不一致')
            return True
        except Exception as e:
            logger.error(f'数据比对失败: {e}')
            import traceback
            logger.error(traceback.format_exc())
            return False

    def fill_empty_fields(self):
        """补全数据中的空字段"""
        try:
            logger.info('开始补全空字段')
            
            total_nulls_filled = 0
            
            for table_name, df in self.excel_data.items():
                original_null_count = df.isnull().sum().sum()
                
                if original_null_count == 0:
                    logger.info(f'✓ 表 {table_name}: 无空值，共 {len(df)} 行')
                    self.processed_data[table_name] = df
                    continue
                
                # 补全空字段
                fill_values = {}
                for col in df.columns:
                    if df[col].isnull().any():
                        if df[col].dtype == 'object':
                            fill_values[col] = ''
                        elif df[col].dtype in ['int64', 'float64']:
                            fill_values[col] = 0
                        else:
                            fill_values[col] = ''
                
                if fill_values:
                    df.fillna(value=fill_values, inplace=True)
                
                final_null_count = df.isnull().sum().sum()
                nulls_filled = original_null_count - final_null_count
                total_nulls_filled += nulls_filled
                
                self.processed_data[table_name] = df
                logger.info(f'✓ 表 {table_name}: 补全了 {nulls_filled} 个空值，共 {len(df)} 行')
            
            logger.info(f'\n空字段补全完成，共补全 {total_nulls_filled} 个空值')
            return True
        except Exception as e:
            logger.error(f'补全空字段失败: {e}')
            import traceback
            logger.error(traceback.format_exc())
            return False

    def write_to_clickhouse(self):
        """将处理后的数据写入 ClickHouse"""
        try:
            logger.info('开始写入 ClickHouse')
            success_count = 0
            fail_count = 0
            total_rows = 0
            
            # 列名拼写修正映射
            column_name_fixes = {
                'privious_node_rrn': 'previous_node_rrn'
            }
            
            for table_name, df in self.processed_data.items():
                if df.empty:
                    logger.warning(f'⚠ 表 {table_name} 数据为空，跳过')
                    continue
                
                try:
                    # 创建副本以避免修改原始数据
                    df_copy = df.copy()
                    
                    # 修正列名拼写错误
                    df_copy.rename(columns=column_name_fixes, inplace=True)
                    
                    # 第一步：处理所有列的基本类型转换
                    for col in df_copy.columns:
                        col_lower = col.lower()
                        
                        # 检查是否是 DateTime 类型的列（根据列名判断）
                        is_datetime_col = any(keyword in col_lower for keyword in 
                                            ['time', 'date', 'created', 'updated', 'logon', 'approved'])
                        
                        if is_datetime_col or pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                            # DateTime 类型：转换 Excel serial number 或处理 NaT
                            def convert_datetime(x):
                                if x is None or (hasattr(pd, 'isna') and pd.isna(x)):
                                    return None
                                elif isinstance(x, (int, float)):
                                    try:
                                        dt = pd.to_datetime('1899-12-30') + pd.Timedelta(days=x)
                                        if hasattr(pd, 'isna') and pd.isna(dt):
                                            return None
                                        return dt
                                    except:
                                        return None
                                elif hasattr(x, 'timestamp'):
                                    if hasattr(pd, 'isna') and pd.isna(x):
                                        return None
                                    return x
                                else:
                                    try:
                                        dt = pd.to_datetime(x)
                                        if hasattr(pd, 'isna') and pd.isna(dt):
                                            return None
                                        return dt
                                    except:
                                        return None
                            
                            df_copy[col] = df_copy[col].apply(convert_datetime)
                    
                    # 第二步：将所有非数值、非DateTime列强制转为字符串
                    for col in df_copy.columns:
                        col_lower = col.lower()
                        is_datetime_col = any(keyword in col_lower for keyword in 
                                            ['time', 'date', 'created', 'updated', 'logon', 'approved'])
                        
                        # 如果不是 DateTime 且不是数值类型，则转为字符串
                        if not is_datetime_col and not pd.api.types.is_numeric_dtype(df_copy[col]):
                            def to_string_safe(x):
                                if x is None or (hasattr(pd, 'isna') and pd.isna(x)):
                                    return ''
                                return str(x)
                            
                            df_copy[col] = df_copy[col].apply(to_string_safe)
                    
                    # 第三步：处理数值列的 NaN
                    for col in df_copy.columns:
                        if pd.api.types.is_numeric_dtype(df_copy[col]):
                            df_copy[col] = df_copy[col].where(df_copy[col].notna(), None)
                    
                    # 提取列名并转换为小写
                    columns = [col.lower() for col in df_copy.columns]
                    
                    # 第四步：构建数据行，做最后的类型检查和转换
                    data = []
                    for _, row in df_copy.iterrows():
                        row_data = []
                        for idx, val in enumerate(row):
                            col_name = columns[idx]
                            
                            # 严格检查空值
                            is_empty = False
                            if val is None:
                                is_empty = True
                            else:
                                try:
                                    is_empty = bool(pd.isna(val))
                                except:
                                    pass
                                
                                try:
                                    if type(val).__name__ == 'NaTType':
                                        is_empty = True
                                except:
                                    pass
                            
                            if is_empty:
                                # 对于 String 列，使用空字符串；对于其他列，使用 None
                                # 这里简化处理：统一使用 None，让 ClickHouse 自己处理
                                row_data.append(None)
                            elif hasattr(val, 'timestamp'):
                                # DateTime 对象
                                try:
                                    row_data.append(int(val.timestamp()))
                                except:
                                    row_data.append(None)
                            elif isinstance(val, str):
                                row_data.append(val)
                            elif isinstance(val, (int, float)):
                                row_data.append(val)
                            else:
                                # 其他类型转为字符串
                                row_data.append(str(val))
                        
                        data.append(row_data)
                    
                    # 插入数据到 ClickHouse
                    self.client.insert(f'rptdw.{table_name}', data, column_names=columns)
                    
                    row_count = len(df_copy)
                    total_rows += row_count
                    logger.info(f'✓ 成功写入表 {table_name}: {row_count} 条数据')
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f'✗ 写入表 {table_name} 失败: {e}')
                    import traceback
                    logger.error(traceback.format_exc())
                    fail_count += 1
                    continue
            
            logger.info(f'\n数据写入完成:')
            logger.info(f'  成功: {success_count} 个表')
            logger.info(f'  失败: {fail_count} 个表')
            logger.info(f'  总数据量: {total_rows} 条')
            
            return fail_count == 0
        except Exception as e:
            logger.error(f'写入 ClickHouse 失败: {e}')
            import traceback
            logger.error(traceback.format_exc())
            return False

    def run(self):
        """运行整个数据处理流程"""
        logger.info('=' * 80)
        logger.info('开始数据处理流程')
        logger.info('=' * 80)
        
        # 1. 连接 ClickHouse
        logger.info('\n【步骤 1/6】连接 ClickHouse')
        if not self.connect_clickhouse():
            logger.error('❌ 连接 ClickHouse 失败，终止流程')
            return False
        logger.info('✓ 连接成功')
        
        # 2. 执行 SQL 文件创建表结构
        logger.info('\n【步骤 2/6】执行 SQL 文件创建表结构')
        if not self.execute_sql_file(SQL_FILE_PATH):
            logger.error('❌ 执行 SQL 文件失败，终止流程')
            return False
        logger.info('✓ 表结构创建成功')
        
        # 3. 从 table_name_sheet_map 文件中解析表元数据
        logger.info('\n【步骤 3/6】解析表元数据（从 table_name_sheet_map 文件）')
        if not self.parse_table_metadata_from_mapping_file():
            logger.error('❌ 解析表元数据失败，终止流程')
            return False
        logger.info('✓ 元数据解析成功')
        
        # 4. 从 Excel 文件加载数据
        logger.info('\n【步骤 4/6】从 Excel 加载数据')
        if not self.load_data_from_excel():
            logger.error('❌ 从 Excel 加载数据失败，终止流程')
            return False
        logger.info('✓ 数据加载成功')
        
        # 5. 比对数据
        logger.info('\n【步骤 5/6】比对数据一致性')
        if not self.compare_data():
            logger.error('❌ 数据比对失败，终止流程')
            return False
        logger.info('✓ 数据比对完成')
        
        # 6. 补全空字段并写入 ClickHouse
        logger.info('\n【步骤 6/6】补全空字段并写入 ClickHouse')
        if not self.fill_empty_fields():
            logger.error('❌ 补全空字段失败，终止流程')
            return False
        
        if not self.write_to_clickhouse():
            logger.error('❌ 写入 ClickHouse 失败')
            return False
        
        logger.info('\n' + '=' * 80)
        logger.info('✅ 数据处理流程全部完成')
        logger.info('=' * 80)
        return True


if __name__ == '__main__':
    processor = DataProcessor()
    success = processor.run()
    
    print('\n' + '=' * 80)
    if success:
        print('✅ 数据处理成功完成！')
        print('详细信息请查看日志文件: efd_data_processing.log')
    else:
        print('❌ 数据处理失败，请查看日志文件了解详情。')
        print('日志文件位置: efd_data_processing.log')
    print('=' * 80)
