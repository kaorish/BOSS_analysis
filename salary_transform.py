import pandas as pd
import re

# 读取CSV文件
file_path = 'Combined.csv'
df = pd.read_csv(file_path,encoding='ANSI')

# 确保Salary列是字符串类型
df['Salary'] = df['Salary'].astype(str)

# 检查并提取薪资格式
def extract_salary_range(s):
    # 正则表达式匹配薪资范围，忽略可能的福利部分
    pattern = r'(\d+)-(\d+)(?:K|元/月)(?:·.*)?'
    match = re.match(pattern, s)
    if match:
        min_salary_str, max_salary_str = match.groups()
        # 处理K和元/月的单位
        if 'K' in s:
            min_salary, max_salary = int(min_salary_str) * 1000, int(max_salary_str) * 1000
        else:
            min_salary, max_salary = int(min_salary_str), int(max_salary_str)
        return min_salary, max_salary
    else:
        return None, None

# 应用函数并创建新的列
df[['Salary_Min_Processed', 'Salary_Max_Processed']] = df['Salary'].apply(extract_salary_range).apply(pd.Series)

# 过滤出薪资格式已经成功提取的行（可选）
df_filtered = df.dropna(subset=['Salary_Min_Processed', 'Salary_Max_Processed'])

# 保存处理后的DataFrame到新的CSV文件
output_file_path = 'output1.sv'  # 你想要保存的新CSV文件路径
df_filtered.to_csv(output_file_path, index=False)