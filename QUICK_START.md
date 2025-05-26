# 个人画像数据库 - 快速启动指南

## 🚀 5分钟快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行测试（可选）
```bash
python run_tests.py
```

### 3. 启动MCP服务器
```bash
python run_server.py
```

## 📝 基础使用示例

### 直接使用Python API

```python
from src.database import PersonalProfileDatabase

# 初始化数据库
db = PersonalProfileDatabase()

# 添加一个信念
belief = {
    "content": "持续学习是成功的关键",
    "related": ["学习", "成长", "成功"],
    "emotion": "积极"
}
record_id = db.insert_record("beliefs", belief)
print(f"添加信念记录，ID: {record_id}")

# 查询所有信念
beliefs = db.get_records("beliefs")
print(f"共有 {len(beliefs)} 条信念记录")

# 搜索相关记录
results = db.search_records("all", "学习")
print(f"找到 {len(results)} 条包含'学习'的记录")
```

## 🎯 常用操作

### 添加不同类型的记录

```python
# 添加洞察
insight = {
    "content": "通过实践发现，早起确实能提高一天的效率",
    "related": ["习惯", "效率", "时间管理"],
    "emotion": "积极"
}
db.insert_record("insights", insight)

# 添加短期目标
goal = {
    "content": "本月完成3个编程项目",
    "related": ["编程", "项目", "目标"],
    "emotion": "积极",
    "status": "active",
    "deadline": "2024-06-30"
}
db.insert_record("short_term_goals", goal)

# 添加方法论
method = {
    "content": "使用番茄工作法提高专注度",
    "related": ["时间管理", "专注", "效率"],
    "emotion": "积极",
    "category": "时间管理",
    "effectiveness": 8
}
db.insert_record("methodologies", method)
```

### 数据分析

```python
# 获取统计信息
stats = db.get_statistics()
print("数据库统计:")
for table, count in stats.items():
    print(f"  {table}: {count} 条记录")

# 搜索特定主题
tech_records = db.search_records("all", "技术")
print(f"技术相关记录: {len(tech_records)} 条")
```

## 🛠️ MCP工具使用

如果您使用支持MCP协议的客户端，可以通过以下工具操作数据库：

### 添加记录
```json
{
  "tool": "add_record",
  "arguments": {
    "table_name": "belief",
    "content": "AI将改变未来的工作方式",
    "related": ["AI", "未来", "工作"],
    "emotion": "积极"
  }
}
```

### 搜索记录
```json
{
  "tool": "search_records", 
  "arguments": {
    "keyword": "学习",
    "limit": 10
  }
}
```

### 获取统计信息
```json
{
  "tool": "get_statistics",
  "arguments": {}
}
```

## 📊 数据表说明

| 表名 | 中文名 | 用途 | 特殊字段 |
|------|--------|------|----------|
| beliefs | 信念 | 存储对事物的判断和预测 | - |
| insights | 洞察 | 存储通过经历获得的认识 | - |
| focuses | 关注点 | 存储关注的领域和主题 | - |
| long_term_goals | 长期目标 | 存储1年以上的目标 | status |
| short_term_goals | 短期目标 | 存储1年内的目标 | status, deadline |
| preferences | 偏好 | 存储个人选择倾向 | strength |
| decisions | 决策 | 存储具体的选择 | context, outcome |
| methodologies | 方法论 | 存储系统性的方法 | category, effectiveness |

## 🔍 搜索技巧

- **关键词搜索**: 在内容和相关标签中搜索
- **跨表搜索**: 使用 `table_name="all"` 搜索所有表
- **精确匹配**: 使用完整的词语获得更准确的结果

## 📈 分析功能

系统提供多种数据分析功能：

1. **情绪分布**: 分析不同情绪标签的分布
2. **主题频率**: 统计最常出现的主题标签
3. **时间趋势**: 查看记录创建的时间模式
4. **目标进度**: 分析目标的完成状态

## 🎨 自定义扩展

### 添加自定义字段
```python
# 为决策记录添加自定义字段
decision_data = {
    "content": "选择使用React框架",
    "related": ["技术", "前端", "React"],
    "emotion": "积极",
    "context": "新项目技术选型",
    "outcome": "开发效率提升",
    "confidence_level": 8,  # 自定义字段
    "impact_score": 9       # 自定义字段
}
db.insert_record("decisions", decision_data)
```

## 🔧 故障排除

### 常见问题

1. **导入错误**: 确保在项目根目录运行脚本
2. **数据库锁定**: 确保没有其他程序占用数据库文件
3. **权限问题**: 确保对数据库文件有读写权限

### 重置数据库
```python
import os
if os.path.exists("personal_profile.db"):
    os.remove("personal_profile.db")
    
# 重新初始化
db = PersonalProfileDatabase()
```

## 📚 更多资源

- 📖 [完整文档](README_DATABASE.md)
- 🧪 [测试示例](run_tests.py)
- 🔧 [配置选项](src/config.py)
- 📊 [示例数据](sample_personal_profile_export.json)

## 💡 使用建议

1. **定期记录**: 建议每天记录1-2条新的想法或经历
2. **标签一致性**: 使用一致的标签名称便于后续搜索
3. **定期回顾**: 利用搜索和分析功能定期回顾自己的思维模式
4. **数据备份**: 定期导出数据进行备份

开始您的个人画像数据管理之旅吧！🎉 