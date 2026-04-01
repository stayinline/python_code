# 实战任务
import pandas as pd
import numpy as np

# 1. 创建不同类型的Series
s1 = pd.Series([1, 3, 5, np.nan, 6, 8])
s2 = pd.Series(['A', 'B', 'C', 'D'], index=['a', 'b', 'c', 'd'])
s3 = pd.Series({'北京': 2154, '上海': 2428, '广州': 1868, '深圳': 1756})

# 2. Series基本操作
print(s2.values)  # 获取值
print(s2.index)  # 获取索引
print(s3['北京'])  # 按索引取值

# | 1. 导入Pandas库（`import pandas as pd`），验证安装成功；<br>
# 2. 创建Series：存储5个城市的气温数据（带索引）；<br>
# 3. 创建DataFrame：存储3个学生的姓名、年龄、成绩数据；<br>
# 4. 用`head()`和`info()`查看DataFrame信息。 |

