import tushare as ts
import pandas as pd
from datetime import datetime

# 设置tushare的token，需要自己去tushare官网注册获取
# 请将'YOUR_TUSHARE_TOKEN_HERE'替换为自己的token
ts.set_token('68dde442e752cafddb5e37a3462561949e575b10658e9eb493999a02')
pro = ts.pro_api()

# 定义股票代码和名称映射
stocks = {
    '600519.SH': '贵州茅台',
    '000858.SZ': '五粮液',
    '601211.SH': '国泰君安',
    '688981.SH': '中芯国际'
}

# 设置时间范围
start_date = '20210101'
end_date = datetime.now().strftime('%Y%m%d')

# 创建一个空的DataFrame用于存储所有数据
all_data = pd.DataFrame()

for code, name in stocks.items():
    print(f"正在获取{name}({code})的数据...")
    try:
        # 获取股票历史数据
        df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
        # 添加股票名称列
        df['stock_name'] = name
        # 添加股票代码列
        df['stock_code'] = code
        # 按日期排序
        df = df.sort_values('trade_date').reset_index(drop=True)
        # 将日期列从YYYYMMDD格式转换为YYYY-MM-DD格式
        df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        # 追加到总数据框
        all_data = pd.concat([all_data, df], ignore_index=True)
        print(f"{name}数据获取完成，共{len(df)}条记录")
    except Exception as e:
        print(f"获取{name}({code})数据时出错: {e}")

# 按交易日期排序
all_data = all_data.sort_values(['trade_date', 'stock_name']).reset_index(drop=True)

# 保存到Excel文件的单个sheet中
with pd.ExcelWriter('stock_data.xlsx', engine='openpyxl') as writer:
    all_data.to_excel(writer, sheet_name='stock_data', index=False)

print(f"所有股票数据已保存到stock_data.xlsx文件中的stock_data工作表中，总计{len(all_data)}条记录")