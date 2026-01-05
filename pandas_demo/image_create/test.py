from datetime import datetime
import matplotlib.pyplot as plt

# 设置中文字体（解决中文显示乱码问题）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

money = [-405, 1300, 1244, 1080, 680, 770, 135, -460, 1080, -200, 1300, 1700, -34, 1200, -402, -1140, 625, 1480, 1330,
         3187, 2345, 500, -1200, 2100]


def get_past_24_months():
    current_year = datetime.now().year
    current_month = datetime.now().month
    months = []

    for i in range(24):
        # 计算目标月份和年份
        target_month = current_month - i
        target_year = current_year

        # 处理月份小于1的情况（跨年份）
        while target_month < 1:
            target_year -= 1
            target_month += 12

        # 格式化为 "年-月"（补零，比如2月变成02）
        month_str = f"{target_year}-{target_month:02d}"
        months.append(month_str)

    return months


if __name__ == "__main__":    # 获取过去24个月（从新到旧）

    past_24_months = get_past_24_months()

    # 反转金额列表，使其与月份列表（从新到旧）一一对应
    # 注：如果想让金额保持原顺序对应「从旧到新」的月份，可删除这行并反转月份列表
    money_reversed = money[::-1]  # 等价于money.reverse()，但不修改原列表

    # 打印月份和对应金额（验证对应关系）
    print("过去24个月（从新到旧）及对应金额：")
    for month, amount in zip(past_24_months, money_reversed):
        print(f"{month}: {amount}")

    # ========== 绘制二维散点图 ==========
    # 创建画布
    fig, ax = plt.subplots(figsize=(12, 6))

    # 绘制散点图
    # x轴：月份，y轴：金额，设置点的大小、颜色、透明度、边缘色
    ax.scatter(past_24_months, money_reversed, s=80, c='#2E86AB', alpha=0.8, edgecolors='white', linewidth=1)

    # 设置图表标题和轴标签
    ax.set_title('过去24个月收益散点图', fontsize=16, pad=20)
    ax.set_xlabel('年月', fontsize=12, labelpad=10)
    ax.set_ylabel('金额（元）', fontsize=12, labelpad=10)

    # 优化x轴标签显示（旋转45度避免重叠）
    plt.xticks(rotation=45, ha='right')

    # 添加水平参考线（y=0），区分收支
    ax.axhline(y=0, color='#E63946', linestyle='--', alpha=0.7, linewidth=1.5)

    # 网格线（便于读取数值）
    ax.grid(True, alpha=0.3, linestyle='-')

    # 调整布局（防止标签被截断）
    plt.tight_layout()

    # 显示图表
    plt.show()