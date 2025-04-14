-- 用户表迁移SQL
-- 修改用户表结构，移除微信登录依赖，改为账号密码登录

-- 修改openid字段为可空（如果之前是NOT NULL的话）
ALTER TABLE users MODIFY COLUMN openid VARCHAR(100) NULL;

-- 如果username和password字段不存在，则添加这些字段
-- 检查username字段是否存在
SET @usernamecol = (SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'users' 
                    AND COLUMN_NAME = 'username'
                    AND TABLE_SCHEMA = DATABASE());

-- 如果username字段不存在，添加该字段
SET @sqlstmt = IF(@usernamecol = 0, 
                  'ALTER TABLE users ADD COLUMN username VARCHAR(50) NULL UNIQUE COMMENT "用户名"', 
                  'SELECT "username字段已存在，跳过创建" as msg');
PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 检查password字段是否存在
SET @passwordcol = (SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'users' 
                    AND COLUMN_NAME = 'password'
                    AND TABLE_SCHEMA = DATABASE());

-- 如果password字段不存在，添加该字段
SET @sqlstmt = IF(@passwordcol = 0, 
                  'ALTER TABLE users ADD COLUMN password VARCHAR(100) NULL COMMENT "密码"', 
                  'SELECT "password字段已存在，跳过创建" as msg');
PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 创建管理员账号（如果需要）
INSERT INTO users (username, password, nickname, user_type, status, create_time, update_time)
SELECT 'admin', MD5('admin123'), '系统管理员', 2, 1, NOW(), NOW()
FROM DUAL
WHERE NOT EXISTS (SELECT * FROM users WHERE username = 'admin');

-- 创建专家测试账号（如果需要）
INSERT INTO users (username, password, nickname, user_type, status, create_time, update_time)
SELECT 'expert', MD5('expert123'), '农业专家', 1, 1, NOW(), NOW()
FROM DUAL
WHERE NOT EXISTS (SELECT * FROM users WHERE username = 'expert');

-- 创建普通用户测试账号（如果需要）
INSERT INTO users (username, password, nickname, user_type, status, create_time, update_time)
SELECT 'user', MD5('user123'), '普通用户', 0, 1, NOW(), NOW()
FROM DUAL
WHERE NOT EXISTS (SELECT * FROM users WHERE username = 'user');

-- 更新任何已有的没有用户名的用户记录（如果有的话）
UPDATE users
SET username = CONCAT('user_', user_id),
    password = MD5(CONCAT('default_', user_id)),
    nickname = COALESCE(nickname, CONCAT('用户', user_id))
WHERE username IS NULL AND openid IS NOT NULL; 