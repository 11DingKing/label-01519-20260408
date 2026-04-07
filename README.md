# 第六师兵团库房管理系统

## 快速启动

### Docker 一键部署（推荐）

```bash
docker-compose up --build -d
```

启动后访问：http://localhost:8081

### 本地开发环境

```bash
cd backend
python -m venv venv
source venv/bin/activate

# 全程使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# SQLite（默认）
python manage.py migrate
python scripts/init_db.py
python manage.py runserver

# MySQL
USE_MYSQL=true DB_HOST=127.0.0.1 python manage.py migrate
USE_MYSQL=true DB_HOST=127.0.0.1 python scripts/init_db.py
USE_MYSQL=true DB_HOST=127.0.0.1 python manage.py runserver
```

## 测试账号

| 用户名 | 密码 |
|--------|------|
| admin | 123456789 |

## 技术栈

### 后端
- Django + Django REST Framework
- django-filter（多条件筛选，FilterSet 类）
- django-crispy-forms + crispy-bootstrap5（表单美化）
- django-import-export（数据导入导出）
- django-storages（文件存储，支持本地/S3）
- django-debug-toolbar（开发调试）
- django-crontab（定时任务）
- JWT 认证
- 企业级日志系统

### 前端
- HTML5 + CSS3 + JavaScript（模块化）
- 蓝色科技感 UI 主题
- 独立 CSS/JS 组件模块

## 功能菜单

- 仪表盘
- 货物入库
- 类型管理（单位/品类/品种）
- 查询导出
- 每日报表
- 预警
- 审批区域
- 人员管理（考勤/出库人员）

## 项目结构

```
backend/
├── apps/
│   ├── authentication/     # 认证模块
│   │   ├── filters.py      # django-filter 过滤器
│   │   ├── forms.py        # django-crispy-forms 表单
│   │   └── views.py
│   ├── warehouse/          # 库房管理
│   │   ├── filters.py      # django-filter 过滤器
│   │   ├── forms.py        # django-crispy-forms 表单
│   │   ├── resources.py    # django-import-export 资源
│   │   └── views.py
│   ├── personnel/          # 人员管理
│   ├── reports/            # 报表模块
│   └── core/               # 核心模块（日志、异常）
├── static/
│   ├── css/components/     # CSS 组件模块
│   └── js/components/      # JS 组件模块
├── templates/              # HTML 模板
└── logs/                   # 日志文件
```

## 开发调试

### Debug Toolbar
本地 DEBUG=True 时自动启用，页面右侧显示调试面板。

### 日志文件
```
backend/logs/
├── app.log           # 应用日志
├── error.log         # 错误日志
├── access.log        # 访问日志
├── security.log      # 安全日志
└── performance.log   # 性能日志
```

### 运行测试
```bash
cd backend
python manage.py test apps --verbosity=2
```

## 定时任务

```bash
python manage.py crontab add    # 添加
python manage.py crontab show   # 查看
```

| 任务 | 时间 |
|------|------|
| 库存预警检查 | 每天 01:00 |
| 每日报表生成 | 每天 02:00 |
| 日志清理 | 每周日 03:00 |

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| USE_MYSQL | 使用 MySQL | false |
| DB_HOST | 数据库地址 | db |
| DJANGO_DEBUG | 调试模式 | True |
| STORAGE_BACKEND | 存储后端 (local/s3) | local |
