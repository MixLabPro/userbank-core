# Profile数据库字段详细使用指南

## 1. Persona（人物档案表）- 系统核心

### 字段说明
- **id**: 主键，固定为1（系统只维护一个人物档案）
- **name**: 用户姓名，如"张三"
- **gender**: 性别，影响语言风格和称呼方式
- **personality**: 性格描述，如"内向思考型，注重细节，喜欢深度分析"
- **avatar_url**: 头像链接（可选）
- **bio**: 个人简介（可选）

### 使用场景
```sql
-- 获取用户基本信息，用于个性化回复
SELECT name, gender, personality FROM persona WHERE id = 1;

-- 在生成回复时的应用
-- 如果personality包含"内向"，则回复更加深思熟虑
-- 如果gender为"female"，语言风格可能更细腻
```

### 连表使用
```sql
-- 查询某人的所有观点
SELECT v.*, p.name, p.personality 
FROM viewpoint v 
JOIN persona p ON v.persona_id = p.id 
WHERE v.persona_id = 1;
```

---

## 2. Category（分类体系表）

### 字段说明
- **id**: 分类ID
- **first_level**: 一级目录，如"技术"、"生活"、"商业"
- **second_level**: 二级目录，如"编程开发"、"人际关系"、"投资理财"
- **description**: 分类描述
- **is_active**: 是否启用该分类

### 使用场景
```sql
-- 按主题查询内容
SELECT c.first_level, c.second_level, COUNT(v.id) as viewpoint_count
FROM category c
LEFT JOIN viewpoint v ON c.id = v.category_id
GROUP BY c.id;

-- 用于Prompt增强：找到用户在某领域的所有相关内容
SELECT 'viewpoint' as type, v.content, c.first_level, c.second_level
FROM viewpoint v 
JOIN category c ON v.category_id = c.id 
WHERE c.first_level = '技术'
UNION ALL
SELECT 'experience' as type, e.content, c.first_level, c.second_level
FROM experience e 
JOIN category c ON e.category_id = c.id 
WHERE c.first_level = '技术';
```

### 实际应用案例
当用户问"帮我设计一个系统"时：
```sql
-- 查询技术相关的所有用户数据
SELECT v.content as viewpoint, m.content as methodology, e.content as experience
FROM category c
LEFT JOIN viewpoint v ON c.id = v.category_id
LEFT JOIN methodology m ON c.id = m.category_id  
LEFT JOIN experience e ON c.id = e.category_id
WHERE c.first_level = '技术' AND c.second_level = '系统架构';
```

---

## 3. Relations（通用关联表）

### 字段说明
- **source_table**: 源表名，如"insight"
- **source_id**: 源记录ID
- **target_table**: 目标表名，如"decision"
- **target_id**: 目标记录ID
- **relation_type**: 关联类型，如"inspired_by"、"conflicts_with"、"supports"
- **strength**: 关联强度（strong/medium/weak）
- **note**: 关联说明

### 使用场景
```sql
-- 找到启发某个决策的所有洞察
SELECT i.content as insight_content, r.note
FROM relations r
JOIN insight i ON r.source_table = 'insight' AND r.source_id = i.id
WHERE r.target_table = 'decision' AND r.target_id = 123 
AND r.relation_type = 'inspired_by';

-- 构建知识图谱：找到某个观点的所有相关内容
SELECT r.target_table, r.target_id, r.relation_type
FROM relations r 
WHERE r.source_table = 'viewpoint' AND r.source_id = 456;
```

### 实际应用案例
构建用户思维脉络：
```sql
-- 当用户提到某个话题时，找到相关的思维链条
WITH RECURSIVE thought_chain AS (
  SELECT source_table, source_id, target_table, target_id, 1 as level
  FROM relations 
  WHERE source_table = 'viewpoint' AND source_id = 123
  UNION ALL
  SELECT r.source_table, r.source_id, r.target_table, r.target_id, tc.level + 1
  FROM relations r
  JOIN thought_chain tc ON r.source_table = tc.target_table AND r.source_id = tc.target_id
  WHERE tc.level < 3
)
SELECT * FROM thought_chain;
```

---

## 4. Viewpoint（观点表）

### 字段说明
- **content**: 观点内容，如"我认为微服务架构适合团队规模超过20人的项目"
- **subject**: 观点主题，如"微服务架构"
- **stance**: 观点立场（强烈支持到强烈反对）
- **source**: 观点来源，如"项目实践经验"、"技术书籍学习"
- **persona_id**: 固定为1（指向唯一的persona记录）
- **time_period**: 时间段，如"大学时期"、"工作第3年"、"当前"
- **reference_urls**: 参考链接数组
- **category_id**: 分类ID

### 使用场景
```sql
-- 分析观点演变：查看用户在不同时期对同一主题的观点变化
SELECT time_period, stance, content 
FROM viewpoint 
WHERE subject = '微服务架构' 
ORDER BY CASE time_period 
  WHEN '大学时期' THEN 1 
  WHEN '工作第1年' THEN 2 
  WHEN '工作第3年' THEN 3 
  WHEN '当前' THEN 4 
END;

-- Prompt增强：获取用户对当前话题的立场
SELECT content, stance, source 
FROM viewpoint 
WHERE subject LIKE '%架构%' AND time_period = '当前';
```

### 实际应用案例
用户问"我应该选择微服务还是单体架构？"
```sql
-- 查询用户的相关观点和经验
SELECT 
  v.content as viewpoint,
  v.stance,
  v.time_period,
  e.content as related_experience,
  c.first_level, c.second_level
FROM viewpoint v
LEFT JOIN category c ON v.category_id = c.id
LEFT JOIN experience e ON e.category_id = c.id
WHERE v.subject LIKE '%架构%' OR e.field LIKE '%架构%';
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

### 字段说明
- **content**: 洞察内容，如"技术选择往往反映了团队的组织结构"
- **trigger_event**: 触发事件，如"项目重构失败的复盘"
- **impact_level**: 影响程度（high/medium/low）
- **category_id**: 分类ID
- **reference_urls**: 参考链接

### 使用场景
```sql
-- 获取高影响力的洞察用于Prompt增强
SELECT content, trigger_event 
FROM insight 
WHERE impact_level = 'high' 
ORDER BY created_time DESC 
LIMIT 5;

-- 根据触发事件找相关洞察
SELECT content 
FROM insight 
WHERE trigger_event LIKE '%失败%' OR trigger_event LIKE '%挫折%';
```

### 实际应用案例
用户遇到技术选择困难时：
```sql
-- 查询相关的洞察和决策经验
SELECT i.content as insight, d.content as past_decision, d.outcome
FROM insight i
JOIN category c1 ON i.category_id = c1.id
LEFT JOIN decision d ON d.category_id IN (
  SELECT id FROM category WHERE first_level = c1.first_level
)
WHERE c1.first_level = '技术' AND i.impact_level = 'high';
```

---

## 6. Focus（关注点表）

### 字段说明
- **content**: 关注内容，如"学习Rust编程语言"
- **priority**: 优先级（1-10）
- **status**: 状态（active/paused/completed）
- **context**: 上下文，如"工作"、"个人提升"
- **category_id**: 分类ID
- **deadline**: 截止日期

### 使用场景
```sql
-- 获取当前活跃的关注点，评估用户认知负荷
SELECT content, priority, deadline 
FROM focus 
WHERE status = 'active' 
ORDER BY priority DESC;

-- 时间冲突检测
SELECT COUNT(*) as active_high_priority_items
FROM focus 
WHERE status = 'active' AND priority >= 8;
```

### 实际应用案例
用户想学习新技术时：
```sql
-- 评估当前负荷，给出建议
SELECT 
  COUNT(*) as total_active,
  AVG(priority) as avg_priority,
  COUNT(CASE WHEN deadline < DATE_ADD(NOW(), INTERVAL 30 DAY) THEN 1 END) as urgent_items
FROM focus 
WHERE status = 'active';
```

如果active_items > 5且avg_priority > 7：
```
根据你当前的关注点分析：
- 你有5个高优先级的活跃目标
- 平均优先级8.2，认知负荷较重
- 建议：先完成2个现有目标再开始新学习
```

---

## 7. Goal（目标表）

### 字段说明
- **content**: 目标内容
- **type**: 类型（long_term/short_term）
- **deadline**: 截止日期
- **progress**: 进度（0-100）
- **status**: 状态（planning/in_progress/completed/abandoned）
- **category_id**: 分类ID

### 使用场景
```sql
-- 目标进展分析
SELECT type, AVG(progress) as avg_progress, COUNT(*) as count
FROM goal 
WHERE status = 'in_progress'
GROUP BY type;

-- 找到停滞的目标
SELECT content, progress, DATEDIFF(NOW(), updated_time) as days_since_update
FROM goal 
WHERE status = 'in_progress' AND updated_time < DATE_SUB(NOW(), INTERVAL 14 DAY);
```

### 连表查询案例
```sql
-- 将当前决策与长期目标对齐
SELECT g.content as goal, d.content as recent_decision, d.outcome
FROM goal g
JOIN category c ON g.category_id = c.id
JOIN decision d ON d.category_id = c.id
WHERE g.type = 'long_term' AND g.status = 'in_progress'
AND d.created_time > DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

## 8. Preference（偏好表）

### 字段说明
- **content**: 偏好内容，如"喜欢在安静环境中深度思考"
- **strength**: 偏好强度（strong/moderate/flexible）
- **context**: 适用场景，如"学习时"、"工作中"
- **category_id**: 分类ID

### 使用场景
```sql
-- 获取强偏好用于个性化
SELECT content, context 
FROM preference 
WHERE strength = 'strong';

-- 特定场景下的偏好
SELECT content 
FROM preference 
WHERE context LIKE '%学习%' AND strength != 'flexible';
```

### 实际应用案例
制定学习计划时：
```sql
SELECT 
  p.content as preference,
  p.context,
  m.content as learning_methodology
FROM preference p
JOIN category c ON p.category_id = c.id
LEFT JOIN methodology m ON m.category_id = c.id
WHERE (p.context LIKE '%学习%' OR c.second_level LIKE '%学习%')
AND p.strength = 'strong';
```

---

## 9. Decision（决策表）

### 字段说明
- **content**: 决策内容
- **reasoning**: 决策理由
- **outcome**: 决策结果
- **domain**: 决策领域
- **category_id**: 分类ID

### 使用场景
```sql
-- 分析决策模式
SELECT domain, COUNT(*) as decision_count,
       COUNT(CASE WHEN outcome LIKE '%成功%' THEN 1 END) as success_count
FROM decision 
GROUP BY domain;

-- 找到相似决策的历史经验
SELECT content, reasoning, outcome 
FROM decision 
WHERE domain = '技术选择' 
ORDER BY created_time DESC 
LIMIT 3;
```

---

## 10. Methodology（方法论表）

### 字段说明
- **content**: 方法论内容
- **type**: 类型，如"问题解决"、"决策制定"
- **effectiveness**: 有效性（proven/experimental/theoretical）
- **use_cases**: 适用场景
- **persona_id**: 固定为1
- **category_id**: 分类ID
- **reference_urls**: 参考链接

### 连表查询案例
```sql
-- 获取用户的决策方法论
SELECT m.content, m.use_cases, p.personality
FROM methodology m
JOIN persona p ON m.persona_id = p.id
WHERE m.type = '决策制定' AND m.effectiveness = 'proven';
```

---

## 11. Experience（经验表）

### 字段说明
- **content**: 经验内容
- **field**: 领域
- **expertise_level**: 专业程度
- **years**: 经验年数
- **key_learnings**: 关键学习
- **category_id**: 分类ID
- **reference_urls**: 参考链接

### 使用场景
```sql
-- 专业领域匹配
SELECT field, expertise_level, key_learnings 
FROM experience 
WHERE expertise_level IN ('expert', 'proficient');
```

---

## 12. Prediction（预测表）

### 字段说明
- **content**: 预测内容
- **timeframe**: 时间范围
- **basis**: 预测依据
- **verification_status**: 验证状态
- **reference_urls**: 参考链接
- **category_id**: 分类ID

### 使用场景
```sql
-- 验证预测准确性
SELECT 
  timeframe,
  COUNT(*) as total_predictions,
  COUNT(CASE WHEN verification_status = 'correct' THEN 1 END) as correct_count
FROM prediction 
GROUP BY timeframe;
```

---

## 综合连表查询示例

### 场景：用户寻求职业建议
```sql
-- 获取完整的用户画像用于Prompt增强
SELECT 
  'goal' as type, g.content, c.first_level, c.second_level
FROM goal g JOIN category c ON g.category_id = c.id 
WHERE c.first_level = '个人成长' AND g.type = 'long_term'

UNION ALL

SELECT 
  'preference' as type, p.content, c.first_level, c.second_level  
FROM preference p JOIN category c ON p.category_id = c.id
WHERE c.first_level = '个人成长' AND p.strength = 'strong'

UNION ALL

SELECT 
  'experience' as type, e.content, c.first_level, c.second_level
FROM experience e JOIN category c ON e.category_id = c.id  
WHERE c.first_level = '个人成长' AND e.expertise_level IN ('expert', 'proficient')

UNION ALL

SELECT 
  'decision' as type, d.content, c.first_level, c.second_level
FROM decision d JOIN category c ON d.category_id = c.id
WHERE c.first_level = '个人成长' AND d.created_time > DATE_SUB(NOW(), INTERVAL 1 YEAR);
```

这样的设计确保了：
1. **数据完整性**：persona唯一性，分类体系统一
2. **查询灵活性**：支持多维度数据组合
3. **个性化深度**：从基础信息到行为模式的全方位覆盖
4. **关联性**：通过relations表支持复杂的知识图谱构建