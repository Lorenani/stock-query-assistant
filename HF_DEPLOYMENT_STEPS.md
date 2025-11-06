# Hugging Face Spaces 部署步骤

## 📋 准备工作

### 1. 检查文件
确保以下文件已准备好：
- ✅ `app.py` - Hugging Face Spaces 入口文件
- ✅ `stock_query_assistant.py` - 主程序
- ✅ `requirements.txt` - 依赖列表
- ✅ `README_HF.md` - Hugging Face Spaces 的 README（会自动重命名为 README.md）
- ✅ `faq.txt` - 使用说明

### 2. 提交到GitHub（如果还没提交）
```bash
git add app.py README_HF.md
git commit -m "Add Hugging Face Spaces deployment files"
git push
```

## 🚀 部署步骤

### 步骤 1：创建 Hugging Face 账号
1. 访问 https://huggingface.co/
2. 点击右上角 "Sign Up" 注册账号
3. 验证邮箱并登录

### 步骤 2：创建 Space
1. 访问 https://huggingface.co/new-space
2. 填写信息：
   - **Space name**: `stock-query-assistant`（或您喜欢的名字）
   - **SDK**: 选择 `Gradio`
   - **Hardware**: 选择 `CPU basic`（免费）或 `CPU upgrade`（如果需要）
   - **Visibility**: 选择 `Public`（公开）
3. 点击 "Create Space"

### 步骤 3：连接 GitHub 仓库（推荐方式）

#### 方法A：通过 Git 上传
1. 在 Space 页面，点击 "Files and versions" 标签
2. 点击 "Add file" → "Upload files"
3. 上传以下文件：
   - `app.py`
   - `stock_query_assistant.py`
   - `requirements.txt`
   - `faq.txt`
   - `README_HF.md`（上传后会自动重命名为 README.md）

#### 方法B：通过 Git 命令行（推荐）
1. 在 Space 页面，找到 "Clone repository" 部分
2. 复制 Git URL（类似：`https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant`）
3. 在本地执行：
```bash
cd "/Users/lorena/Downloads/AI大模型/交互式BI报表"

# 添加 Hugging Face 远程仓库
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant

# 推送代码
git push hf main
```

### 步骤 4：配置环境变量
1. 在 Space 页面，点击 "Settings" 标签
2. 找到 "Repository secrets" 部分
3. 点击 "New secret"
4. 添加以下环境变量：
   - **Name**: `DASHSCOPE_API_KEY`
   - **Value**: 您的通义千问API密钥
5. 点击 "Add secret"

### 步骤 5：等待构建
1. Hugging Face 会自动检测代码更改
2. 开始构建（Build）过程
3. 查看构建日志，确认没有错误
4. 构建完成后，应用会自动启动

### 步骤 6：访问应用
构建完成后，您会看到：
- **应用链接**: `https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant`
- 这个链接是永久的，可以分享给任何人

## 🔍 故障排查

### 问题1：构建失败
- 检查 `requirements.txt` 是否完整
- 查看构建日志中的错误信息
- 确认所有依赖包名称正确

### 问题2：应用无法启动
- 检查 `app.py` 文件是否正确
- 确认环境变量已配置
- 查看运行日志

### 问题3：API调用失败
- 确认 `DASHSCOPE_API_KEY` 环境变量已设置
- 检查API密钥是否有效
- 查看错误日志

## 📝 更新应用

如果需要更新代码：

```bash
# 修改代码后
git add .
git commit -m "Update: 更新功能"
git push hf main  # 推送到 Hugging Face
```

Hugging Face 会自动重新构建和部署。

## 🎯 在 README.md 中添加链接

在 GitHub 仓库的 README.md 中添加：

```markdown
## 🌐 在线演示

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant)

🔗 访问链接：https://huggingface.co/spaces/YOUR_USERNAME/stock-query-assistant
```

## ✅ 完成检查清单

- [ ] Hugging Face 账号已创建
- [ ] Space 已创建
- [ ] 代码已上传
- [ ] 环境变量已配置
- [ ] 构建成功
- [ ] 应用可以正常访问
- [ ] 在 GitHub README 中添加了链接

---

**提示**：部署完成后，这个链接可以永久使用，非常适合添加到简历中！

