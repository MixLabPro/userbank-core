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
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE UNIQUE INDEX idx_persona_id ON persona(id);
CREATE INDEX idx_persona_private ON persona(private);
```

### 字段说明
- **id**: 主键，固定为1（系统只维护一个人物档案）
- **name**: 用户姓名，如"张三"
- **gender**: 性别，影响语言风格和称呼方式
- **personality**: 性格描述，如"内向思考型，注重细节，喜欢深度分析"
- **avatar_url**: 头像链接（可选）
- **bio**: 个人简介（可选）
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 获取用户基本信息，用于个性化回复（排除私有数据）
SELECT name, gender, personality FROM persona WHERE id = 1 AND private = false;

-- 在生成回复时的应用
-- 如果personality包含"内向"，则回复更加深思熟虑
-- 如果gender为"female"，语言风格可能更细腻
```

### 连表使用
```sql
-- 查询某人的所有观点（排除私有数据）
SELECT v.*, p.name, p.personality 
FROM viewpoint v 
JOIN persona p ON v.persona_id = p.id 
WHERE v.persona_id = 1 AND v.private = false AND p.private = false;
```

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
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_category_levels ON category(first_level, second_level);
CREATE INDEX idx_category_active ON category(is_active);
CREATE INDEX idx_category_private ON category(private);
```

### 字段说明
- **id**: 分类ID
- **first_level**: 一级目录，如"技术"、"生活"、"商业"
- **second_level**: 二级目录，如"编程开发"、"人际关系"、"投资理财"
- **description**: 分类描述
- **is_active**: 是否启用该分类
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 按主题查询内容（排除私有数据）
SELECT c.first_level, c.second_level, COUNT(v.id) as viewpoint_count
FROM category c
LEFT JOIN viewpoint v ON c.id = v.category_id AND v.private = false
WHERE c.private = false
GROUP BY c.id;

-- 用于Prompt增强：找到用户在某领域的所有相关内容（排除私有数据）
SELECT 'viewpoint' as type, v.content, c.first_level, c.second_level
FROM viewpoint v 
JOIN category c ON v.category_id = c.id 
WHERE c.first_level = '技术' AND v.private = false AND c.private = false
UNION ALL
SELECT 'experience' as type, e.content, c.first_level, c.second_level
FROM experience e 
JOIN category c ON e.category_id = c.id 
WHERE c.first_level = '技术' AND e.private = false AND c.private = false;
```

### 实际应用案例
当用户问"帮我设计一个系统"时：
```sql
-- 查询技术相关的所有用户数据（排除私有数据）
SELECT v.content as viewpoint, m.content as methodology, e.content as experience
FROM category c
LEFT JOIN viewpoint v ON c.id = v.category_id AND v.private = false
LEFT JOIN methodology m ON c.id = m.category_id AND m.private = false
LEFT JOIN experience e ON c.id = e.category_id AND e.private = false
WHERE c.first_level = '技术' AND c.second_level = '系统架构' AND c.private = false;
```

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
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_relations_source ON relations(source_table, source_id);
CREATE INDEX idx_relations_target ON relations(target_table, target_id);
CREATE INDEX idx_relations_type ON relations(relation_type);
CREATE INDEX idx_relations_private ON relations(private);
```

### 字段说明
- **id**: 主键
- **source_table**: 源表名，如"insight"
- **source_id**: 源记录ID
- **target_table**: 目标表名，如"decision"
- **target_id**: 目标记录ID
- **relation_type**: 关联类型，如"inspired_by"、"conflicts_with"、"supports"、"parent_of"
- **strength**: 关联强度（strong/medium/weak）
- **note**: 关联说明
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 找到启发某个决策的所有洞察（排除私有数据）
SELECT i.content as insight_content, r.note
FROM relations r
JOIN insight i ON r.source_table = 'insight' AND r.source_id = i.id AND i.private = false
WHERE r.target_table = 'decision' AND r.target_id = 123 
AND r.relation_type = 'inspired_by' AND r.private = false;

-- 构建知识图谱：找到某个观点的所有相关内容（排除私有数据）
SELECT r.target_table, r.target_id, r.relation_type
FROM relations r 
WHERE r.source_table = 'viewpoint' AND r.source_id = 456 AND r.private = false;
```

### 实际应用案例
构建用户思维脉络：
```sql
-- 当用户提到某个话题时，找到相关的思维链条（排除私有数据）
WITH RECURSIVE thought_chain AS (
  SELECT source_table, source_id, target_table, target_id, 1 as level
  FROM relations 
  WHERE source_table = 'viewpoint' AND source_id = 123 AND private = false
  UNION ALL
  SELECT r.source_table, r.source_id, r.target_table, r.target_id, tc.level + 1
  FROM relations r
  JOIN thought_chain tc ON r.source_table = tc.target_table AND r.source_id = tc.target_id
  WHERE tc.level < 3 AND r.private = false
)
SELECT * FROM thought_chain;
```

---

## 4. Viewpoint（观点表）

### 表结构设计
```sql
CREATE TABLE viewpoint (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    subject TEXT NOT NULL,
    stance TEXT CHECK(stance IN ('strongly_support', 'support', 'neutral', 'oppose', 'strongly_oppose')),
    source TEXT,
    persona_id INTEGER DEFAULT 1,
    time_period TEXT,
    reference_urls TEXT,
    category_id INTEGER,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (persona_id) REFERENCES persona(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_viewpoint_subject ON viewpoint(subject);
CREATE INDEX idx_viewpoint_time ON viewpoint(time_period);
CREATE INDEX idx_viewpoint_category ON viewpoint(category_id);
CREATE INDEX idx_viewpoint_private ON viewpoint(private);
```

### 字段说明
- **id**: 主键
- **content**: 观点内容，如"我认为微服务架构适合团队规模超过20人的项目"
- **subject**: 观点主题，如"微服务架构"
- **stance**: 观点立场（强烈支持到强烈反对）
- **source**: 观点来源，如"项目实践经验"、"技术书籍学习"
- **persona_id**: 固定为1（指向唯一的persona记录）
- **time_period**: 时间段，如"大学时期"、"工作第3年"、"当前"
- **reference_urls**: 参考链接数组
- **category_id**: 分类ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 分析观点演变：查看用户在不同时期对同一主题的观点变化（排除私有数据）
SELECT time_period, stance, content 
FROM viewpoint 
WHERE subject = '微服务架构' AND private = false
ORDER BY CASE time_period 
  WHEN '大学时期' THEN 1 
  WHEN '工作第1年' THEN 2 
  WHEN '工作第3年' THEN 3 
  WHEN '当前' THEN 4 
END;

-- Prompt增强：获取用户对当前话题的立场（排除私有数据）
SELECT content, stance, source 
FROM viewpoint 
WHERE subject LIKE '%架构%' AND time_period = '当前' AND private = false;
```

### 实际应用案例
用户问"我应该选择微服务还是单体架构？"
```sql
-- 查询用户的相关观点和经验（排除私有数据）
SELECT 
  v.content as viewpoint,
  v.stance,
  v.time_period,
  e.content as related_experience,
  c.first_level, c.second_level
FROM viewpoint v
LEFT JOIN category c ON v.category_id = c.id AND c.private = false
LEFT JOIN experience e ON e.category_id = c.id AND e.private = false
WHERE (v.subject LIKE '%架构%' OR e.field LIKE '%架构%') 
AND v.private = false;
```

增强后的回复框架：
```
基于你的观点演变：
- 大学时期：偏好单体架构（简单直接）
- 工作第3年：开始认可微服务（复杂项目经验）
- 当前：支持根据团队规模选择架构

建议：考虑你当前的团队规模和项目复杂度...
```

---

## 5. Insight（洞察表）

### 表结构设计
```sql
CREATE TABLE insight (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    trigger_event TEXT,
    impact_level TEXT CHECK(impact_level IN ('high', 'medium', 'low')),
    category_id INTEGER,
    reference_urls TEXT,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_insight_impact ON insight(impact_level);
CREATE INDEX idx_insight_category ON insight(category_id);
CREATE INDEX idx_insight_time ON insight(created_time);
CREATE INDEX idx_insight_private ON insight(private);
```

### 字段说明
- **id**: 主键
- **content**: 洞察内容，如"技术选择往往反映了团队的组织结构"
- **trigger_event**: 触发事件，如"项目重构失败的复盘"
- **impact_level**: 影响程度（high/medium/low）
- **category_id**: 分类ID
- **reference_urls**: 参考链接
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 获取高影响力的洞察用于Prompt增强（排除私有数据）
SELECT content, trigger_event 
FROM insight 
WHERE impact_level = 'high' AND private = false
ORDER BY created_time DESC 
LIMIT 5;

-- 根据触发事件找相关洞察（排除私有数据）
SELECT content 
FROM insight 
WHERE (trigger_event LIKE '%失败%' OR trigger_event LIKE '%挫折%') AND private = false;
```

### 实际应用案例
用户遇到技术选择困难时：
```sql
-- 查询相关的洞察和决策经验（排除私有数据）
SELECT i.content as insight, d.content as past_decision, d.outcome
FROM insight i
JOIN category c1 ON i.category_id = c1.id AND c1.private = false
LEFT JOIN decision d ON d.category_id IN (
  SELECT id FROM category WHERE first_level = c1.first_level AND private = false
) AND d.private = false
WHERE c1.first_level = '技术' AND i.impact_level = 'high' AND i.private = false;
```

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
    category_id INTEGER,
    deadline DATE,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_focus_status ON focus(status);
CREATE INDEX idx_focus_priority ON focus(priority);
CREATE INDEX idx_focus_deadline ON focus(deadline);
CREATE INDEX idx_focus_private ON focus(private);
```

### 字段说明
- **id**: 主键
- **content**: 关注内容，如"学习Rust编程语言"
- **priority**: 优先级（1-10）
- **status**: 状态（active/paused/completed）
- **context**: 上下文，如"工作"、"个人提升"
- **category_id**: 分类ID
- **deadline**: 截止日期
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 获取当前活跃的关注点，评估用户认知负荷（排除私有数据）
SELECT content, priority, deadline 
FROM focus 
WHERE status = 'active' AND private = false
ORDER BY priority DESC;

-- 时间冲突检测（排除私有数据）
SELECT COUNT(*) as active_high_priority_items
FROM focus 
WHERE status = 'active' AND priority >= 8 AND private = false;
```

### 实际应用案例
用户想学习新技术时：
```sql
-- 评估当前负荷，给出建议（排除私有数据）
SELECT 
  COUNT(*) as total_active,
  AVG(priority) as avg_priority,
  COUNT(CASE WHEN deadline < DATE_ADD(NOW(), INTERVAL 30 DAY) THEN 1 END) as urgent_items
FROM focus 
WHERE status = 'active' AND private = false;
```

如果active_items > 5且avg_priority > 7：
```
根据你当前的关注点分析：
- 你有5个高优先级的活跃目标
- 平均优先级8.2，认知负荷较重
- 建议：先完成2个现有目标再开始新学习
```

---

## 7. Goal（目标表）- 增强版

### 表结构设计
```sql
CREATE TABLE goal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    type TEXT CHECK(type IN ('long_term', 'short_term', 'plan', 'todo')),
    deadline DATE,
    progress INTEGER DEFAULT 0 CHECK(progress >= 0 AND progress <= 100),
    status TEXT CHECK(status IN ('planning', 'in_progress', 'completed', 'abandoned')),
    category_id INTEGER,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_goal_type ON goal(type);
CREATE INDEX idx_goal_status ON goal(status);
CREATE INDEX idx_goal_deadline ON goal(deadline);
CREATE INDEX idx_goal_category ON goal(category_id);
CREATE INDEX idx_goal_private ON goal(private);
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
- **progress**: 进度（0-100）
- **status**: 状态（planning/in_progress/completed/abandoned）
- **category_id**: 分类ID
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 目标进展分析（排除私有数据）
SELECT type, AVG(progress) as avg_progress, COUNT(*) as count
FROM goal 
WHERE status = 'in_progress' AND private = false
GROUP BY type;

-- 找到停滞的目标（排除私有数据）
SELECT content, progress, DATEDIFF(NOW(), updated_time) as days_since_update
FROM goal 
WHERE status = 'in_progress' AND updated_time < DATE_SUB(NOW(), INTERVAL 14 DAY) AND private = false;
```

### 目标层级关联查询
```sql
-- 查找长期目标及其关联的短期目标、计划和待办（排除私有数据）
WITH goal_hierarchy AS (
    -- 获取长期目标
    SELECT g1.id as long_term_id, g1.content as long_term_goal,
           g2.id as short_term_id, g2.content as short_term_goal,
           g3.id as plan_id, g3.content as plan,
           g4.id as todo_id, g4.content as todo
    FROM goal g1
    LEFT JOIN relations r1 ON r1.source_table = 'goal' AND r1.source_id = g1.id 
                           AND r1.target_table = 'goal' AND r1.relation_type = 'parent_of' AND r1.private = false
    LEFT JOIN goal g2 ON r1.target_id = g2.id AND g2.type = 'short_term' AND g2.private = false
    LEFT JOIN relations r2 ON r2.source_table = 'goal' AND r2.source_id = g2.id 
                           AND r2.target_table = 'goal' AND r2.relation_type = 'parent_of' AND r2.private = false
    LEFT JOIN goal g3 ON r2.target_id = g3.id AND g3.type = 'plan' AND g3.private = false
    LEFT JOIN relations r3 ON r3.source_table = 'goal' AND r3.source_id = g3.id 
                           AND r3.target_table = 'goal' AND r3.relation_type = 'parent_of' AND r3.private = false
    LEFT JOIN goal g4 ON r3.target_id = g4.id AND g4.type = 'todo' AND g4.private = false
    WHERE g1.type = 'long_term' AND g1.status = 'in_progress' AND g1.private = false
)
SELECT * FROM goal_hierarchy;

-- 计算整体进度：从待办向上汇总（排除私有数据）
SELECT 
    g_parent.id,
    g_parent.content,
    g_parent.type,
    AVG(g_child.progress) as calculated_progress,
    g_parent.progress as recorded_progress
FROM goal g_parent
JOIN relations r ON r.source_table = 'goal' AND r.source_id = g_parent.id AND r.private = false
JOIN goal g_child ON r.target_table = 'goal' AND r.target_id = g_child.id AND g_child.private = false
WHERE r.relation_type = 'parent_of' AND g_parent.private = false
GROUP BY g_parent.id;
```

### 实际应用案例

#### 1. 每日任务规划
```sql
-- 获取今日待办及其关联的上层目标（排除私有数据）
SELECT 
    t.id as todo_id,
    t.content as todo,
    t.deadline,
    p.content as related_plan,
    st.content as related_short_term,
    lt.content as related_long_term
FROM goal t
LEFT JOIN relations r1 ON r1.target_table = 'goal' AND r1.target_id = t.id 
                        AND r1.source_table = 'goal' AND r1.relation_type = 'parent_of' AND r1.private = false
LEFT JOIN goal p ON r1.source_id = p.id AND p.type = 'plan' AND p.private = false
LEFT JOIN relations r2 ON r2.target_table = 'goal' AND r2.target_id = p.id 
                        AND r2.source_table = 'goal' AND r2.relation_type = 'parent_of' AND r2.private = false
LEFT JOIN goal st ON r2.source_id = st.id AND st.type = 'short_term' AND st.private = false
LEFT JOIN relations r3 ON r3.target_table = 'goal' AND r3.target_id = st.id 
                        AND r3.source_table = 'goal' AND r3.relation_type = 'parent_of' AND r3.private = false
LEFT JOIN goal lt ON r3.source_id = lt.id AND lt.type = 'long_term' AND lt.private = false
WHERE t.type = 'todo' 
AND t.status IN ('planning', 'in_progress')
AND (t.deadline = CURDATE() OR t.deadline IS NULL)
AND t.private = false
ORDER BY t.deadline, t.created_time;
```

#### 2. 周度回顾与规划
```sql
-- 本周完成情况统计（排除私有数据）
SELECT 
    type,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
    AVG(progress) as avg_progress
FROM goal
WHERE updated_time >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND private = false
GROUP BY type
ORDER BY FIELD(type, 'todo', 'plan', 'short_term', 'long_term');

-- 下周需要关注的目标（排除私有数据）
SELECT 
    g.*,
    c.first_level,
    c.second_level,
    DATEDIFF(g.deadline, CURDATE()) as days_remaining
FROM goal g
LEFT JOIN category c ON g.category_id = c.id AND c.private = false
WHERE g.status = 'in_progress'
AND g.deadline BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
AND g.private = false
ORDER BY g.deadline, g.type;
```

#### 3. 目标对齐检查
```sql
-- 检查孤立的目标（没有上级或下级关联）（排除私有数据）
SELECT 
    g.id,
    g.content,
    g.type,
    CASE 
        WHEN g.type = 'todo' AND NOT EXISTS (
            SELECT 1 FROM relations r 
            WHERE r.target_table = 'goal' AND r.target_id = g.id 
            AND r.relation_type = 'parent_of' AND r.private = false
        ) THEN '缺少上级计划'
        WHEN g.type = 'plan' AND NOT EXISTS (
            SELECT 1 FROM relations r 
            WHERE r.source_table = 'goal' AND r.source_id = g.id 
            AND r.relation_type = 'parent_of' AND r.private = false
        ) THEN '缺少具体待办'
        WHEN g.type = 'long_term' AND NOT EXISTS (
            SELECT 1 FROM relations r 
            WHERE r.source_table = 'goal' AND r.source_id = g.id 
            AND r.relation_type = 'parent_of' AND r.private = false
        ) THEN '缺少执行计划'
    END as alignment_issue
FROM goal g
WHERE g.status = 'in_progress' AND g.private = false
HAVING alignment_issue IS NOT NULL;
```

---

## 8. Preference（偏好表）

### 表结构设计
```sql
CREATE TABLE preference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    strength TEXT CHECK(strength IN ('strong', 'moderate', 'flexible')),
    context TEXT,
    category_id INTEGER,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_preference_strength ON preference(strength);
CREATE INDEX idx_preference_context ON preference(context);
CREATE INDEX idx_preference_private ON preference(private);
```

### 字段说明
- **id**: 主键
- **content**: 偏好内容，如"喜欢在安静环境中深度思考"
- **strength**: 偏好强度（strong/moderate/flexible）
- **context**: 适用场景，如"学习时"、"工作中"
- **category_id**: 分类ID
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 获取强偏好用于个性化（排除私有数据）
SELECT content, context 
FROM preference 
WHERE strength = 'strong' AND private = false;

-- 特定场景下的偏好（排除私有数据）
SELECT content 
FROM preference 
WHERE context LIKE '%学习%' AND strength != 'flexible' AND private = false;
```

### 实际应用案例
制定学习计划时：
```sql
SELECT 
  p.content as preference,
  p.context,
  m.content as learning_methodology
FROM preference p
JOIN category c ON p.category_id = c.id AND c.private = false
LEFT JOIN methodology m ON m.category_id = c.id AND m.private = false
WHERE (p.context LIKE '%学习%' OR c.second_level LIKE '%学习%')
AND p.strength = 'strong' AND p.private = false;
```

---

## 9. Decision（决策表）

### 表结构设计
```sql
CREATE TABLE decision (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    reasoning TEXT,
    outcome TEXT,
    domain TEXT,
    category_id INTEGER,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_decision_domain ON decision(domain);
CREATE INDEX idx_decision_time ON decision(created_time);
CREATE INDEX idx_decision_private ON decision(private);
```

### 字段说明
- **id**: 主键
- **content**: 决策内容
- **reasoning**: 决策理由
- **outcome**: 决策结果
- **domain**: 决策领域
- **category_id**: 分类ID
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 分析决策模式（排除私有数据）
SELECT domain, COUNT(*) as decision_count,
       COUNT(CASE WHEN outcome LIKE '%成功%' THEN 1 END) as success_count
FROM decision 
WHERE private = false
GROUP BY domain;

-- 找到相似决策的历史经验（排除私有数据）
SELECT content, reasoning, outcome 
FROM decision 
WHERE domain = '技术选择' AND private = false
ORDER BY created_time DESC 
LIMIT 3;
```

---

## 10. Methodology（方法论表）

### 表结构设计
```sql
CREATE TABLE methodology (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    type TEXT,
    effectiveness TEXT CHECK(effectiveness IN ('proven', 'experimental', 'theoretical')),
    use_cases TEXT,
    persona_id INTEGER DEFAULT 1,
    category_id INTEGER,
    reference_urls TEXT,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (persona_id) REFERENCES persona(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_methodology_type ON methodology(type);
CREATE INDEX idx_methodology_effectiveness ON methodology(effectiveness);
CREATE INDEX idx_methodology_private ON methodology(private);
```

### 字段说明
- **id**: 主键
- **content**: 方法论内容
- **type**: 类型，如"问题解决"、"决策制定"
- **effectiveness**: 有效性（proven/experimental/theoretical）
- **use_cases**: 适用场景
- **persona_id**: 固定为1
- **category_id**: 分类ID
- **reference_urls**: 参考链接
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 连表查询案例
```sql
-- 获取用户的决策方法论（排除私有数据）
SELECT m.content, m.use_cases, p.personality
FROM methodology m
JOIN persona p ON m.persona_id = p.id AND p.private = false
WHERE m.type = '决策制定' AND m.effectiveness = 'proven' AND m.private = false;
```

---

## 11. Experience（经验表）

### 表结构设计
```sql
CREATE TABLE experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    field TEXT,
    expertise_level TEXT CHECK(expertise_level IN ('beginner', 'intermediate', 'proficient', 'expert')),
    years INTEGER,
    key_learnings TEXT,
    category_id INTEGER,
    reference_urls TEXT,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_experience_field ON experience(field);
CREATE INDEX idx_experience_level ON experience(expertise_level);
CREATE INDEX idx_experience_private ON experience(private);
```

### 字段说明
- **id**: 主键
- **content**: 经验内容
- **field**: 领域
- **expertise_level**: 专业程度
- **years**: 经验年数
- **key_learnings**: 关键学习
- **category_id**: 分类ID
- **reference_urls**: 参考链接
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 专业领域匹配（排除私有数据）
SELECT field, expertise_level, key_learnings 
FROM experience 
WHERE expertise_level IN ('expert', 'proficient') AND private = false;
```

---

## 12. Prediction（预测表）

### 表结构设计
```sql
CREATE TABLE prediction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    timeframe TEXT,
    basis TEXT,
    verification_status TEXT CHECK(verification_status IN ('pending', 'correct', 'incorrect', 'partial')),
    reference_urls TEXT,
    category_id INTEGER,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_prediction_timeframe ON prediction(timeframe);
CREATE INDEX idx_prediction_status ON prediction(verification_status);
CREATE INDEX idx_prediction_private ON prediction(private);
```

### 字段说明
- **id**: 主键
- **content**: 预测内容
- **timeframe**: 时间范围
- **basis**: 预测依据
- **verification_status**: 验证状态（pending/correct/incorrect/partial）
- **reference_urls**: 参考链接
- **category_id**: 分类ID
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 验证预测准确性（排除私有数据）
SELECT 
  timeframe,
  COUNT(*) as total_predictions,# Profile数据库字段详细使用指南

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
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE UNIQUE INDEX idx_persona_id ON persona(id);
CREATE INDEX idx_persona_private ON persona(private);
```

### 字段说明
- **id**: 主键，固定为1（系统只维护一个人物档案）
- **name**: 用户姓名，如"张三"
- **gender**: 性别，影响语言风格和称呼方式
- **personality**: 性格描述，如"内向思考型，注重细节，喜欢深度分析"
- **avatar_url**: 头像链接（可选）
- **bio**: 个人简介（可选）
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 获取用户基本信息，用于个性化回复（排除私有数据）
SELECT name, gender, personality FROM persona WHERE id = 1 AND private = false;

-- 在生成回复时的应用
-- 如果personality包含"内向"，则回复更加深思熟虑
-- 如果gender为"female"，语言风格可能更细腻
```

### 连表使用
```sql
-- 查询某人的所有观点（排除私有数据）
SELECT v.*, p.name, p.personality 
FROM viewpoint v 
JOIN persona p ON v.persona_id = p.id 
WHERE v.persona_id = 1 AND v.private = false AND p.private = false;
```

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
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_category_levels ON category(first_level, second_level);
CREATE INDEX idx_category_active ON category(is_active);
CREATE INDEX idx_category_private ON category(private);
```

### 字段说明
- **id**: 分类ID
- **first_level**: 一级目录，如"技术"、"生活"、"商业"
- **second_level**: 二级目录，如"编程开发"、"人际关系"、"投资理财"
- **description**: 分类描述
- **is_active**: 是否启用该分类
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 按主题查询内容（排除私有数据）
SELECT c.first_level, c.second_level, COUNT(v.id) as viewpoint_count
FROM category c
LEFT JOIN viewpoint v ON c.id = v.category_id AND v.private = false
WHERE c.private = false
GROUP BY c.id;

-- 用于Prompt增强：找到用户在某领域的所有相关内容（排除私有数据）
SELECT 'viewpoint' as type, v.content, c.first_level, c.second_level
FROM viewpoint v 
JOIN category c ON v.category_id = c.id 
WHERE c.first_level = '技术' AND v.private = false AND c.private = false
UNION ALL
SELECT 'experience' as type, e.content, c.first_level, c.second_level
FROM experience e 
JOIN category c ON e.category_id = c.id 
WHERE c.first_level = '技术' AND e.private = false AND c.private = false;
```

### 实际应用案例
当用户问"帮我设计一个系统"时：
```sql
-- 查询技术相关的所有用户数据（排除私有数据）
SELECT v.content as viewpoint, m.content as methodology, e.content as experience
FROM category c
LEFT JOIN viewpoint v ON c.id = v.category_id AND v.private = false
LEFT JOIN methodology m ON c.id = m.category_id AND m.private = false
LEFT JOIN experience e ON c.id = e.category_id AND e.private = false
WHERE c.first_level = '技术' AND c.second_level = '系统架构' AND c.private = false;
```

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
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_relations_source ON relations(source_table, source_id);
CREATE INDEX idx_relations_target ON relations(target_table, target_id);
CREATE INDEX idx_relations_type ON relations(relation_type);
CREATE INDEX idx_relations_private ON relations(private);
```

### 字段说明
- **id**: 主键
- **source_table**: 源表名，如"insight"
- **source_id**: 源记录ID
- **target_table**: 目标表名，如"decision"
- **target_id**: 目标记录ID
- **relation_type**: 关联类型，如"inspired_by"、"conflicts_with"、"supports"、"parent_of"
- **strength**: 关联强度（strong/medium/weak）
- **note**: 关联说明
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 找到启发某个决策的所有洞察（排除私有数据）
SELECT i.content as insight_content, r.note
FROM relations r
JOIN insight i ON r.source_table = 'insight' AND r.source_id = i.id AND i.private = false
WHERE r.target_table = 'decision' AND r.target_id = 123 
AND r.relation_type = 'inspired_by' AND r.private = false;

-- 构建知识图谱：找到某个观点的所有相关内容（排除私有数据）
SELECT r.target_table, r.target_id, r.relation_type
FROM relations r 
WHERE r.source_table = 'viewpoint' AND r.source_id = 456 AND r.private = false;
```

### 实际应用案例
构建用户思维脉络：
```sql
-- 当用户提到某个话题时，找到相关的思维链条（排除私有数据）
WITH RECURSIVE thought_chain AS (
  SELECT source_table, source_id, target_table, target_id, 1 as level
  FROM relations 
  WHERE source_table = 'viewpoint' AND source_id = 123 AND private = false
  UNION ALL
  SELECT r.source_table, r.source_id, r.target_table, r.target_id, tc.level + 1
  FROM relations r
  JOIN thought_chain tc ON r.source_table = tc.target_table AND r.source_id = tc.target_id
  WHERE tc.level < 3 AND r.private = false
)
SELECT * FROM thought_chain;
```

---

## 4. Viewpoint（观点表）

### 表结构设计
```sql
CREATE TABLE viewpoint (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    subject TEXT NOT NULL,
    stance TEXT CHECK(stance IN ('strongly_support', 'support', 'neutral', 'oppose', 'strongly_oppose')),
    source TEXT,
    persona_id INTEGER DEFAULT 1,
    time_period TEXT,
    reference_urls TEXT,
    category_id INTEGER,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (persona_id) REFERENCES persona(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_viewpoint_subject ON viewpoint(subject);
CREATE INDEX idx_viewpoint_time ON viewpoint(time_period);
CREATE INDEX idx_viewpoint_category ON viewpoint(category_id);
CREATE INDEX idx_viewpoint_private ON viewpoint(private);
```

### 字段说明
- **id**: 主键
- **content**: 观点内容，如"我认为微服务架构适合团队规模超过20人的项目"
- **subject**: 观点主题，如"微服务架构"
- **stance**: 观点立场（强烈支持到强烈反对）
- **source**: 观点来源，如"项目实践经验"、"技术书籍学习"
- **persona_id**: 固定为1（指向唯一的persona记录）
- **time_period**: 时间段，如"大学时期"、"工作第3年"、"当前"
- **reference_urls**: 参考链接数组
- **category_id**: 分类ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 分析观点演变：查看用户在不同时期对同一主题的观点变化（排除私有数据）
SELECT time_period, stance, content 
FROM viewpoint 
WHERE subject = '微服务架构' AND private = false
ORDER BY CASE time_period 
  WHEN '大学时期' THEN 1 
  WHEN '工作第1年' THEN 2 
  WHEN '工作第3年' THEN 3 
  WHEN '当前' THEN 4 
END;

-- Prompt增强：获取用户对当前话题的立场（排除私有数据）
SELECT content, stance, source 
FROM viewpoint 
WHERE subject LIKE '%架构%' AND time_period = '当前' AND private = false;
```

### 实际应用案例
用户问"我应该选择微服务还是单体架构？"
```sql
-- 查询用户的相关观点和经验（排除私有数据）
SELECT 
  v.content as viewpoint,
  v.stance,
  v.time_period,
  e.content as related_experience,
  c.first_level, c.second_level
FROM viewpoint v
LEFT JOIN category c ON v.category_id = c.id AND c.private = false
LEFT JOIN experience e ON e.category_id = c.id AND e.private = false
WHERE (v.subject LIKE '%架构%' OR e.field LIKE '%架构%') 
AND v.private = false;
```

增强后的回复框架：
```
基于你的观点演变：
- 大学时期：偏好单体架构（简单直接）
- 工作第3年：开始认可微服务（复杂项目经验）
- 当前：支持根据团队规模选择架构

建议：考虑你当前的团队规模和项目复杂度...
```

---

## 5. Insight（洞察表）

### 表结构设计
```sql
CREATE TABLE insight (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    trigger_event TEXT,
    impact_level TEXT CHECK(impact_level IN ('high', 'medium', 'low')),
    category_id INTEGER,
    reference_urls TEXT,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_insight_impact ON insight(impact_level);
CREATE INDEX idx_insight_category ON insight(category_id);
CREATE INDEX idx_insight_time ON insight(created_time);
CREATE INDEX idx_insight_private ON insight(private);
```

### 字段说明
- **id**: 主键
- **content**: 洞察内容，如"技术选择往往反映了团队的组织结构"
- **trigger_event**: 触发事件，如"项目重构失败的复盘"
- **impact_level**: 影响程度（high/medium/low）
- **category_id**: 分类ID
- **reference_urls**: 参考链接
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 获取高影响力的洞察用于Prompt增强（排除私有数据）
SELECT content, trigger_event 
FROM insight 
WHERE impact_level = 'high' AND private = false
ORDER BY created_time DESC 
LIMIT 5;

-- 根据触发事件找相关洞察（排除私有数据）
SELECT content 
FROM insight 
WHERE (trigger_event LIKE '%失败%' OR trigger_event LIKE '%挫折%') AND private = false;
```

### 实际应用案例
用户遇到技术选择困难时：
```sql
-- 查询相关的洞察和决策经验（排除私有数据）
SELECT i.content as insight, d.content as past_decision, d.outcome
FROM insight i
JOIN category c1 ON i.category_id = c1.id AND c1.private = false
LEFT JOIN decision d ON d.category_id IN (
  SELECT id FROM category WHERE first_level = c1.first_level AND private = false
) AND d.private = false
WHERE c1.first_level = '技术' AND i.impact_level = 'high' AND i.private = false;
```

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
    category_id INTEGER,
    deadline DATE,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_focus_status ON focus(status);
CREATE INDEX idx_focus_priority ON focus(priority);
CREATE INDEX idx_focus_deadline ON focus(deadline);
CREATE INDEX idx_focus_private ON focus(private);
```

### 字段说明
- **id**: 主键
- **content**: 关注内容，如"学习Rust编程语言"
- **priority**: 优先级（1-10）
- **status**: 状态（active/paused/completed）
- **context**: 上下文，如"工作"、"个人提升"
- **category_id**: 分类ID
- **deadline**: 截止日期
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 获取当前活跃的关注点，评估用户认知负荷（排除私有数据）
SELECT content, priority, deadline 
FROM focus 
WHERE status = 'active' AND private = false
ORDER BY priority DESC;

-- 时间冲突检测（排除私有数据）
SELECT COUNT(*) as active_high_priority_items
FROM focus 
WHERE status = 'active' AND priority >= 8 AND private = false;
```

### 实际应用案例
用户想学习新技术时：
```sql
-- 评估当前负荷，给出建议（排除私有数据）
SELECT 
  COUNT(*) as total_active,
  AVG(priority) as avg_priority,
  COUNT(CASE WHEN deadline < DATE_ADD(NOW(), INTERVAL 30 DAY) THEN 1 END) as urgent_items
FROM focus 
WHERE status = 'active' AND private = false;
```

如果active_items > 5且avg_priority > 7：
```
根据你当前的关注点分析：
- 你有5个高优先级的活跃目标
- 平均优先级8.2，认知负荷较重
- 建议：先完成2个现有目标再开始新学习
```

---

## 7. Goal（目标表）- 增强版

### 表结构设计
```sql
CREATE TABLE goal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    type TEXT CHECK(type IN ('long_term', 'short_term', 'plan', 'todo')),
    deadline DATE,
    progress INTEGER DEFAULT 0 CHECK(progress >= 0 AND progress <= 100),
    status TEXT CHECK(status IN ('planning', 'in_progress', 'completed', 'abandoned')),
    category_id INTEGER,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_goal_type ON goal(type);
CREATE INDEX idx_goal_status ON goal(status);
CREATE INDEX idx_goal_deadline ON goal(deadline);
CREATE INDEX idx_goal_category ON goal(category_id);
CREATE INDEX idx_goal_private ON goal(private);
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
- **progress**: 进度（0-100）
- **status**: 状态（planning/in_progress/completed/abandoned）
- **category_id**: 分类ID
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 目标进展分析（排除私有数据）
SELECT type, AVG(progress) as avg_progress, COUNT(*) as count
FROM goal 
WHERE status = 'in_progress' AND private = false
GROUP BY type;

-- 找到停滞的目标（排除私有数据）
SELECT content, progress, DATEDIFF(NOW(), updated_time) as days_since_update
FROM goal 
WHERE status = 'in_progress' AND updated_time < DATE_SUB(NOW(), INTERVAL 14 DAY) AND private = false;
```

### 目标层级关联查询
```sql
-- 查找长期目标及其关联的短期目标、计划和待办（排除私有数据）
WITH goal_hierarchy AS (
    -- 获取长期目标
    SELECT g1.id as long_term_id, g1.content as long_term_goal,
           g2.id as short_term_id, g2.content as short_term_goal,
           g3.id as plan_id, g3.content as plan,
           g4.id as todo_id, g4.content as todo
    FROM goal g1
    LEFT JOIN relations r1 ON r1.source_table = 'goal' AND r1.source_id = g1.id 
                           AND r1.target_table = 'goal' AND r1.relation_type = 'parent_of' AND r1.private = false
    LEFT JOIN goal g2 ON r1.target_id = g2.id AND g2.type = 'short_term' AND g2.private = false
    LEFT JOIN relations r2 ON r2.source_table = 'goal' AND r2.source_id = g2.id 
                           AND r2.target_table = 'goal' AND r2.relation_type = 'parent_of' AND r2.private = false
    LEFT JOIN goal g3 ON r2.target_id = g3.id AND g3.type = 'plan' AND g3.private = false
    LEFT JOIN relations r3 ON r3.source_table = 'goal' AND r3.source_id = g3.id 
                           AND r3.target_table = 'goal' AND r3.relation_type = 'parent_of' AND r3.private = false
    LEFT JOIN goal g4 ON r3.target_id = g4.id AND g4.type = 'todo' AND g4.private = false
    WHERE g1.type = 'long_term' AND g1.status = 'in_progress' AND g1.private = false
)
SELECT * FROM goal_hierarchy;

-- 计算整体进度：从待办向上汇总（排除私有数据）
SELECT 
    g_parent.id,
    g_parent.content,
    g_parent.type,
    AVG(g_child.progress) as calculated_progress,
    g_parent.progress as recorded_progress
FROM goal g_parent
JOIN relations r ON r.source_table = 'goal' AND r.source_id = g_parent.id AND r.private = false
JOIN goal g_child ON r.target_table = 'goal' AND r.target_id = g_child.id AND g_child.private = false
WHERE r.relation_type = 'parent_of' AND g_parent.private = false
GROUP BY g_parent.id;
```

### 实际应用案例

#### 1. 每日任务规划
```sql
-- 获取今日待办及其关联的上层目标（排除私有数据）
SELECT 
    t.id as todo_id,
    t.content as todo,
    t.deadline,
    p.content as related_plan,
    st.content as related_short_term,
    lt.content as related_long_term
FROM goal t
LEFT JOIN relations r1 ON r1.target_table = 'goal' AND r1.target_id = t.id 
                        AND r1.source_table = 'goal' AND r1.relation_type = 'parent_of' AND r1.private = false
LEFT JOIN goal p ON r1.source_id = p.id AND p.type = 'plan' AND p.private = false
LEFT JOIN relations r2 ON r2.target_table = 'goal' AND r2.target_id = p.id 
                        AND r2.source_table = 'goal' AND r2.relation_type = 'parent_of' AND r2.private = false
LEFT JOIN goal st ON r2.source_id = st.id AND st.type = 'short_term' AND st.private = false
LEFT JOIN relations r3 ON r3.target_table = 'goal' AND r3.target_id = st.id 
                        AND r3.source_table = 'goal' AND r3.relation_type = 'parent_of' AND r3.private = false
LEFT JOIN goal lt ON r3.source_id = lt.id AND lt.type = 'long_term' AND lt.private = false
WHERE t.type = 'todo' 
AND t.status IN ('planning', 'in_progress')
AND (t.deadline = CURDATE() OR t.deadline IS NULL)
AND t.private = false
ORDER BY t.deadline, t.created_time;
```

#### 2. 周度回顾与规划
```sql
-- 本周完成情况统计（排除私有数据）
SELECT 
    type,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
    AVG(progress) as avg_progress
FROM goal
WHERE updated_time >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND private = false
GROUP BY type
ORDER BY FIELD(type, 'todo', 'plan', 'short_term', 'long_term');

-- 下周需要关注的目标（排除私有数据）
SELECT 
    g.*,
    c.first_level,
    c.second_level,
    DATEDIFF(g.deadline, CURDATE()) as days_remaining
FROM goal g
LEFT JOIN category c ON g.category_id = c.id AND c.private = false
WHERE g.status = 'in_progress'
AND g.deadline BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
AND g.private = false
ORDER BY g.deadline, g.type;
```

#### 3. 目标对齐检查
```sql
-- 检查孤立的目标（没有上级或下级关联）（排除私有数据）
SELECT 
    g.id,
    g.content,
    g.type,
    CASE 
        WHEN g.type = 'todo' AND NOT EXISTS (
            SELECT 1 FROM relations r 
            WHERE r.target_table = 'goal' AND r.target_id = g.id 
            AND r.relation_type = 'parent_of' AND r.private = false
        ) THEN '缺少上级计划'
        WHEN g.type = 'plan' AND NOT EXISTS (
            SELECT 1 FROM relations r 
            WHERE r.source_table = 'goal' AND r.source_id = g.id 
            AND r.relation_type = 'parent_of' AND r.private = false
        ) THEN '缺少具体待办'
        WHEN g.type = 'long_term' AND NOT EXISTS (
            SELECT 1 FROM relations r 
            WHERE r.source_table = 'goal' AND r.source_id = g.id 
            AND r.relation_type = 'parent_of' AND r.private = false
        ) THEN '缺少执行计划'
    END as alignment_issue
FROM goal g
WHERE g.status = 'in_progress' AND g.private = false
HAVING alignment_issue IS NOT NULL;
```

---

## 8. Preference（偏好表）

### 表结构设计
```sql
CREATE TABLE preference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    strength TEXT CHECK(strength IN ('strong', 'moderate', 'flexible')),
    context TEXT,
    category_id INTEGER,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_preference_strength ON preference(strength);
CREATE INDEX idx_preference_context ON preference(context);
CREATE INDEX idx_preference_private ON preference(private);
```

### 字段说明
- **id**: 主键
- **content**: 偏好内容，如"喜欢在安静环境中深度思考"
- **strength**: 偏好强度（strong/moderate/flexible）
- **context**: 适用场景，如"学习时"、"工作中"
- **category_id**: 分类ID
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 获取强偏好用于个性化（排除私有数据）
SELECT content, context 
FROM preference 
WHERE strength = 'strong' AND private = false;

-- 特定场景下的偏好（排除私有数据）
SELECT content 
FROM preference 
WHERE context LIKE '%学习%' AND strength != 'flexible' AND private = false;
```

### 实际应用案例
制定学习计划时：
```sql
SELECT 
  p.content as preference,
  p.context,
  m.content as learning_methodology
FROM preference p
JOIN category c ON p.category_id = c.id AND c.private = false
LEFT JOIN methodology m ON m.category_id = c.id AND m.private = false
WHERE (p.context LIKE '%学习%' OR c.second_level LIKE '%学习%')
AND p.strength = 'strong' AND p.private = false;
```

---

## 9. Decision（决策表）

### 表结构设计
```sql
CREATE TABLE decision (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    reasoning TEXT,
    outcome TEXT,
    domain TEXT,
    category_id INTEGER,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_decision_domain ON decision(domain);
CREATE INDEX idx_decision_time ON decision(created_time);
CREATE INDEX idx_decision_private ON decision(private);
```

### 字段说明
- **id**: 主键
- **content**: 决策内容
- **reasoning**: 决策理由
- **outcome**: 决策结果
- **domain**: 决策领域
- **category_id**: 分类ID
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 分析决策模式（排除私有数据）
SELECT domain, COUNT(*) as decision_count,
       COUNT(CASE WHEN outcome LIKE '%成功%' THEN 1 END) as success_count
FROM decision 
WHERE private = false
GROUP BY domain;

-- 找到相似决策的历史经验（排除私有数据）
SELECT content, reasoning, outcome 
FROM decision 
WHERE domain = '技术选择' AND private = false
ORDER BY created_time DESC 
LIMIT 3;
```

---

## 10. Methodology（方法论表）

### 表结构设计
```sql
CREATE TABLE methodology (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    type TEXT,
    effectiveness TEXT CHECK(effectiveness IN ('proven', 'experimental', 'theoretical')),
    use_cases TEXT,
    persona_id INTEGER DEFAULT 1,
    category_id INTEGER,
    reference_urls TEXT,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (persona_id) REFERENCES persona(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 创建索引
CREATE INDEX idx_methodology_type ON methodology(type);
CREATE INDEX idx_methodology_effectiveness ON methodology(effectiveness);
CREATE INDEX idx_methodology_private ON methodology(private);
```

### 字段说明
- **id**: 主键
- **content**: 方法论内容
- **type**: 类型，如"问题解决"、"决策制定"
- **effectiveness**: 有效性（proven/experimental/theoretical）
- **use_cases**: 适用场景
- **persona_id**: 固定为1
- **category_id**: 分类ID
- **reference_urls**: 参考链接
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 连表查询案例
```sql
-- 获取用户的决策方法论（排除私有数据）
SELECT m.content, m.use_cases, p.personality
FROM methodology m
JOIN persona p ON m.persona_id = p.id AND p.private = false
WHERE m.type = '决策制定' AND m.effectiveness = 'proven' AND m.private = false;
```

---

## 11. Experience（经验表）

### 表结构设计
```sql
CREATE TABLE experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    field TEXT,
    expertise_level TEXT CHECK(expertise_level IN ('beginner', 'intermediate', 'proficient', 'expert')),
    years INTEGER,
    key_learnings TEXT,
    category_id INTEGER,
    reference_urls TEXT,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_experience_field ON experience(field);
CREATE INDEX idx_experience_level ON experience(expertise_level);
CREATE INDEX idx_experience_private ON experience(private);
```

### 字段说明
- **id**: 主键
- **content**: 经验内容
- **field**: 领域
- **expertise_level**: 专业程度
- **years**: 经验年数
- **key_learnings**: 关键学习
- **category_id**: 分类ID
- **reference_urls**: 参考链接
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 专业领域匹配（排除私有数据）
SELECT field, expertise_level, key_learnings 
FROM experience 
WHERE expertise_level IN ('expert', 'proficient') AND private = false;
```

---

## 12. Prediction（预测表）

### 表结构设计
```sql
CREATE TABLE prediction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    timeframe TEXT,
    basis TEXT,
    verification_status TEXT CHECK(verification_status IN ('pending', 'correct', 'incorrect', 'partial')),
    reference_urls TEXT,
    category_id INTEGER,
    persona_id INTEGER DEFAULT 1,
    private BOOLEAN DEFAULT false,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (persona_id) REFERENCES persona(id)
);

-- 创建索引
CREATE INDEX idx_prediction_timeframe ON prediction(timeframe);
CREATE INDEX idx_prediction_status ON prediction(verification_status);
CREATE INDEX idx_prediction_private ON prediction(private);
```

### 字段说明
- **id**: 主键
- **content**: 预测内容
- **timeframe**: 时间范围
- **basis**: 预测依据
- **verification_status**: 验证状态（pending/correct/incorrect/partial）
- **reference_urls**: 参考链接
- **category_id**: 分类ID
- **persona_id**: 人物ID
- **private**: 是否为私有数据，true时不读取
- **created_time**: 创建时间
- **updated_time**: 更新时间

### 使用场景
```sql
-- 验证预测准确性（排除私有数据）
SELECT 
  timeframe,
  COUNT(*) as total_predictions,
  COUNT(CASE WHEN verification_status = 'correct' THEN 1 END) as correct_count
FROM prediction 
WHERE private = false
GROUP BY timeframe;
```

---

## 综合连表查询示例

### 场景1：用户寻求职业建议
```sql
-- 获取完整的用户画像用于Prompt增强（排除私有数据）
SELECT 
  'goal' as type, g.content, c.first_level, c.second_level
FROM goal g JOIN category c ON g.category_id = c.id AND c.private = false
WHERE c.first_level = '个人成长' AND g.type = 'long_term' AND g.private = false

UNION ALL

SELECT 
  'preference' as type, p.content, c.first_level, c.second_level  
FROM preference p JOIN category c ON p.category_id = c.id AND c.private = false
WHERE c.first_level = '个人成长' AND p.strength = 'strong' AND p.private = false

UNION ALL

SELECT 
  'experience' as type, e.content, c.first_level, c.second_level
FROM experience e JOIN category c ON e.category_id = c.id AND c.private = false
WHERE c.first_level = '个人成长' AND e.expertise_level IN ('expert', 'proficient') AND e.private = false

UNION ALL

SELECT 
  'decision' as type, d.content, c.first_level, c.second_level
FROM decision d JOIN category c ON d.category_id = c.id AND c.private = false
WHERE c.first_level = '个人成长' AND d.created_time > DATE_SUB(NOW(), INTERVAL 1 YEAR) AND d.private = false;
```

### 场景2：智能任务推荐
```sql
-- 基于用户当前状态推荐下一步行动（排除私有数据）
WITH user_context AS (
    SELECT 
        COUNT(CASE WHEN type = 'todo' AND status = 'in_progress' THEN 1 END) as active_todos,
        COUNT(CASE WHEN type = 'plan' AND status = 'in_progress' THEN 1 END) as active_plans,
        AVG(CASE WHEN type = 'todo' THEN progress END) as todo_avg_progress
    FROM goal
    WHERE persona_id = 1 AND private = false
),
available_todos AS (
    SELECT 
        g.*,
        c.first_level,
        c.second_level,
        f.priority as focus_priority
    FROM goal g
    LEFT JOIN category c ON g.category_id = c.id AND c.private = false
    LEFT JOIN focus f ON f.category_id = c.id AND f.status = 'active' AND f.private = false
    WHERE g.type = 'todo' 
    AND g.status = 'planning'
    AND g.private = false
    AND NOT EXISTS (
        SELECT 1 FROM goal g2 
        WHERE g2.type = 'todo' 
        AND g2.status = 'in_progress' 
        AND g2.category_id = g.category_id
        AND g2.private = false
    )
)
SELECT * FROM available_todos
ORDER BY focus_priority DESC, created_time ASC
LIMIT 3;
```

### 场景3：学习路径规划
```sql
-- 基于用户经验和目标生成学习建议（排除私有数据）
WITH learning_context AS (
    -- 获取用户当前技能水平
    SELECT 
        e.field,
        e.expertise_level,
        e.years,
        c.first_level,
        c.second_level
    FROM experience e
    JOIN category c ON e.category_id = c.id AND c.private = false
    WHERE c.first_level = '技术' AND e.private = false
),
learning_goals AS (
    -- 获取相关学习目标
    SELECT 
        g.content,
        g.type,
        g.deadline,
        g.progress,
        c.second_level as goal_area
    FROM goal g
    JOIN category c ON g.category_id = c.id AND c.private = false
    WHERE c.first_level = '技术' 
    AND g.status = 'in_progress'
    AND g.private = false
),
learning_preferences AS (
    -- 获取学习偏好
    SELECT 
        p.content as preference,
        p.strength,
        m.content as methodology
    FROM preference p
    LEFT JOIN methodology m ON p.category_id = m.category_id AND m.private = false
    WHERE p.context LIKE '%学习%' AND p.private = false
)
SELECT * FROM learning_context
UNION ALL
SELECT * FROM learning_goals
UNION ALL  
SELECT * FROM learning_preferences;
```

### 场景4：决策支持系统
```sql
-- 当用户面临重要决策时，提供历史经验和洞察（排除私有数据）
WITH decision_context AS (
    -- 查找类似的历史决策
    SELECT 
        d.content as past_decision,
        d.reasoning,
        d.outcome,
        i.content as related_insight
    FROM decision d
    LEFT JOIN relations r ON r.target_table = 'decision' 
                          AND r.target_id = d.id 
                          AND r.source_table = 'insight'
                          AND r.private = false
    LEFT JOIN insight i ON r.source_id = i.id AND i.private = false
    WHERE d.domain = '技术选择' AND d.private = false
    ORDER BY d.created_time DESC
    LIMIT 5
),
relevant_viewpoints AS (
    -- 获取相关观点
    SELECT 
        v.content,
        v.stance,
        v.time_period
    FROM viewpoint v
    WHERE v.subject LIKE '%技术选择%'
    AND v.time_period = '当前'
    AND v.private = false
)
SELECT 'decision' as type, past_decision as content FROM decision_context
UNION ALL
SELECT 'viewpoint' as type, content FROM relevant_viewpoints;
```

### 场景5：个人成长追踪
```sql
-- 综合分析用户成长轨迹（排除私有数据）
WITH growth_timeline AS (
    SELECT 
        'viewpoint' as item_type,
        v.time_period,
        v.content,
        v.stance,
        NULL as progress,
        v.created_time
    FROM viewpoint v
    WHERE v.subject IN (
        SELECT DISTINCT subject FROM viewpoint WHERE persona_id = 1 AND private = false
    ) AND v.private = false
    
    UNION ALL
    
    SELECT 
        'goal' as item_type,
        CASE 
            WHEN g.type = 'long_term' THEN '长期规划'
            WHEN g.type = 'short_term' THEN '短期目标'
            ELSE '当前执行'
        END as time_period,
        g.content,
        NULL as stance,
        g.progress,
        g.created_time
    FROM goal g
    WHERE g.persona_id = 1 AND g.private = false
    
    UNION ALL
    
    SELECT 
        'insight' as item_type,
        '洞察时刻' as time_period,
        i.content,
        NULL as stance,
        NULL as progress,
        i.created_time
    FROM insight i
    WHERE i.impact_level = 'high' AND i.private = false
)
SELECT * FROM growth_timeline
ORDER BY created_time DESC;
```

### 场景6：认知负荷评估
```sql
-- 全面评估用户当前的认知负荷（排除私有数据）
WITH cognitive_load AS (
    SELECT 
        'active_goals' as metric,
        COUNT(*) as value,
        AVG(progress) as avg_progress
    FROM goal
    WHERE status = 'in_progress' AND private = false
    
    UNION ALL
    
    SELECT 
        'active_focus' as metric,
        COUNT(*) as value,
        AVG(priority) as avg_priority
    FROM focus
    WHERE status = 'active' AND private = false
    
    UNION ALL
    
    SELECT 
        'pending_decisions' as metric,
        COUNT(*) as value,
        NULL as extra_info
    FROM decision
    WHERE (outcome IS NULL OR outcome = '') AND private = false
),
recommendations AS (
    SELECT 
        CASE 
            WHEN (SELECT value FROM cognitive_load WHERE metric = 'active_goals') > 10 
            THEN '建议：减少并行目标，聚焦核心任务'
            WHEN (SELECT value FROM cognitive_load WHERE metric = 'active_focus') > 5 
            THEN '建议：整理关注点，建立优先级'
            ELSE '状态良好，可以接受新挑战'
        END as suggestion
)
SELECT * FROM cognitive_load
UNION ALL
SELECT 'recommendation', suggestion, NULL FROM recommendations;
```

---

## 数据库设计总结

这样的设计确保了：

1. **数据完整性**
   - 所有表都有主键和时间戳
   - 外键约束保证引用完整性
   - CHECK约束确保数据有效性

2. **查询性能优化**
   - 为常用查询字段建立索引
   - 支持高效的连表查询
   - 优化时间范围查询

3. **灵活的关联体系**
   - Relations表支持任意表间关联
   - 支持多对多关系
   - 可扩展的关系类型

4. **完整的个人画像**
   - 从基础信息到行为模式
   - 从观点到决策的完整链条
   - 支持时间维度的演变追踪

5. **实用的应用场景**
   - 目标管理（GTD方法论）
   - 知识管理（知识图谱）
   - 决策支持（历史经验）
   - 个人成长（轨迹追踪）

6. **隐私保护机制**
   - 每个表都有private字段控制数据可见性
   - 所有查询都排除private=true的数据
   - 为private字段建立索引优化查询性能
   - 支持细粒度的隐私控制
  COUNT(CASE WHEN verification_status = 'correct' THEN 1 END) as correct_count
FROM prediction 
WHERE private = false
GROUP BY timeframe;
```

---

## 综合连表查询示例

### 场景1：用户寻求职业建议
```sql
-- 获取完整的用户画像用于Prompt增强（排除私有数据）
SELECT 
  'goal' as type, g.content, c.first_level, c.second_level
FROM goal g JOIN category c ON g.category_id = c.id AND c.private = false
WHERE c.first_level = '个人成长' AND g.type = 'long_term' AND g.private = false

UNION ALL

SELECT 
  'preference' as type, p.content, c.first_level, c.second_level  
FROM preference p JOIN category c ON p.category_id = c.id AND c.private = false
WHERE c.first_level = '个人成长' AND p.strength = 'strong' AND p.private = false

UNION ALL

SELECT 
  'experience' as type, e.content, c.first_level, c.second_level
FROM experience e JOIN category c ON e.category_id = c.id AND c.private = false
WHERE c.first_level = '个人成长' AND e.expertise_level IN ('expert', 'proficient') AND e.private = false

UNION ALL

SELECT 
  'decision' as type, d.content, c.first_level, c.second_level
FROM decision d JOIN category c ON d.category_id = c.id AND c.private = false
WHERE c.first_level = '个人成长' AND d.created_time > DATE_SUB(NOW(), INTERVAL 1 YEAR) AND d.private = false;
```

### 场景2：智能任务推荐
```sql
-- 基于用户当前状态推荐下一步行动（排除私有数据）
WITH user_context AS (
    SELECT 
        COUNT(CASE WHEN type = 'todo' AND status = 'in_progress' THEN 1 END) as active_todos,
        COUNT(CASE WHEN type = 'plan' AND status = 'in_progress' THEN 1 END) as active_plans,
        AVG(CASE WHEN type = 'todo' THEN progress END) as todo_avg_progress
    FROM goal
    WHERE persona_id = 1 AND private = false
),
available_todos AS (
    SELECT 
        g.*,
        c.first_level,
        c.second_level,
        f.priority as focus_priority
    FROM goal g
    LEFT JOIN category c ON g.category_id = c.id AND c.private = false
    LEFT JOIN focus f ON f.category_id = c.id AND f.status = 'active' AND f.private = false
    WHERE g.type = 'todo' 
    AND g.status = 'planning'
    AND g.private = false
    AND NOT EXISTS (
        SELECT 1 FROM goal g2 
        WHERE g2.type = 'todo' 
        AND g2.status = 'in_progress' 
        AND g2.category_id = g.category_id
        AND g2.private = false
    )
)
SELECT * FROM available_todos
ORDER BY focus_priority DESC, created_time ASC
LIMIT 3;
```

### 场景3：学习路径规划
```sql
-- 基于用户经验和目标生成学习建议（排除私有数据）
WITH learning_context AS (
    -- 获取用户当前技能水平
    SELECT 
        e.field,
        e.expertise_level,
        e.years,
        c.first_level,
        c.second_level
    FROM experience e
    JOIN category c ON e.category_id = c.id AND c.private = false
    WHERE c.first_level = '技术' AND e.private = false
),
learning_goals AS (
    -- 获取相关学习目标
    SELECT 
        g.content,
        g.type,
        g.deadline,
        g.progress,
        c.second_level as goal_area
    FROM goal g
    JOIN category c ON g.category_id = c.id AND c.private = false
    WHERE c.first_level = '技术' 
    AND g.status = 'in_progress'
    AND g.private = false
),
learning_preferences AS (
    -- 获取学习偏好
    SELECT 
        p.content as preference,
        p.strength,
        m.content as methodology
    FROM preference p
    LEFT JOIN methodology m ON p.category_id = m.category_id AND m.private = false
    WHERE p.context LIKE '%学习%' AND p.private = false
)
SELECT * FROM learning_context
UNION ALL
SELECT * FROM learning_goals
UNION ALL  
SELECT * FROM learning_preferences;
```

### 场景4：决策支持系统
```sql
-- 当用户面临重要决策时，提供历史经验和洞察（排除私有数据）
WITH decision_context AS (
    -- 查找类似的历史决策
    SELECT 
        d.content as past_decision,
        d.reasoning,
        d.outcome,
        i.content as related_insight
    FROM decision d
    LEFT JOIN relations r ON r.target_table = 'decision' 
                          AND r.target_id = d.id 
                          AND r.source_table = 'insight'
                          AND r.private = false
    LEFT JOIN insight i ON r.source_id = i.id AND i.private = false
    WHERE d.domain = '技术选择' AND d.private = false
    ORDER BY d.created_time DESC
    LIMIT 5
),
relevant_viewpoints AS (
    -- 获取相关观点
    SELECT 
        v.content,
        v.stance,
        v.time_period
    FROM viewpoint v
    WHERE v.subject LIKE '%技术选择%'
    AND v.time_period = '当前'
    AND v.private = false
)
SELECT 'decision' as type, past_decision as content FROM decision_context
UNION ALL
SELECT 'viewpoint' as type, content FROM relevant_viewpoints;
```

### 场景5：个人成长追踪
```sql
-- 综合分析用户成长轨迹（排除私有数据）
WITH growth_timeline AS (
    SELECT 
        'viewpoint' as item_type,
        v.time_period,
        v.content,
        v.stance,
        NULL as progress,
        v.created_time
    FROM viewpoint v
    WHERE v.subject IN (
        SELECT DISTINCT subject FROM viewpoint WHERE persona_id = 1 AND private = false
    ) AND v.private = false
    
    UNION ALL
    
    SELECT 
        'goal' as item_type,
        CASE 
            WHEN g.type = 'long_term' THEN '长期规划'
            WHEN g.type = 'short_term' THEN '短期目标'
            ELSE '当前执行'
        END as time_period,
        g.content,
        NULL as stance,
        g.progress,
        g.created_time
    FROM goal g
    WHERE g.persona_id = 1 AND g.private = false
    
    UNION ALL
    
    SELECT 
        'insight' as item_type,
        '洞察时刻' as time_period,
        i.content,
        NULL as stance,
        NULL as progress,
        i.created_time
    FROM insight i
    WHERE i.impact_level = 'high' AND i.private = false
)
SELECT * FROM growth_timeline
ORDER BY created_time DESC;
```

### 场景6：认知负荷评估
```sql
-- 全面评估用户当前的认知负荷（排除私有数据）
WITH cognitive_load AS (
    SELECT 
        'active_goals' as metric,
        COUNT(*) as value,
        AVG(progress) as avg_progress
    FROM goal
    WHERE status = 'in_progress' AND private = false
    
    UNION ALL
    
    SELECT 
        'active_focus' as metric,
        COUNT(*) as value,
        AVG(priority) as avg_priority
    FROM focus
    WHERE status = 'active' AND private = false
    
    UNION ALL
    
    SELECT 
        'pending_decisions' as metric,
        COUNT(*) as value,
        NULL as extra_info
    FROM decision
    WHERE (outcome IS NULL OR outcome = '') AND private = false
),
recommendations AS (
    SELECT 
        CASE 
            WHEN (SELECT value FROM cognitive_load WHERE metric = 'active_goals') > 10 
            THEN '建议：减少并行目标，聚焦核心任务'
            WHEN (SELECT value FROM cognitive_load WHERE metric = 'active_focus') > 5 
            THEN '建议：整理关注点，建立优先级'
            ELSE '状态良好，可以接受新挑战'
        END as suggestion
)
SELECT * FROM cognitive_load
UNION ALL
SELECT 'recommendation', suggestion, NULL FROM recommendations;
```

---

## 数据库设计总结

这样的设计确保了：

1. **数据完整性**
   - 所有表都有主键和时间戳
   - 外键约束保证引用完整性
   - CHECK约束确保数据有效性

2. **查询性能优化**
   - 为常用查询字段建立索引
   - 支持高效的连表查询
   - 优化时间范围查询

3. **灵活的关联体系**
   - Relations表支持任意表间关联
   - 支持多对多关系
   - 可扩展的关系类型

4. **完整的个人画像**
   - 从基础信息到行为模式
   - 从观点到决策的完整链条
   - 支持时间维度的演变追踪

5. **实用的应用场景**
   - 目标管理（GTD方法论）
   - 知识管理（知识图谱）
   - 决策支持（历史经验）
   - 个人成长（轨迹追踪）

6. **隐私保护机制**
   - 每个表都有private字段控制数据可见性
   - 所有查询都排除private=true的数据
   - 为private字段建立索引优化查询性能
   - 支持细粒度的隐私控制