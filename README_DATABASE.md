# 个人画像数据库系统

基于SQLite和MCP协议的个人思维模式和行为特征数据管理系统。

## 📋 目录

- [系统概述](#系统概述)
- [功能特性](#功能特性)
- [数据库结构](#数据库结构)
- [安装和配置](#安装和配置)
- [使用方法](#使用方法)
- [MCP工具说明](#mcp工具说明)
- [API参考](#api参考)
- [示例用法](#示例用法)
- [故障排除](#故障排除)

## 🎯 系统概述

个人画像数据库系统是一个基于认知科学理论的个人数据管理工具，将个人的思维模式和行为特征按照三层八类框架进行分类存储：

### 三层八类框架

**认知层 (Cognition Layer)**
- **信念 (Belief)**: 对事物的判断性陈述和未来预测
- **洞察 (Insight)**: 通过经历获得的深层认识
- **关注点 (Focus)**: 注意力投放的领域和主题

**动机层 (Motivation Layer)**
- **长期目标 (Long-term Goal)**: 1年以上的抽象期望状态
- **短期目标 (Short-term Goal)**: 1年内的具体可衡量目标
- **偏好 (Preference)**: 个人选择时的稳定倾向性

**行为层 (Action Layer)**
- **决策 (Decision)**: 特定场景下的具体选择
- **方法论 (Methodology)**: 实现目标的系统性路径

## ✨ 功能特性

### 核心功能
- 🗄️ **完整的CRUD操作**: 增加、查询、更新、删除记录
- 🔍 **智能搜索**: 支持关键词搜索和跨表搜索
- 📊 **数据分析**: 情绪分布、主题频率、时间趋势分析
- 📈 **统计报告**: 实时数据统计和可视化摘要
- 🔄 **数据导出**: JSON格式的完整数据导出

### 技术特性
- 🚀 **高性能**: SQLite数据库，支持索引优化
- 🛡️ **数据安全**: 输入验证和SQL注入防护
- 📝 **详细日志**: 完整的操作日志记录
- 🔧 **易于扩展**: 模块化设计，支持自定义扩展
- 🌐 **MCP协议**: 标准化的工具接口

## 🗃️ 数据库结构

### 表结构说明

所有表都包含以下基础字段：
- `id`: 主键，自动递增
- `content`: 记录内容（必填）
- `related`: 相关主题标签（JSON数组格式）
- `emotion`: 情绪标签（积极/消极/中性等）
- `create_time`: 创建时间
- `update_time`: 更新时间

### 特殊字段

**长期目标表 (long_term_goals)**
- `status`: 状态（active/completed/paused/cancelled）

**短期目标表 (short_term_goals)**
- `status`: 状态
- `deadline`: 截止日期

**偏好表 (preferences)**
- `strength`: 偏好强度（1-10）

**决策表 (decisions)**
- `context`: 决策背景
- `outcome`: 决策结果

**方法论表 (methodologies)**
- `category`: 方法论分类
- `effectiveness`: 有效性评分（1-10）

## 🚀 安装和配置

### 1. 环境要求
- Python 3.8+
- 已安装的依赖包（见requirements.txt）

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行测试
```bash
python run_tests.py
```

### 4. 启动MCP服务器
```bash
python run_server.py
```

## 📖 使用方法

### 基础使用

#### 1. 直接使用数据库类
```python
from src.database import PersonalProfileDatabase

# 初始化数据库
db = PersonalProfileDatabase("my_profile.db")

# 添加信念记录
belief_data = {
    "content": "持续学习是成功的关键",
    "related": ["学习", "成长", "成功"],
    "emotion": "积极"
}
record_id = db.insert_record("beliefs", belief_data)

# 查询记录
records = db.get_records("beliefs", limit=10)

# 搜索记录
results = db.search_records("beliefs", "学习")
```

#### 2. 使用MCP工具
通过MCP协议调用工具（需要MCP客户端）：

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

## 🛠️ MCP工具说明

### 1. add_record
**功能**: 添加新记录到指定表
**参数**:
- `table_name`: 表名（必填）
- `content`: 记录内容（必填）
- `related`: 相关主题数组（必填）
- `emotion`: 情绪标签（可选，默认"中性"）
- `extra_fields`: 额外字段（可选）

### 2. get_records
**功能**: 获取记录列表
**参数**:
- `table_name`: 表名（必填）
- `limit`: 返回记录数（可选，默认20）
- `offset`: 偏移量（可选，默认0）
- `order_by`: 排序字段（可选，默认"create_time DESC"）

### 3. search_records
**功能**: 搜索记录
**参数**:
- `keyword`: 搜索关键词（必填）
- `table_name`: 表名（可选，默认"all"搜索所有表）
- `limit`: 返回记录数（可选，默认20）

### 4. update_record
**功能**: 更新指定记录
**参数**:
- `table_name`: 表名（必填）
- `record_id`: 记录ID（必填）
- `content`: 新内容（可选）
- `related`: 新相关主题（可选）
- `emotion`: 新情绪标签（可选）
- `extra_fields`: 其他字段（可选）

### 5. delete_record
**功能**: 删除指定记录
**参数**:
- `table_name`: 表名（必填）
- `record_id`: 记录ID（必填）

### 6. get_statistics
**功能**: 获取数据库统计信息
**参数**: 无

### 7. get_recent_records
**功能**: 获取最近的记录
**参数**:
- `days`: 天数（可选，默认7天）
- `limit`: 记录数限制（可选，默认50）

### 8. analyze_patterns
**功能**: 分析数据模式
**参数**:
- `analysis_type`: 分析类型（可选）
  - `emotion_distribution`: 情绪分布
  - `topic_frequency`: 主题频率
  - `time_trends`: 时间趋势
  - `goal_progress`: 目标进度
- `time_range`: 分析时间范围天数（可选，默认30天）

## 📚 API参考

### 数据库类方法

#### PersonalProfileDatabase

```python
class PersonalProfileDatabase:
    def __init__(self, db_path: str = "personal_profile.db")
    def insert_record(self, table_name: str, data: Dict[str, Any]) -> int
    def get_records(self, table_name: str, limit: int = 100, offset: int = 0, order_by: str = "create_time DESC") -> List[Dict[str, Any]]
    def search_records(self, table_name: str, keyword: str, limit: int = 50) -> List[Dict[str, Any]]
    def update_record(self, table_name: str, record_id: int, data: Dict[str, Any]) -> bool
    def delete_record(self, table_name: str, record_id: int) -> bool
    def get_statistics(self) -> Dict[str, int]
```

## 💡 示例用法

### 示例1: 记录学习心得
```python
# 添加洞察记录
insight_data = {
    "content": "通过实践发现，番茄工作法确实能提高专注度",
    "related": ["学习方法", "专注", "效率"],
    "emotion": "积极"
}
db.insert_record("insights", insight_data)

# 添加对应的方法论
methodology_data = {
    "content": "使用25分钟专注+5分钟休息的番茄工作法",
    "related": ["时间管理", "专注", "效率"],
    "emotion": "积极",
    "category": "时间管理",
    "effectiveness": 8
}
db.insert_record("methodologies", methodology_data)
```

### 示例2: 设定和跟踪目标
```python
# 设定短期目标
short_goal = {
    "content": "三个月内完成Python高级编程课程",
    "related": ["学习", "编程", "Python"],
    "emotion": "积极",
    "status": "active",
    "deadline": "2024-06-01"
}
db.insert_record("short_term_goals", short_goal)

# 设定长期目标
long_goal = {
    "content": "成为全栈开发工程师",
    "related": ["职业发展", "编程", "技能"],
    "emotion": "积极",
    "status": "active"
}
db.insert_record("long_term_goals", long_goal)
```

### 示例3: 记录决策过程
```python
# 记录技术选择决策
decision_data = {
    "content": "选择React而不是Vue作为前端框架",
    "related": ["技术选择", "前端", "React"],
    "emotion": "中性",
    "context": "新项目技术栈选择",
    "outcome": "团队更熟悉React，开发效率更高"
}
db.insert_record("decisions", decision_data)
```

### 示例4: 数据分析
```python
# 获取统计信息
stats = db.get_statistics()
print(f"总记录数: {sum(stats.values())}")

# 搜索特定主题
learning_records = db.search_records("all", "学习")
print(f"找到 {len(learning_records)} 条关于学习的记录")

# 获取最近的记录
recent = db.get_records("beliefs", limit=5, order_by="create_time DESC")
```

## 🔧 故障排除

### 常见问题

#### 1. 数据库文件权限问题
```bash
# 确保数据库文件有读写权限
chmod 644 personal_profile.db
```

#### 2. 依赖包安装问题
```bash
# 升级pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

#### 3. MCP服务器启动失败
```bash
# 检查Python路径
python --version

# 检查模块导入
python -c "from src.database import PersonalProfileDatabase; print('导入成功')"
```

#### 4. 数据库连接问题
- 检查数据库文件路径是否正确
- 确保有足够的磁盘空间
- 检查文件系统权限

### 日志调试

启用详细日志：
```bash
export LOG_LEVEL=DEBUG
python run_server.py
```

### 性能优化

1. **定期清理**: 删除不需要的旧记录
2. **索引优化**: 系统已自动创建时间索引
3. **批量操作**: 使用事务进行批量插入

## 📄 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 支持

如有问题，请通过以下方式联系：
- 提交GitHub Issue
- 查看文档和示例代码
- 运行测试脚本验证环境 