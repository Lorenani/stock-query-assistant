# 部署指南 - 创建公开访问链接

## 🚀 方案一：使用 Gradio Share（快速，临时链接）

### 使用方法
代码中已经设置了 `share=True`，运行程序后会自动生成一个公网链接。

```bash
python stock_query_assistant.py
```

运行后会显示类似这样的链接：
```
Running on public URL: https://xxxxx.gradio.live
```

**优点**：
- ✅ 快速简单，无需额外配置
- ✅ 免费使用
- ✅ 自动生成HTTPS链接

**缺点**：
- ⚠️ 链接有时效性（通常72小时）
- ⚠️ 需要本地运行程序

---

## 🌐 方案二：部署到 Hugging Face Spaces（推荐，永久链接）

### 步骤 1：创建 Hugging Face 账号
1. 访问 https://huggingface.co/
2. 注册账号并登录

### 步骤 2：创建 Space
1. 访问 https://huggingface.co/new-space
2. 填写信息：
   - Space name: `stock-query-assistant`
   - SDK: 选择 `Gradio`
   - Visibility: `Public`
3. 点击 "Create Space"

### 步骤 3：准备部署文件
在项目中创建以下文件：

#### `app.py` (Hugging Face Spaces 入口文件)
```python
import os
from stock_query_assistant import app_gui

if __name__ == '__main__':
    app_gui()
```

#### `README.md` (Hugging Face Spaces 会自动读取)
```markdown
---
title: 智能股票查询助手
emoji: 📈
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---
```

### 步骤 4：上传代码
1. 在 Hugging Face Space 页面，点击 "Files and versions"
2. 上传项目文件（或使用 Git）
3. 在 Settings → Secrets 中添加环境变量：
   - `DASHSCOPE_API_KEY`: 您的API密钥

### 步骤 5：等待构建
Hugging Face 会自动构建和部署，完成后会生成永久链接：
```
https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant
```

---

## ☁️ 方案三：部署到 Render（免费，永久链接）

### 步骤 1：创建 Render 账号
访问 https://render.com/ 注册账号

### 步骤 2：创建 Web Service
1. 连接 GitHub 仓库
2. 选择仓库 `Lorenani/stock-query-assistant`
3. 配置：
   - Name: `stock-query-assistant`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python stock_query_assistant.py`
4. 添加环境变量：
   - `DASHSCOPE_API_KEY`: 您的API密钥

### 步骤 3：部署
点击 "Create Web Service"，等待部署完成。

---

## 📝 推荐方案对比

| 方案 | 难度 | 链接类型 | 费用 | 推荐度 |
|------|------|---------|------|--------|
| Gradio Share | ⭐ 简单 | 临时（72小时） | 免费 | ⭐⭐⭐ |
| Hugging Face Spaces | ⭐⭐ 中等 | 永久 | 免费 | ⭐⭐⭐⭐⭐ |
| Render | ⭐⭐⭐ 较难 | 永久 | 免费（有限制） | ⭐⭐⭐⭐ |

## 🎯 简历展示建议

### 使用 Hugging Face Spaces（最推荐）
- 链接格式：`https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant`
- 优点：永久链接，专业展示，支持自动更新
- 适合：简历、作品集展示

### 在 README.md 中添加
```markdown
## 🌐 在线演示

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant)

访问链接：https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant
```

---

## ⚙️ 环境变量配置

无论使用哪种方案，都需要配置环境变量：

- `DASHSCOPE_API_KEY`: 通义千问API密钥
- `TAVILY_API_KEY`: Tavily搜索API密钥（可选）

**注意**：不要将API密钥提交到代码仓库！

---

## 🔧 故障排查

### 问题1：Gradio Share 链接无法访问
- 检查网络连接
- 确认程序正在运行
- 尝试重新运行生成新链接

### 问题2：Hugging Face 部署失败
- 检查 `requirements.txt` 是否完整
- 查看构建日志
- 确认环境变量已配置

### 问题3：Render 部署超时
- 检查启动命令是否正确
- 增加构建超时时间
- 查看日志排查问题

---

## 📞 需要帮助？

如果遇到问题，可以：
1. 查看 Hugging Face Spaces 文档
2. 查看 Render 文档
3. 在 GitHub Issues 中提问

