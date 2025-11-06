# 📈 智能股票查询助手 (Stock Query Assistant)

一个基于大语言模型的交互式股票查询与分析系统，支持股票历史价格查询、多股票对比分析、价格预测和热点新闻搜索。

## ✨ 项目特色

- 🤖 **AI驱动的智能对话**：基于通义千问大模型，支持自然语言交互
- 📊 **多维度数据分析**：历史价格查询、多股票对比、可视化图表
- 🔮 **时间序列预测**：使用ARIMA模型预测未来股票价格走势
- 📰 **实时新闻搜索**：集成Tavily和必应搜索，获取股票热点新闻
- 🎨 **现代化Web界面**：美观的圆润按钮设计，流畅的用户体验

## 🚀 核心功能

### 1. 股票历史价格查询
- 支持按时间范围查询股票的开盘价、收盘价、最高价、最低价
- 自动生成可视化图表（折线图/柱状图）
- 支持成交量、成交额等指标统计

### 2. 多支股票对比分析
- 同时对比多支股票的价格走势
- 计算涨跌幅对比
- 生成对比分析图表

### 3. 股票价格预测（ARIMA）
- 使用ARIMA(5,1,5)时间序列模型
- 基于过去一年的历史数据
- 预测未来N天的收盘价
- 可视化历史价格与预测价格

### 4. 热点新闻搜索
- 集成Tavily和必应搜索API
- 自动切换备选搜索源
- 实时获取股票相关新闻和市场动态

## 🛠️ 技术栈

- **AI框架**: Qwen Agent (通义千问)
- **后端**: Python 3.11+
- **数据库**: MySQL
- **数据可视化**: Matplotlib
- **时间序列分析**: Statsmodels (ARIMA)
- **Web界面**: Qwen Agent WebUI
- **搜索服务**: Tavily API, 必应搜索

## 📦 安装与配置

### 1. 环境要求
- Python 3.11+
- MySQL数据库
- Node.js (用于MCP服务器)

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 环境变量配置

创建 `.env` 文件或设置环境变量：

```bash
export DASHSCOPE_API_KEY='your_dashscope_api_key'
```

### 4. 数据库配置

确保MySQL数据库中有 `stock_price` 表，表结构参考：

```sql
CREATE TABLE stock_price (
    id INT AUTO_INCREMENT PRIMARY KEY,
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
```

### 5. 运行项目

```bash
python stock_query_assistant.py
```

访问 `http://127.0.0.1:7860` 使用Web界面。

## 📖 使用示例

### 查询历史价格
```
查询2024年全年贵州茅台的收盘价走势
```

### 多股票对比
```
对比2024年中芯国际和贵州茅台的涨跌幅
```

### 价格预测
```
预测贵州茅台未来7天的收盘价
```

### 热点新闻
```
贵州茅台最近的热点新闻
```

## 📁 项目结构

```
交互式BI报表/
├── stock_query_assistant.py    # 主程序文件
├── requirements.txt             # 依赖包列表
├── faq.txt                     # 常见问题说明
├── README.md                   # 项目说明文档
├── .gitignore                  # Git忽略文件
└── image_show/                  # 生成的图表目录
    ├── stock_*.png             # 股票数据图表
    └── arima_*.png             # ARIMA预测图表
```

## 🔧 核心模块说明

### 1. SQL查询工具 (exc_sql)
- 执行SQL查询语句
- 自动生成可视化图表
- 支持数据统计信息展示

### 2. ARIMA预测工具 (arima_stock)
- 获取历史收盘价数据
- ARIMA(5,1,5)模型训练
- 生成预测结果和可视化图表

### 3. MCP搜索工具
- Tavily搜索（主要）
- 必应搜索（备选）
- 自动故障切换

## 🎯 技术亮点

1. **智能工具调用**：基于LLM自动选择合适的工具
2. **容错机制**：搜索工具自动切换，提高可用性
3. **数据可视化**：智能选择图表类型（折线图/柱状图）
4. **中文支持**：完整的中文显示和交互支持
5. **模块化设计**：工具可扩展，易于维护

## 📊 项目展示

### 功能演示
- ✅ 股票历史价格查询与可视化
- ✅ 多股票对比分析
- ✅ ARIMA时间序列预测
- ✅ 热点新闻搜索
- ✅ 现代化Web界面

## 🔐 注意事项

- API密钥请妥善保管，不要提交到代码仓库
- 数据库连接信息需要根据实际情况配置
- 首次运行需要安装MCP服务器依赖（通过npx自动安装）

## 📝 开发日志

- ✅ 实现股票历史价格查询功能
- ✅ 实现多股票对比分析功能
- ✅ 集成ARIMA价格预测模型
- ✅ 集成Tavily和必应搜索
- ✅ 优化Web界面样式
- ✅ 添加容错机制

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目仅供学习和研究使用。

## 👤 作者

[您的名字]

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！

