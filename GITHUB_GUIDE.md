# GitHub 上传指南

## 📋 准备工作

### 1. 检查文件
确保以下文件已准备好：
- ✅ `stock_query_assistant.py` - 主程序
- ✅ `requirements.txt` - 依赖列表
- ✅ `README.md` - 项目说明
- ✅ `.gitignore` - Git忽略文件
- ✅ `faq.txt` - 使用说明

### 2. 清理敏感信息
检查代码中是否包含：
- ❌ API密钥（应该使用环境变量）
- ❌ 数据库密码（应该使用环境变量）
- ❌ 个人敏感信息

## 🚀 上传步骤

### 方法一：使用Git命令行（推荐）

#### 1. 初始化Git仓库
```bash
cd "/Users/lorena/Downloads/AI大模型/交互式BI报表"
git init
```

#### 2. 添加文件
```bash
# 添加所有文件（.gitignore会自动排除不需要的文件）
git add .

# 或者选择性添加
git add stock_query_assistant.py
git add requirements.txt
git add README.md
git add .gitignore
git add faq.txt
```

#### 3. 提交代码
```bash
git commit -m "Initial commit: 智能股票查询助手项目"
```

#### 4. 在GitHub创建仓库
1. 登录GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - Repository name: `stock-query-assistant` (或您喜欢的名字)
   - Description: `基于大语言模型的智能股票查询与分析系统`
   - 选择 Public（公开）或 Private（私有）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
4. 点击 "Create repository"

#### 5. 连接远程仓库并推送
```bash
# 添加远程仓库（将YOUR_USERNAME替换为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/stock-query-assistant.git

# 或者使用SSH（如果您配置了SSH密钥）
# git remote add origin git@github.com:YOUR_USERNAME/stock-query-assistant.git

# 推送代码
git branch -M main
git push -u origin main
```

### 方法二：使用GitHub Desktop（图形界面）

1. 下载安装 [GitHub Desktop](https://desktop.github.com/)
2. 登录您的GitHub账号
3. 点击 "File" → "Add Local Repository"
4. 选择项目文件夹
5. 填写提交信息并提交
6. 点击 "Publish repository" 发布到GitHub

### 方法三：使用GitHub网页直接上传

1. 在GitHub创建新仓库
2. 点击 "uploading an existing file"
3. 拖拽文件到页面
4. 填写提交信息
5. 点击 "Commit changes"

## 📝 完善项目信息

### 1. 添加项目描述
在GitHub仓库页面：
- 点击 "Settings" → "General"
- 在 "Description" 中添加项目描述
- 添加 Topics（标签）：`python`, `ai`, `stock-analysis`, `arima`, `llm`, `chatbot`

### 2. 添加README徽章（可选）
在README.md顶部添加：

```markdown
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
```

### 3. 添加截图（推荐）
1. 运行程序并截图
2. 创建 `docs/` 或 `screenshots/` 目录
3. 将截图放入目录
4. 在README.md中引用截图

示例：
```markdown
## 📸 界面截图

![主界面](screenshots/main_interface.png)
![预测结果](screenshots/prediction_result.png)
```

## 🔒 安全注意事项

### 必须忽略的文件
确保 `.gitignore` 包含：
- `.env` - 环境变量文件
- `*.key` - 密钥文件
- `*.xlsx` - 可能包含敏感数据的Excel文件
- `笔记*.txt` - 个人笔记

### 检查已提交的敏感信息
如果之前不小心提交了敏感信息：
```bash
# 查看提交历史
git log

# 如果发现敏感信息，需要重写历史（谨慎操作）
# 或者直接删除仓库重新创建
```

## 📌 后续维护

### 更新代码
```bash
# 修改代码后
git add .
git commit -m "更新：添加新功能"
git push
```

### 添加新功能分支
```bash
# 创建新分支
git checkout -b feature/new-feature

# 开发完成后
git add .
git commit -m "添加新功能"
git push origin feature/new-feature

# 在GitHub上创建Pull Request
```

## 🎯 简历展示建议

### 1. 项目描述
在简历中可以这样描述：
> **智能股票查询助手** | Python, AI Agent, 时间序列分析
> - 基于通义千问大模型开发的交互式股票分析系统
> - 实现ARIMA时间序列模型进行股票价格预测
> - 集成多源搜索API，支持实时新闻获取
> - 开发Web界面，支持自然语言交互和可视化展示

### 2. 技术栈突出
- 大语言模型应用（LLM）
- 时间序列分析（ARIMA）
- 数据可视化
- Web应用开发
- API集成

### 3. GitHub链接
在简历中直接添加GitHub仓库链接：
```
GitHub: https://github.com/YOUR_USERNAME/stock-query-assistant
```

## ✅ 检查清单

上传前确认：
- [ ] README.md 内容完整
- [ ] .gitignore 配置正确
- [ ] 代码中无敏感信息
- [ ] requirements.txt 完整
- [ ] 项目可以正常运行
- [ ] 添加了项目截图（可选）
- [ ] 仓库设置为Public（如果想展示）

---

**提示**：首次上传后，建议邀请朋友或同事查看，确保项目展示效果良好！

