# psyas：心理分析聊天助手（开发中）  

### 🌟 项目目标  
用 **Flask + Vue** 打造一个能「引导用户对话、结合心理学知识做情绪/问题分析」的聊天助手，帮大家更清晰地梳理心理状态。  


### 👋 新人快速上手（重点！降低参与门槛）  
若你是第一次接触项目，想跑通代码或参与开发，按以下步骤操作：  

#### 1. 选运行方式（推荐 Docker，最简单）  
```bash
# 开发环境（实时热更新，适合改代码）
docker compose up flask-dev  

# 生产环境（稳定版，适合体验功能）
docker compose up flask-prod  

```
#### 2. 初始化数据库（必须！否则对话功能无法使用）
无论用 Docker 还是本地运行，均需初始化数据库：
```bash
# Docker 方式
docker compose run --rm manage db init  
docker compose run --rm manage db migrate  
docker compose run --rm manage db upgrade  

# 本地运行方式
flask db init  
flask db migrate  
flask db upgrade  
```
#### 3. 修改前端（Vue 代码在 frontend/ 目录）
```bash
cd frontend  
npm install  # 安装依赖  
npm run dev  # 启动前端热更新  

```
### 🛠️协作流程
#### 1.分支规范
master/main：生产环境分支，存放可部署的稳定代码，受保护，仅通过 PR 合并。​

develop：开发集成分支，用于功能集成和测试，从 master 创建。​

feature/xxx：功能分支，从 develop 创建，命名格式为 feature / 功能描述，用于开发新功能。​

bugfix/xxx：修复分支，从 develop 创建，命名格式为 bugfix / 问题描述，用于修复开发中的 bug。​

#### 2.提 PR 流程
1）同步远程分支信息（避免代码冲突）：
```bash
git fetch origin  # 拉取远程所有分支最新信息 

```
2）切换到 develop 分支并拉取最新代码
```bash
git checkout develop  
git pull origin develop  
```
3）创建个人开发分支（功能 / 修复分支）：
```bash
# 开发新功能用 feature/xxx 命名
git checkout -b feature/你的功能描述  
# 修复 Bug 用 bugfix/xxx 命名
git checkout -b bugfix/你的问题描述  
```
4）开发完成后，提交代码：
```bash
git add .  # 暂存所有修改
git commit -m "清晰描述修改：如‘实现对话引导关键词匹配’‘修复数据库连接超时’"  
```
5）推送分支到远程仓库：
```bash
git push -u origin 你的分支名  # 例：git push -u origin feature/对话引导
```
6）发起 PR 并等待审核：
打开 GitHub 仓库页面，找到 “Pull requests” → “New pull request”

选择 “base: develop”（合并到开发分支）、“compare: 你的分支名”

填写 PR 标题（如 “feat: 实现对话引导功能”）和描述（改了什么、解决什么问题）

提交后等待管理员审核，通过后分支会自动合并到 develop

### 📦 核心功能
目前已实现：

✅ 前后端分离架构（Flask + Vue）


待开发：
⏳ 用户对话存储（数据库记录用户输入、助手回复）
⏳ 简单引导问题（关键词触发心理学追问，如 “提到‘烦躁’时追问具体事件”）
⏳ 对接 NLP 服务（意图识别、情绪分析）
⏳ 心理学知识库关联（分析时自动匹配知识）
### 🌟 补充说明
这是我第一次在 GitHub 独立开源项目，经验尚在积累～若你：

遇到代码运行问题 → 直接开 Issue 提问（记得贴报错日志！） 

有功能建议（如 “想让助手支持 XX 心理场景”） → 去 Discussion 区交流

想直接贡献代码 → 提 PR 前，可先在 Issue 说明想做内容，避免重复开发

一起把这个 “心理分析助手” 做得更有价值吧！
