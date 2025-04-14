# 农作物病虫害识别系统后端

这是使用 Flask 框架开发的农作物病虫害识别系统后端 API。

## 项目结构

```
flask_backend/
├── app/
│   ├── __init__.py    # 应用工厂函数
│   ├── config.py      # 配置文件
│   ├── models.py      # 数据库模型
│   ├── routes/        # 路由目录
│   │   ├── __init__.py
│   │   ├── auth.py    # 认证路由
│   │   ├── category.py # 分类路由
│   │   └── disease.py  # 病害路由
└── run.py             # 入口文件
```

## 数据库设计

系统使用了以下数据表：

1. `user` - 用户表
2. `crop_categories` - 农作物分类表
3. `diseases` - 病虫害表

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置数据库：
在 `app/config.py` 文件中，修改 `SQLALCHEMY_DATABASE_URI` 为你的数据库连接字符串。

3. 运行应用：
```bash
python run.py
```

## API 接口

### 1. 用户认证接口

- 注册: `POST /api/auth/register`
- 登录: `POST /api/auth/login`
- 获取个人信息: `GET /api/auth/profile`
- 更新个人信息: `PUT /api/auth/profile`

### 2. 农作物分类接口

- 获取所有分类: `GET /api/categories`
- 获取单个分类: `GET /api/categories/<id>`
- 创建分类: `POST /api/categories` (需要管理员权限)
- 更新分类: `PUT /api/categories/<id>` (需要管理员权限)
- 删除分类: `DELETE /api/categories/<id>` (需要管理员权限)

### 3. 病害接口

- 获取所有病害: `GET /api/diseases`
- 按分类获取病害: `GET /api/diseases?category_id=<id>`
- 获取单个病害: `GET /api/diseases/<id>`
- 创建病害: `POST /api/diseases` (需要管理员权限)
- 更新病害: `PUT /api/diseases/<id>` (需要管理员权限)
- 删除病害: `DELETE /api/diseases/<id>` (需要管理员权限) 