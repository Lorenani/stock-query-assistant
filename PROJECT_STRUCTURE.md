# 项目结构说明

## 核心文件

### stock_query_assistant.py
主程序文件，包含：
- 股票查询助手的主要逻辑
- SQL查询工具实现
- ARIMA预测工具实现
- Web界面配置
- MCP服务器集成

### requirements.txt
项目依赖包列表，包括：
- qwen-agent: AI Agent框架
- dashscope: 通义千问API
- pandas: 数据处理
- sqlalchemy: 数据库连接
- matplotlib: 数据可视化
- statsmodels: ARIMA模型
- 其他依赖...

### faq.txt
常见问题和使用说明文档

## 目录说明

### image_show/
存储程序生成的图表文件
- stock_*.png: 股票数据可视化图表
- arima_*.png: ARIMA预测结果图表

### workspace/
工作目录（已忽略，不提交到Git）

## 配置文件

### .env (需要创建)
环境变量配置文件，包含：
- DASHSCOPE_API_KEY: 通义千问API密钥

## 数据库

需要MySQL数据库，包含stock_price表

