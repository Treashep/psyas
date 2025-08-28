# Apifox 测试指南

## 快速开始

### 1. 准备工作

确保服务正在运行：
```bash
# 在项目目录下
cd d:\newwork\psyas

# 初始化数据（创建测试用户和引导问题）
python init_data.py

# 启动 Flask 服务
python -m psyas.app
# 或使用 Docker: docker compose up flask-dev
```

### 2. 导入 Apifox 配置

1. 打开 Apifox
2. 创建新项目或选择现有项目
3. 点击"导入" > "从文件导入"
4. 选择项目根目录下的 `apifox_collection.json` 文件
5. 导入成功后，您会看到以下接口分组：
   - **对话服务** (3个接口)
   - **分析服务** (5个接口)  
   - **测试接口** (2个接口)

### 3. 环境变量配置

导入后，Apifox 会自动配置以下环境变量：
- `baseUrl`: http://localhost:5000
- `testUserId`: 1

您可以在"环境管理"中修改这些值。

## 测试流程建议

### 第一步：验证服务状态
1. **对话服务状态** - GET `/api/conversation/status`
2. **分析服务状态** - GET `/api/analysis/status`
3. **Hello测试** - GET `/test/hello`

### 第二步：测试核心业务流程
1. **发送对话消息** - POST `/api/conversation/chat`
   ```json
   {
     "user_id": 1,
     "message": "我最近感觉很焦虑，工作压力很大"
   }
   ```

2. **分析对话** - POST `/api/analysis/analyze`
   ```json
   {
     "user_id": 1
   }
   ```

### 第三步：验证查询接口
1. **获取对话历史** - GET `/api/conversation/history/1`
2. **获取分析结果列表** - GET `/api/analysis/results/1`
3. **获取分析摘要** - GET `/api/analysis/summary/1`

## 测试数据示例

### 对话消息示例
```json
// 焦虑相关
{
  "user_id": 1,
  "message": "我最近很担心工作的事情，总是睡不好"
}

// 压力相关
{
  "user_id": 1,
  "message": "感觉压力好大，每天都很累，不知道该怎么办"
}

// 情感相关
{
  "user_id": 1,
  "message": "和男朋友吵架了，感觉很难过"
}

// 快乐相关
{
  "user_id": 1,
  "message": "今天升职了，特别开心！"
}
```

### 预期响应格式

#### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    // 具体数据内容
  }
}
```

#### 错误响应
```json
{
  "code": 400/404/500,
  "message": "错误描述",
  "error": "详细错误信息"
}
```

## 接口详细说明

### 对话接口 POST `/api/conversation/chat`
- **功能**: 处理用户输入，返回智能引导回复
- **必需字段**: user_id, message
- **返回**: 对话ID、助手回复、创建时间

### 分析接口 POST `/api/analysis/analyze`  
- **功能**: 分析用户对话，提取情绪和问题
- **必需字段**: user_id
- **可选字段**: conversation_id（不提供则分析最新对话）
- **返回**: 分析ID、情绪、核心问题、结论

### 历史查询接口
- **对话历史**: GET `/api/conversation/history/{user_id}?limit=10`
- **分析结果**: GET `/api/analysis/results/{user_id}?limit=10`
- **分析详情**: GET `/api/analysis/detail/{user_id}/{analysis_id}`
- **分析摘要**: GET `/api/analysis/summary/{user_id}`

## 故障排除

### 1. 连接拒绝错误
- 确保 Flask 服务正在运行
- 检查端口 5000 是否被占用
- 验证 baseUrl 环境变量

### 2. 404 错误
- 检查 URL 路径是否正确
- 确认用户ID存在

### 3. 500 内部错误
- 检查数据库连接
- 查看 Flask 控制台错误日志
- 确认已运行 `python init_data.py`

## 数据库依赖

测试前请确保已运行数据初始化：
```bash
python init_data.py
```

这会创建：
- 测试用户（ID: 1, 用户名: testuser）
- 25个引导问题，覆盖各种心理场景

## 高级测试场景

### 1. 批量对话测试
连续发送多条不同情绪的消息，观察引导问题的变化

### 2. 分析历史测试  
发送多条对话后，检查分析摘要中的情绪分布统计

### 3. 错误处理测试
- 发送空消息
- 使用不存在的用户ID
- 分析不存在的对话ID

### 4. 边界值测试
- 超长消息内容
- 特殊字符消息
- 数字和英文混合消息

通过 Apifox 可以轻松保存测试用例，建立自动化测试套件！