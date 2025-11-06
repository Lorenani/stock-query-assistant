import os
import asyncio
from typing import Optional
import dashscope
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
import pandas as pd
from sqlalchemy import create_engine
from qwen_agent.tools.base import BaseTool, register_tool
import matplotlib.pyplot as plt
import io
import base64
import time
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']  # 优先使用的中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 定义资源文件根目录
ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')

# 配置 DashScope
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY', '')  # 从环境变量获取 API Key
dashscope.timeout = 30  # 设置超时时间为 30 秒

# ====== 股票查询助手 system prompt 和函数描述 ======
system_prompt = """我是股票查询助手，以下是关于股票历史价格表 stock_price 的字段，我可能会编写对应的SQL，对数据进行查询
-- 股票历史价格表
CREATE TABLE stock_price (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    stock_name VARCHAR(20) NOT NULL COMMENT '股票名称',
    ts_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    trade_date VARCHAR(10) NOT NULL COMMENT '交易日期',
    open DECIMAL(15,2) COMMENT '开盘价',
    high DECIMAL(15,2) COMMENT '最高价',
    low DECIMAL(15,2) COMMENT '最低价',
    close DECIMAL(15,2) COMMENT '收盘价',
    vol DECIMAL(20,2) COMMENT '成交量',
    amount DECIMAL(20,2) COMMENT '成交额',
    UNIQUE KEY uniq_stock_date (ts_code, trade_date)
);
我将回答用户关于股票历史价格的相关问题。

功能说明：
1. 股票历史价格查询：可以通过SQL查询指定股票的历史价格数据
2. 多支股票对比分析：可以对比多支股票的价格走势、涨跌幅等指标
3. 热点新闻：可以搜索股票相关的热点新闻。如果Tavily搜索工具连接失败，请尝试使用必应搜索（bing-cn-mcp-server）作为备选方案。
4. 股票价格预测：使用ARIMA时间序列模型对未来股票价格进行预测

每当 exc_sql 工具返回 markdown 表格和图片时，你必须原样输出工具返回的全部内容（包括图片 markdown），不要只总结表格，也不要省略图片。这样用户才能直接看到表格和图片。

搜索热点新闻时，如果tavily-mcp工具连接失败，请自动尝试使用bing-cn-mcp-server的bing_search工具进行搜索。

如果是预测未来价格，需要对未来的价格进行详细的解释说明，比如价格将持续走高，或价格将相对平稳，或价格将持续走低。

查询股票撰写SQL的时候，需要按照 trade_date 升序排序，这样可以看到不同股票在同一天的价格对比。
trade_date的格式类似：2024-01-01
"""

# ====== 会话隔离 DataFrame 存储 ======
# 用于存储每个会话的 DataFrame，避免多用户数据串扰
_last_df_dict = {}

def get_session_id(kwargs):
    """根据 kwargs 获取当前会话的唯一 session_id，这里用 messages 的 id"""
    messages = kwargs.get('messages')
    if messages is not None:
        return id(messages)
    return None

# ====== exc_sql 工具类实现 ======
@register_tool('exc_sql')
class ExcSQLTool(BaseTool):
    """
    SQL查询工具，执行传入的SQL语句并返回结果，并自动进行可视化。
    支持股票历史价格查询和多支股票对比分析。
    """
    description = '对于生成的SQL，进行SQL查询，并自动可视化'
    parameters = [{
        'name': 'sql_input',
        'type': 'string',
        'description': '生成的SQL语句',
        'required': True
    }, {
        'name': 'need_visualize',
        'type': 'boolean',
        'description': '是否需要可视化和统计信息，默认True。如果是对比分析等场景可设为False，不进行可视化。',
        'required': False,
        'default': True
    }]

    def call(self, params: str, **kwargs) -> str:
        import json
        import matplotlib.pyplot as plt
        import io, os, time
        import numpy as np
        args = json.loads(params)
        sql_input = args['sql_input']
        database = args.get('database', 'stock')
        engine = create_engine(
            f'mysql+mysqlconnector://student123:student321@rm-uf6z891lon6dxuqblqo.mysql.rds.aliyuncs.com:3306/{database}?charset=utf8mb4',
            connect_args={'connect_timeout': 10}, pool_size=10, max_overflow=20
        )
        try:
            df = pd.read_sql(sql_input, engine)
            # 前5行+后5行拼接展示
            if len(df) > 10:
                md = pd.concat([df.head(5), df.tail(5)]).to_markdown(index=False)
            else:
                md = df.to_markdown(index=False)
            # 如果只有一行数据，只返回表格
            if len(df) == 1:
                return md
            need_visualize = args.get('need_visualize', True)
            if not need_visualize:
                return md
            desc_md = df.describe().to_markdown()
            # 自动创建目录
            save_dir = os.path.join(os.path.dirname(__file__), 'image_show')
            os.makedirs(save_dir, exist_ok=True)
            filename = f'stock_{int(time.time()*1000)}.png'
            save_path = os.path.join(save_dir, filename)
            # 智能选择可视化方式
            generate_smart_chart_png(df, save_path)
            img_path = os.path.join('image_show', filename)
            img_md = f'![股票数据图表]({img_path})'
            return f"{md}\n\n{desc_md}\n\n{img_md}"
        except Exception as e:
            return f"SQL执行或可视化出错: {str(e)}"

# ========== 智能可视化函数 ========== 
def generate_smart_chart_png(df_sql, save_path):
    """
    根据数据特征智能选择可视化方式
    - 数据点较多时使用折线图
    - 数据点较少时使用柱状图
    - 支持多支股票对比分析
    """
    columns = df_sql.columns
    if len(df_sql) == 0 or len(columns) < 2:
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, '无可视化数据', ha='center', va='center', fontsize=16)
        plt.axis('off')
        plt.savefig(save_path)
        plt.close()
        return
    
    x_col = columns[0]
    y_cols = columns[1:]
    x = df_sql[x_col]
    
    # 如果数据点较多，自动采样10个点
    if len(df_sql) > 20:
        idx = np.linspace(0, len(df_sql) - 1, 10, dtype=int)
        x = x.iloc[idx]
        df_plot = df_sql.iloc[idx]
        chart_type = 'line'
    else:
        df_plot = df_sql
        chart_type = 'bar'
    
    plt.figure(figsize=(10, 6))
    for y_col in y_cols:
        if chart_type == 'bar':
            plt.bar(df_plot[x_col], df_plot[y_col], label=str(y_col))
        else:
            plt.plot(df_plot[x_col], df_plot[y_col], marker='o', label=str(y_col))
    
    plt.xlabel(x_col)
    plt.ylabel('数值')
    plt.title('股票数据统计')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# ====== ARIMA股票预测工具 ======
@register_tool('arima_stock')
class ArimaStockTool(BaseTool):
    """
    对指定股票的收盘价进行ARIMA(5,1,5)建模，并预测未来n天的价格
    """
    description = '对指定股票(ts_code)的收盘价进行ARIMA(5,1,5)建模，并预测未来n天的价格，返回预测表格和折线图。'
    parameters = [
        {
            'name': 'ts_code',
            'type': 'string',
            'description': '股票代码，必填',
            'required': True
        },
        {
            'name': 'n',
            'type': 'integer',
            'description': '预测未来天数，必填',
            'required': True
        }
    ]
    
    def call(self, params: str, **kwargs) -> str:
        import json
        args = json.loads(params)
        ts_code = args['ts_code']
        n = int(args['n'])
        
        # 获取今天和一年前的日期
        today = datetime.now().date()
        start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
        
        # 连接MySQL，获取历史收盘价
        engine = create_engine(
            f"mysql+mysqlconnector://student123:student321@rm-uf6z891lon6dxuqblqo.mysql.rds.aliyuncs.com:3306/stock?charset=utf8mb4",
            connect_args={'connect_timeout': 10}, pool_size=10, max_overflow=20
        )
        sql = f"""
            SELECT trade_date, close FROM stock_price
            WHERE ts_code = '{ts_code}' AND trade_date >= '{start_date}' AND trade_date < '{end_date}'
            ORDER BY trade_date ASC
        """
        df = pd.read_sql(sql, engine)
        if len(df) < 30:
            return '历史数据不足，无法进行ARIMA建模预测。至少需要30天的历史数据。'
        
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df = df.dropna(subset=['close'])
        
        # ARIMA建模
        try:
            model = ARIMA(df['close'], order=(5,1,5))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=n)
            
            # 生成预测日期
            last_date = pd.to_datetime(df['trade_date'].iloc[-1])
            pred_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(n)]
            pred_df = pd.DataFrame({'预测日期': pred_dates, '预测收盘价': forecast})
            
            # 保存预测图
            save_dir = os.path.join(os.path.dirname(__file__), 'image_show')
            os.makedirs(save_dir, exist_ok=True)
            filename = f'arima_{ts_code}_{int(time.time()*1000)}.png'
            save_path = os.path.join(save_dir, filename)
            
            plt.figure(figsize=(10,6))
            plt.plot(df['trade_date'], df['close'], label='历史收盘价', linewidth=2)
            plt.plot(pred_df['预测日期'], pred_df['预测收盘价'], marker='o', label='预测收盘价', linewidth=2)
            plt.xlabel('日期')
            plt.ylabel('收盘价')
            plt.title(f'{ts_code} 收盘价ARIMA预测')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # 横坐标自动稀疏显示
            all_dates = list(df['trade_date']) + list(pred_df['预测日期'])
            total_len = len(all_dates)
            if total_len > 12:
                step = max(1, total_len // 10)
                show_idx = list(range(0, total_len, step))
                show_labels = [all_dates[i] for i in show_idx]
                plt.xticks(show_idx, show_labels, rotation=45)
            else:
                plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()
            
            img_path = os.path.join('image_show', filename)
            img_md = f'![ARIMA预测]({img_path})'
            return f"{pred_df.to_markdown(index=False)}\n\n{img_md}"
        except Exception as e:
            return f'ARIMA建模或预测出错: {str(e)}'

# ====== 初始化股票查询助手服务 ======
def init_agent_service():
    """初始化股票查询助手服务"""
    llm_cfg = {
        'model': 'qwen-turbo-2025-04-28',
        'timeout': 30,
        'retry_count': 3,
    }
    
    # 配置工具列表，包括MCP服务器和自定义工具
    function_list = [
        {
            "mcpServers": {
                # Tavily搜索工具，用于搜索股票热点新闻（主要）
                "tavily-mcp": {
                    "command": "npx",
                    "args": ["-y", "tavily-mcp@0.1.4"],
                    "env": {
                        "TAVILY_API_KEY": "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"
                    },
                    "disabled": False,
                    "autoApprove": []
                },
                # 必应搜索工具，作为Tavily的备选方案
                "bing-cn-mcp-server": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-bing-cn"],
                    "env": {},
                    "disabled": False,
                    "autoApprove": []
                }
            }
        },
        'exc_sql',      # SQL查询工具
        'arima_stock'   # ARIMA预测工具
    ]
    
    try:
        bot = Assistant(
            llm=llm_cfg,
            name='股票查询助手',
            description='股票历史价格查询、对比分析与价格预测',
            system_message=system_prompt,
            function_list=function_list
        )
        print("股票查询助手初始化成功！")
        return bot
    except Exception as e:
        print(f"助手初始化失败: {str(e)}")
        raise

def app_tui():
    """终端交互模式
    
    提供命令行交互界面，支持：
    - 连续对话
    - 文件输入
    - 实时响应
    """
    try:
        # 初始化助手
        bot = init_agent_service()

        # 对话历史
        messages = []
        while True:
            try:
                # 获取用户输入
                query = input('user question: ')
                # 获取可选的文件输入
                file = input('file url (press enter if no file): ').strip()
                
                # 输入验证
                if not query:
                    print('user question cannot be empty！')
                    continue
                    
                # 构建消息
                if not file:
                    messages.append({'role': 'user', 'content': query})
                else:
                    messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})

                print("正在处理您的请求...")
                # 运行助手并处理响应
                response = []
                for response in bot.run(messages):
                    print('bot response:', response)
                messages.extend(response)
            except Exception as e:
                print(f"处理请求时出错: {str(e)}")
                print("请重试或输入新的问题")
    except Exception as e:
        print(f"启动终端模式失败: {str(e)}")


def app_gui():
    """图形界面模式，提供 Web 图形界面"""
    try:
        print("正在启动 Web 界面...")
        # 初始化助手
        bot = init_agent_service()
        # 配置聊天界面，列举典型股票查询问题（分类展示）
        chatbot_config = {
            # 快速提示建议，按功能分类
            'prompt.suggestions': [
                # 历史价格查询类
                '查询2024年全年贵州茅台的收盘价走势',
                '查询中芯国际最近一个月的开盘价和收盘价',
                '统计2024年4月国泰君安的日均成交量',
                # 多股票对比分析类
                '对比2024年中芯国际和贵州茅台的涨跌幅',
                '对比五粮液和贵州茅台2024年的价格走势',
                '对比国泰君安和中芯国际的成交量变化',
                # 价格预测类
                '预测贵州茅台未来7天的收盘价',
                '预测中芯国际未来10天的股价走势',
                '预测五粮液未来5天的价格趋势',
                # 热点新闻类
                '贵州茅台最近的热点新闻',
                '中芯国际最新的市场动态',
                '搜索股票市场最新资讯',
            ],
            # 界面标题和描述
            'prompt.placeholder': '请输入您的问题，例如：查询股票价格、对比分析、价格预测、热点新闻等...',
            'prompt.title': '股票查询助手',
            'prompt.description': '支持股票历史价格查询、多股票对比分析、价格预测（ARIMA）和热点新闻搜索',
            # 自定义CSS样式，让按钮更圆润精致
            'custom_css': '''
                <style>
                    /* 圆润的按钮样式 */
                    button, .btn, [class*="button"], [class*="Button"] {
                        border-radius: 20px !important;
                        padding: 10px 20px !important;
                        font-size: 14px !important;
                        font-weight: 500 !important;
                        transition: all 0.3s ease !important;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
                        border: none !important;
                    }
                    
                    /* 按钮悬停效果 */
                    button:hover, .btn:hover, [class*="button"]:hover, [class*="Button"]:hover {
                        transform: translateY(-2px) !important;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
                    }
                    
                    /* 提示建议按钮样式 */
                    [class*="suggestion"], [class*="Suggestion"], [class*="prompt"] button {
                        border-radius: 25px !important;
                        padding: 12px 24px !important;
                        margin: 5px !important;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                        color: white !important;
                        font-weight: 500 !important;
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
                    }
                    
                    [class*="suggestion"]:hover, [class*="Suggestion"]:hover, [class*="prompt"] button:hover {
                        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
                        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
                        transform: translateY(-3px) !important;
                    }
                    
                    /* 输入框样式 */
                    input[type="text"], textarea {
                        border-radius: 15px !important;
                        padding: 12px 20px !important;
                        border: 2px solid #e0e0e0 !important;
                        transition: all 0.3s ease !important;
                    }
                    
                    input[type="text"]:focus, textarea:focus {
                        border-color: #667eea !important;
                        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
                        outline: none !important;
                    }
                    
                    /* 发送按钮样式 */
                    [class*="send"], [class*="Send"], [class*="submit"] {
                        border-radius: 20px !important;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                        color: white !important;
                        padding: 12px 30px !important;
                        font-weight: 600 !important;
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
                    }
                    
                    [class*="send"]:hover, [class*="Send"]:hover, [class*="submit"]:hover {
                        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
                        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
                        transform: translateY(-2px) !important;
                    }
                    
                    /* 整体容器圆角 */
                    [class*="container"], [class*="Container"], [class*="chat"] {
                        border-radius: 15px !important;
                    }
                    
                    /* 卡片样式 */
                    [class*="card"], [class*="Card"], [class*="message"] {
                        border-radius: 12px !important;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
                    }
                </style>
            '''
        }
        print("Web 界面准备就绪，正在启动服务...")
        # 启动 Web 界面
        webui = WebUI(
            bot,
            chatbot_config=chatbot_config,
            # 可选：设置服务器配置
            server_name='0.0.0.0',  # 允许外部访问（可选）
            server_port=7860,       # 端口号
            share=False             # 是否创建公网链接
        )
        
        # 注入自定义CSS样式（如果WebUI支持）
        try:
            # 尝试通过gradio的css参数注入样式
            if hasattr(webui, 'app') and hasattr(webui.app, 'css'):
                custom_css = """
                button, .btn, [class*="button"], [class*="Button"] {
                    border-radius: 20px !important;
                    padding: 10px 20px !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
                }
                button:hover, .btn:hover {
                    transform: translateY(-2px) !important;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
                }
                [class*="suggestion"] button, [class*="prompt"] button {
                    border-radius: 25px !important;
                    padding: 12px 24px !important;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                    color: white !important;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
                }
                [class*="suggestion"] button:hover {
                    transform: translateY(-3px) !important;
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
                }
                input, textarea {
                    border-radius: 15px !important;
                    padding: 12px 20px !important;
                }
                """
                webui.app.css = custom_css
        except Exception as e:
            print(f"CSS注入失败（不影响使用）: {str(e)}")
        
        webui.run()
    except Exception as e:
        print(f"启动 Web 界面失败: {str(e)}")
        print("请检查网络连接和 API Key 配置")


if __name__ == '__main__':
    # 运行模式选择
    app_gui()          # 图形界面模式（默认）
    # app_tui()        # 终端交互模式（取消注释以启用）

