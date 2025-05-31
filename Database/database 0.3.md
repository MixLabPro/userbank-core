# Profile数据库字段详细使用指南

## 1. Persona（人物档案表）- 系统核心

### 表结构设计
```sql
CREATE TABLE persona (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT,
    personality TEXT,
    avatar_url TEXT,
    bio TEXT,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE UNIQUE INDEX idx_persona_id ON persona(id);
CREATE INDEX idx_persona_privacy ON persona(privacy_level);
```

### 字段说明
- **id**: 主键，固定为1（系统只维护一个人物档案）
- **name**: 用户姓名，如"张三"
- **gender**: 性别，影响语言风格和称呼方式
- **personality**: 性格描述，如"内向思考型，注重细节，喜欢深度分析"
- **avatar_url**: 头像链接（可选）
- **bio**: 个人简介（可选）
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 2. Category（分类体系表）

### 表结构设计
```sql
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_level TEXT NOT NULL,
    second_level TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_category_levels ON category(first_level, second_level);
CREATE INDEX idx_category_active ON category(is_active);
CREATE INDEX idx_category_privacy ON category(privacy_level);
```

### 字段说明
- **id**: 分类ID
- **first_level**: 一级目录，如"技术"、"生活"、"商业"
- **second_level**: 二级目录，如"编程开发"、"人际关系"、"投资理财"
- **description**: 分类描述
- **is_active**: 是否启用该分类
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 3. Relations（通用关联表）

### 表结构设计
```sql
CREATE TABLE relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_table TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    target_table TEXT NOT NULL,
    target_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    strength TEXT CHECK(strength IN ('strong', 'medium', 'weak')),
    note TEXT,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_relations_source ON relations(source_table, source_id);
CREATE INDEX idx_relations_target ON relations(target_table, target_id);
CREATE INDEX idx_relations_type ON relations(relation_type);
CREATE INDEX idx_relations_privacy ON relations(privacy_level);
```

### 字段说明
- **id**: 主键
- **source_table**: 源表名，如"insight"
- **source_id**: 源记录ID
- **target_table**: 目标表名，如"goal"
- **target_id**: 目标记录ID
- **relation_type**: 关联类型，如"inspired_by"、"conflicts_with"、"supports"、"parent_of"
- **strength**: 关联强度（strong/medium/weak）
- **note**: 关联说明
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 4. Viewpoint（观点表）

### 表结构设计
```sql
CREATE TABLE viewpoint (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    source_people TEXT,
    keywords TEXT,
    source_app TEXT,
    related_event TEXT,
    reference_urls TEXT,
    category_id INTEGER,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_viewpoint_source_people ON viewpoint(source_people);
CREATE INDEX idx_viewpoint_source_app ON viewpoint(source_app);
CREATE INDEX idx_viewpoint_category ON viewpoint(category_id);
CREATE INDEX idx_viewpoint_privacy ON viewpoint(privacy_level);
```

### 字段说明
- **id**: 主键
- **content**: 观点内容，如"微服务架构适合团队规模超过20人的项目"
- **source_people**: 观点来源人员，如"张三"、"技术专家李四"
- **keywords**: 关键词数组，JSON格式存储，如["微服务","架构","团队管理"]
- **source_app**: 数据来源应用，如"微信读书"、"手动输入"、"会议记录"
- **related_event**: 相关事件，如"技术分享会"、"项目复盘会议"
- **reference_urls**: 参考链接数组
- **category_id**: 分类ID
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 5. Insight（洞察表）

### 表结构设计
```sql
CREATE TABLE insight (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    source_people TEXT,
    keywords TEXT,
    source_app TEXT,
    category_id INTEGER,
    reference_urls TEXT,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_insight_source_people ON insight(source_people);
CREATE INDEX idx_insight_source_app ON insight(source_app);
CREATE INDEX idx_insight_category ON insight(category_id);
CREATE INDEX idx_insight_time ON insight(created_time);
CREATE INDEX idx_insight_privacy ON insight(privacy_level);
```

### 字段说明
- **id**: 主键
- **content**: 洞察内容，如"技术选择往往反映了团队的组织结构"
- **source_people**: 洞察来源人员，如"架构师王五"、"自己"
- **keywords**: 关键词数组，JSON格式存储，如["技术选择","组织架构","团队管理"]
- **source_app**: 数据来源应用，如"技术博客"、"项目复盘工具"
- **category_id**: 分类ID
- **reference_urls**: 参考链接
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 6. Focus（关注点表）

### 表结构设计
```sql
CREATE TABLE focus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    priority INTEGER CHECK(priority >= 1 AND priority <= 10),
    status TEXT CHECK(status IN ('active', 'paused', 'completed')),
    context TEXT,
    keywords TEXT,
    source_app TEXT,
    category_id INTEGER,
    deadline DATE,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_focus_status ON focus(status);
CREATE INDEX idx_focus_priority ON focus(priority);
CREATE INDEX idx_focus_deadline ON focus(deadline);
CREATE INDEX idx_focus_source_app ON focus(source_app);
CREATE INDEX idx_focus_privacy ON focus(privacy_level);
```

### 字段说明
- **id**: 主键
- **content**: 关注内容，如"学习Rust编程语言"
- **priority**: 优先级（1-10）
- **status**: 状态（active/paused/completed）
- **context**: 上下文，如"工作"、"个人提升"
- **keywords**: 关键词数组，JSON格式存储，如["Rust","编程","学习"]
- **source_app**: 数据来源应用，如"学习计划App"、"工作管理工具"
- **category_id**: 分类ID
- **deadline**: 截止日期
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 7. Goal（目标表）

### 表结构设计
```sql
CREATE TABLE goal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    type TEXT CHECK(type IN ('long_term', 'short_term', 'plan', 'todo')),
    deadline DATE,
    status TEXT CHECK(status IN ('planning', 'in_progress', 'completed', 'abandoned')),
    keywords TEXT,
    source_app TEXT,
    category_id INTEGER,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_goal_type ON goal(type);
CREATE INDEX idx_goal_status ON goal(status);
CREATE INDEX idx_goal_deadline ON goal(deadline);
CREATE INDEX idx_goal_category ON goal(category_id);
CREATE INDEX idx_goal_source_app ON goal(source_app);
CREATE INDEX idx_goal_privacy ON goal(privacy_level);
```

### 字段说明
- **id**: 主键
- **content**: 目标内容
- **type**: 类型
  - `long_term`: 长期目标（1年以上）
  - `short_term`: 短期目标（3个月-1年）
  - `plan`: 计划（1周-3个月）
  - `todo`: 待办事项（1周内）
- **deadline**: 截止日期
- **status**: 状态（planning/in_progress/completed/abandoned）
- **keywords**: 关键词数组，JSON格式存储，如["学习","技能提升","职业发展"]
- **source_app**: 数据来源应用，如"任务管理App"、"项目管理工具"
- **category_id**: 分类ID
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 8. Preference（偏好表）

### 表结构设计
```sql
CREATE TABLE preference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    context TEXT,
    keywords TEXT,
    source_app TEXT,
    category_id INTEGER,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_preference_context ON preference(context);
CREATE INDEX idx_preference_source_app ON preference(source_app);
CREATE INDEX idx_preference_privacy ON preference(privacy_level);
```

### 字段说明
- **id**: 主键
- **content**: 偏好内容，如"喜欢在安静环境中深度思考"
- **context**: 适用场景，如"学习时"、"工作中"
- **keywords**: 关键词数组，JSON格式存储，如["环境偏好","思考方式","工作习惯"]
- **source_app**: 数据来源应用，如"生活记录App"、"习惯追踪工具"
- **category_id**: 分类ID
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 9. Methodology（方法论表）

### 表结构设计
```sql
CREATE TABLE methodology (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    type TEXT,
    effectiveness TEXT CHECK(effectiveness IN ('proven', 'experimental', 'theoretical')),
    use_cases TEXT,
    keywords TEXT,
    source_app TEXT,
    category_id INTEGER,
    reference_urls TEXT,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_methodology_type ON methodology(type);
CREATE INDEX idx_methodology_effectiveness ON methodology(effectiveness);
CREATE INDEX idx_methodology_source_app ON methodology(source_app);
CREATE INDEX idx_methodology_privacy ON methodology(privacy_level);
```

### 字段说明
- **id**: 主键
- **content**: 方法论内容
- **type**: 类型，如"问题解决"、"决策制定"
- **effectiveness**: 有效性（proven/experimental/theoretical）
- **use_cases**: 适用场景
- **keywords**: 关键词数组，JSON格式存储，如["问题解决","方法论","工作流程"]
- **source_app**: 数据来源应用，如"知识管理工具"、"学习平台"
- **category_id**: 分类ID
- **reference_urls**: 参考链接
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 10. Prediction（预测表）

### 表结构设计
```sql
CREATE TABLE prediction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    timeframe TEXT,
    basis TEXT,
    verification_status TEXT CHECK(verification_status IN ('pending', 'correct', 'incorrect', 'partial')),
    keywords TEXT,
    source_app TEXT,
    reference_urls TEXT,
    category_id INTEGER,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_prediction_timeframe ON prediction(timeframe);
CREATE INDEX idx_prediction_status ON prediction(verification_status);
CREATE INDEX idx_prediction_source_app ON prediction(source_app);
CREATE INDEX idx_prediction_privacy ON prediction(privacy_level);
```

### 字段说明
- **id**: 主键
- **content**: 预测内容
- **timeframe**: 时间范围
- **basis**: 预测依据
- **verification_status**: 验证状态（pending/correct/incorrect/partial）
- **keywords**: 关键词数组，JSON格式存储，如["行业趋势","技术预测","市场分析"]
- **source_app**: 数据来源应用，如"行业分析工具"、"趋势预测平台"
- **reference_urls**: 参考链接
- **category_id**: 分类ID
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 11. Memory（记忆表）

### 表结构设计
```sql
CREATE TABLE memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    memory_type TEXT CHECK(memory_type IN ('experience', 'event', 'learning', 'interaction', 'achievement', 'mistake')),
    importance INTEGER CHECK(importance >= 1 AND importance <= 10),
    related_people TEXT,
    location TEXT,
    memory_date DATE,
    keywords TEXT,
    source_app TEXT,
    category_id INTEGER,
    reference_urls TEXT,
    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_memory_type ON memory(memory_type);
CREATE INDEX idx_memory_importance ON memory(importance);
CREATE INDEX idx_memory_date ON memory(memory_date);
CREATE INDEX idx_memory_people ON memory(related_people);
CREATE INDEX idx_memory_location ON memory(location);
CREATE INDEX idx_memory_source_app ON memory(source_app);
CREATE INDEX idx_memory_privacy ON memory(privacy_level);
```

### 字段说明
- **id**: 主键
- **content**: 记忆内容，如"第一次使用新技术解决复杂问题的经历"
- **memory_type**: 记忆类型
  - `experience`: 个人经历
  - `event`: 重要事件
  - `learning`: 学习体验
  - `interaction`: 人际互动
  - `achievement`: 成就记录
  - `mistake`: 错误教训
- **importance**: 重要程度（1-10），10为最重要
- **related_people**: 相关人员，如"同事张三，导师李四"
- **location**: 发生地点，如"公司会议室"、"线上会议"
- **memory_date**: 记忆发生的具体日期
- **keywords**: 关键词数组，JSON格式存储，如["技术突破","团队合作","问题解决"]
- **source_app**: 数据来源应用，如"日记App"、"工作记录工具"、"回忆录"
- **category_id**: 分类ID
- **reference_urls**: 相关链接，如照片、文档、视频链接
- **privacy_level**: 隐私级别（public/private）
- **created_time**: 创建时间
- **updated_time**: 更新时间

---

## 数据库设计总结

### 核心特性

1. **统一的数据来源追踪**
   - 所有核心表都包含`source_app`字段，记录数据来源应用
   - 支持多应用数据集成和来源追溯
   - 便于数据质量管理和应用使用分析

2. **关键词标签系统**
   - 所有核心表都包含`keywords`字段（JSON数组格式）
   - 支持灵活的标签分类和语义搜索
   - 便于构建知识图谱和内容关联

3. **人员来源记录**
   - `Viewpoint`和`Insight`表包含`source_people`字段
   - 记录观点和洞察的人员来源
   - 支持基于来源的可信度评估

4. **简化的隐私控制**
   - 统一使用`privacy_level`枚举（public/private）
   - 清晰的二级隐私控制体系
   - 为每个隐私字段建立索引优化查询性能

5. **灵活的关联体系**
   - `Relations`表支持任意表间的多对多关联
   - 支持关联强度和类型定义
   - 可扩展的关系语义

6. **分层目标管理**
   - `Goal`表支持四层目标体系（long_term/short_term/plan/todo）
   - 通过`Relations`表建立目标层级关系
   - 移除进度字段，简化状态管理

7. **事件关联机制**
   - `Viewpoint`表的`related_event`字段
   - 支持观点与具体事件的关联
   - 便于基于场景的内容检索

8. **个人记忆管理**
   - `Memory`表支持多种记忆类型（experience/event/learning/interaction/achievement/mistake）
   - 包含时空信息（memory_date/location）和人员关联（related_people）
   - 重要程度评级（1-10）和情感上下文记录
   - 支持个人成长轨迹追踪和经验复盘

### 数据完整性保障

- 所有表都有主键和时间戳
- 外键约束保证引用完整性
- CHECK约束确保枚举值有效性
- 为常用查询字段建立索引

### 扩展性设计

- 通过`keywords`支持灵活的语义分类
- `Relations`表提供通用的关联机制
- `Category`两级分类体系支持层次化组织
- JSON格式的`keywords`和`reference_urls`支持灵活的数据结构