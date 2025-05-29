-- 1. Belief（信念）
CREATE TABLE belief (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    strength ENUM('strong', 'moderate', 'weak') DEFAULT 'moderate',
    domain VARCHAR(100), -- 领域：技术、人生、工作等
    related JSON, -- 相关标签
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_domain (domain),
    FULLTEXT idx_content (content)
);

-- 2. Insight（洞察）
CREATE TABLE insight (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    trigger_event TEXT, -- 触发这个洞察的事件
    impact_level ENUM('high', 'medium', 'low') DEFAULT 'medium',
    category VARCHAR(100), -- 分类：技术洞察、人际洞察、商业洞察等
    related JSON,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_impact (impact_level)
);

-- 3. Focus（关注点）
CREATE TABLE focus (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    priority INT DEFAULT 5, -- 1-10优先级
    status ENUM('active', 'paused', 'completed') DEFAULT 'active',
    context VARCHAR(200), -- 上下文：工作、学习、生活等
    related JSON,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_priority_status (priority, status)
);

-- 4. Goal（目标）- 合并长短期
CREATE TABLE goal (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    type ENUM('long_term', 'short_term') NOT NULL,
    deadline DATE,
    progress INT DEFAULT 0, -- 0-100
    status ENUM('planning', 'in_progress', 'completed', 'abandoned') DEFAULT 'planning',
    related JSON,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type_status (type, status),
    INDEX idx_deadline (deadline)
);

-- 5. Preference（偏好）
CREATE TABLE preference (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    category VARCHAR(100), -- 沟通风格、工作方式、学习方式等
    strength ENUM('strong', 'moderate', 'flexible') DEFAULT 'moderate',
    context VARCHAR(200), -- 适用场景
    related JSON,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category)
);

-- 6. Decision（决策）
CREATE TABLE decision (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    reasoning TEXT, -- 决策理由
    outcome TEXT, -- 决策结果
    confidence_level ENUM('high', 'medium', 'low') DEFAULT 'medium',
    domain VARCHAR(100),
    related JSON,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_domain_confidence (domain, confidence_level)
);

-- 7. Methodology（方法论）
CREATE TABLE methodology (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    type VARCHAR(100), -- 问题解决、决策制定、学习方法等
    effectiveness ENUM('proven', 'experimental', 'theoretical') DEFAULT 'experimental',
    use_cases TEXT, -- 适用场景描述
    related JSON,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type_effectiveness (type, effectiveness)
);

-- 8. Experience（经验）
CREATE TABLE experience (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    field VARCHAR(100), -- 领域
    expertise_level ENUM('expert', 'proficient', 'intermediate', 'beginner') DEFAULT 'intermediate',
    years INT, -- 经验年数
    key_learnings TEXT, -- 关键学习
    related JSON,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_field_level (field, expertise_level)
);

-- 9. Prediction（预测）
CREATE TABLE prediction (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    confidence DECIMAL(3,2), -- 0.00 - 1.00
    timeframe VARCHAR(50), -- 预测时间范围
    basis TEXT, -- 预测依据
    verification_status ENUM('pending', 'correct', 'incorrect', 'partial') DEFAULT 'pending',
    related JSON,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_confidence_status (confidence, verification_status)
);