# 部署文档

## 1. 概述

本文档描述了社区管理系统的部署流程，包括生产环境要求、部署前准备、部署步骤、配置说明和维护指南等内容。本指南旨在帮助系统管理员将社区管理系统部署到生产环境，并确保系统的稳定运行。

## 2. 生产环境要求

### 2.1 硬件要求

| 配置类型 | 最低配置 | 推荐配置 |
|----------|----------|----------|
| CPU | 2核 | 4核及以上 |
| 内存 | 4GB | 8GB及以上 |
| 存储 | 50GB HDD | 100GB SSD及以上 |
| 网络 | 100Mbps | 1Gbps及以上 |

### 2.2 软件要求

| 软件 | 版本 | 用途 |
|------|------|------|
| 操作系统 | Ubuntu 20.04 LTS / CentOS 8+ | 服务器操作系统 |
| Python | 3.11+ | 运行环境 |
| Django | 5.2.8 | Web框架 |
| PostgreSQL | 14+ | 数据库 |
| Nginx | 1.20+ | Web服务器/反向代理 |
| Gunicorn | 20.1+ | WSGI服务器 |
| Redis | 6.2+ | 缓存（可选） |
| SSL证书 | - | HTTPS支持 |

## 3. 部署前准备

### 3.1 服务器准备

1. **操作系统安装**：安装Ubuntu 20.04 LTS或CentOS 8+操作系统
2. **系统更新**：更新系统到最新版本
   ```bash
   # Ubuntu
   sudo apt update && sudo apt upgrade -y
   
   # CentOS
   sudo yum update -y
   ```
3. **创建专用用户**：创建一个专用用户来运行应用
   ```bash
   sudo useradd -m -s /bin/bash community
   ```
4. **安装依赖包**：
   ```bash
   # Ubuntu
   sudo apt install -y python3-pip python3-venv python3-dev build-essential libpq-dev nginx git
   
   # CentOS
   sudo yum install -y python3-pip python3-venv python3-devel gcc postgresql-devel nginx git
   ```

### 3.2 数据库准备

1. **安装PostgreSQL**：
   ```bash
   # Ubuntu
   sudo apt install -y postgresql postgresql-contrib
   
   # CentOS
   sudo yum install -y postgresql-server postgresql-contrib
   sudo postgresql-setup initdb
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```
2. **创建数据库和用户**：
   ```bash
   sudo -u postgres psql
   
   # 创建数据库
   CREATE DATABASE community_management;
   
   # 创建用户
   CREATE USER community_user WITH PASSWORD 'your_secure_password';
   
   # 授权
   GRANT ALL PRIVILEGES ON DATABASE community_management TO community_user;
   ALTER USER community_user CREATEDB;
   
   # 退出
   \q
   ```
3. **配置PostgreSQL**：
   ```bash
   # Ubuntu: 编辑 /etc/postgresql/14/main/postgresql.conf
   # CentOS: 编辑 /var/lib/pgsql/data/postgresql.conf
   sudo nano /etc/postgresql/14/main/postgresql.conf
   
   # 修改以下配置
   listen_addresses = '*'  # 允许所有IP访问
   
   # 编辑 pg_hba.conf
   sudo nano /etc/postgresql/14/main/pg_hba.conf
   
   # 添加以下行
   host    all             all             0.0.0.0/0               md5
   
   # 重启PostgreSQL
   sudo systemctl restart postgresql
   ```

### 3.3 代码准备

1. **切换到专用用户**：
   ```bash
   sudo su - community
   ```
2. **克隆代码库**：
   ```bash
   git clone https://github.com/yourusername/community_management.git
   cd community_management
   ```
3. **创建虚拟环境**：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **安装依赖**：
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 4. 部署步骤

### 4.1 配置应用

1. **创建环境变量文件**：
   ```bash
   cp .env.example .env
   nano .env
   ```

2. **配置环境变量**：
   ```
   # 基本配置
   SECRET_KEY=your_secure_secret_key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   
   # 数据库配置
   DATABASE_URL=postgresql://community_user:your_secure_password@localhost:5432/community_management
   
   # 邮件配置（可选）
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.yourdomain.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=noreply@yourdomain.com
   EMAIL_HOST_PASSWORD=your_email_password
   
   # Redis配置（可选）
   REDIS_URL=redis://localhost:6379/0
   
   # 日志配置
   LOG_LEVEL=INFO
   ```

3. **配置Django设置**：
   ```bash
   nano community_management/settings.py
   ```

   确保以下配置正确：
   ```python
   # 基本配置
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   
   # 数据库配置
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'community_management',
           'USER': 'community_user',
           'PASSWORD': 'your_secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   
   # 静态文件配置
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   
   # 媒体文件配置
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   
   # 安全配置
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

### 4.2 数据库迁移

1. **运行数据库迁移**：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **创建超级用户**：
   ```bash
   python manage.py createsuperuser
   ```

3. **收集静态文件**：
   ```bash
   python manage.py collectstatic --noinput
   ```

### 4.3 配置Gunicorn

1. **创建Gunicorn配置文件**：
   ```bash
   nano gunicorn_config.py
   ```

2. **添加配置内容**：
   ```python
   bind = "127.0.0.1:8000"
   workers = 3
   worker_class = "sync"
   timeout = 120
   loglevel = "info"
   accesslog = "gunicorn_access.log"
   errorlog = "gunicorn_error.log"
   capture_output = True
   ```

3. **创建systemd服务文件**：
   ```bash
   sudo nano /etc/systemd/system/community_management.service
   ```

4. **添加服务配置**：
   ```ini
   [Unit]
   Description=Gunicorn instance to serve community_management
   After=network.target
   
   [Service]
   User=community
   Group=www-data
   WorkingDirectory=/home/community/community_management
   Environment="PATH=/home/community/community_management/venv/bin"
   ExecStart=/home/community/community_management/venv/bin/gunicorn --config gunicorn_config.py community_management.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **启动并启用服务**：
   ```bash
   sudo systemctl start community_management
   sudo systemctl enable community_management
   ```

### 4.4 配置Nginx

1. **创建Nginx配置文件**：
   ```bash
   sudo nano /etc/nginx/sites-available/community_management
   ```

2. **添加Nginx配置**：
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl;
       server_name yourdomain.com www.yourdomain.com;
       
       # SSL证书配置
       ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
       ssl_certificate_key /etc/ssl/private/yourdomain.com.key;
       
       # SSL优化配置
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_prefer_server_ciphers off;
       ssl_session_timeout 1d;
       ssl_session_cache shared:MozSSL:10m;
       ssl_session_tickets off;
       
       # 安全头配置
       add_header Strict-Transport-Security "max-age=63072000" always;
       add_header X-Frame-Options SAMEORIGIN;
       add_header X-Content-Type-Options nosniff;
       add_header X-XSS-Protection "1; mode=block";
       
       # 静态文件配置
       location /static/ {
           alias /home/community/community_management/staticfiles/;
           expires 30d;
       }
       
       # 媒体文件配置
       location /media/ {
           alias /home/community/community_management/media/;
           expires 30d;
       }
       
       # 应用代理配置
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           
           # WebSocket支持（如果需要）
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

3. **启用站点**：
   ```bash
   sudo ln -s /etc/nginx/sites-available/community_management /etc/nginx/sites-enabled/
   ```

4. **测试Nginx配置**：
   ```bash
   sudo nginx -t
   ```

5. **重启Nginx**：
   ```bash
   sudo systemctl restart nginx
   ```

### 4.5 配置防火墙

1. **允许HTTP和HTTPS流量**：
   ```bash
   # Ubuntu（使用ufw）
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw reload
   
   # CentOS（使用firewalld）
   sudo firewall-cmd --permanent --add-service=http
   sudo firewall-cmd --permanent --add-service=https
   sudo firewall-cmd --reload
   ```

## 5. 环境变量配置

### 5.1 必要环境变量

| 变量名 | 描述 | 示例值 |
|--------|------|--------|
| `SECRET_KEY` | Django密钥，用于加密会话数据 | `django-insecure-xxxxxxxxxxxxxxxxxx` |
| `DEBUG` | 是否开启调试模式 | `False`（生产环境） |
| `ALLOWED_HOSTS` | 允许访问的主机名 | `yourdomain.com,www.yourdomain.com` |
| `DATABASE_URL` | 数据库连接URL | `postgresql://user:password@localhost:5432/dbname` |
| `EMAIL_BACKEND` | 邮件后端 | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | SMTP服务器 | `smtp.yourdomain.com` |
| `EMAIL_PORT` | SMTP端口 | `587` |
| `EMAIL_USE_TLS` | 是否使用TLS | `True` |
| `EMAIL_HOST_USER` | SMTP用户名 | `noreply@yourdomain.com` |
| `EMAIL_HOST_PASSWORD` | SMTP密码 | `your_email_password` |

### 5.2 可选环境变量

| 变量名 | 描述 | 示例值 |
|--------|------|--------|
| `REDIS_URL` | Redis缓存连接URL | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Celery消息队列URL | `redis://localhost:6379/1` |
| `CELERY_RESULT_BACKEND` | Celery结果后端URL | `redis://localhost:6379/2` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `LOG_FILE` | 日志文件路径 | `/var/log/community_management.log` |
| `STATIC_URL` | 静态文件URL前缀 | `/static/` |
| `MEDIA_URL` | 媒体文件URL前缀 | `/media/` |

## 6. 维护指南

### 6.1 日志管理

1. **应用日志**：
   ```bash
   # 查看Gunicorn访问日志
   tail -f /home/community/community_management/gunicorn_access.log
   
   # 查看Gunicorn错误日志
   tail -f /home/community/community_management/gunicorn_error.log
   ```

2. **Nginx日志**：
   ```bash
   # 查看Nginx访问日志
   tail -f /var/log/nginx/access.log
   
   # 查看Nginx错误日志
   tail -f /var/log/nginx/error.log
   ```

3. **Django日志**：
   ```bash
   # 查看Django日志（如果配置了）
   tail -f /var/log/community_management.log
   ```

### 6.2 备份与恢复

1. **数据库备份**：
   ```bash
   # 备份数据库
   pg_dump -U community_user -h localhost community_management > community_management_backup_$(date +%Y%m%d_%H%M%S).sql
   
   # 压缩备份文件
   gzip community_management_backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **数据库恢复**：
   ```bash
   # 解压备份文件
   gunzip community_management_backup_20250101_120000.sql.gz
   
   # 恢复数据库
   psql -U community_user -h localhost community_management < community_management_backup_20250101_120000.sql
   ```

3. **文件备份**：
   ```bash
   # 备份静态文件和媒体文件
   tar -czf community_management_files_$(date +%Y%m%d_%H%M%S).tar.gz /home/community/community_management/staticfiles /home/community/community_management/media
   ```

### 6.3 系统更新

1. **更新应用代码**：
   ```bash
   sudo su - community
   cd community_management
   git pull origin main
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic --noinput
   deactivate
   exit
   
   # 重启服务
   sudo systemctl restart community_management
   sudo systemctl restart nginx
   ```

2. **更新系统依赖**：
   ```bash
   # Ubuntu
   sudo apt update && sudo apt upgrade -y
   
   # CentOS
   sudo yum update -y
   ```

### 6.4 常见问题排查

1. **应用无法启动**：
   ```bash
   # 查看应用日志
   sudo journalctl -u community_management
   tail -f /home/community/community_management/gunicorn_error.log
   ```

2. **Nginx无法启动**：
   ```bash
   # 检查Nginx配置
   sudo nginx -t
   
   # 查看Nginx日志
   tail -f /var/log/nginx/error.log
   ```

3. **数据库连接问题**：
   ```bash
   # 测试数据库连接
   psql -U community_user -h localhost -d community_management
   
   # 查看PostgreSQL日志
   tail -f /var/log/postgresql/postgresql-14-main.log
   ```

4. **静态文件无法访问**：
   ```bash
   # 检查静态文件权限
   ls -la /home/community/community_management/staticfiles
   
   # 检查Nginx配置
   sudo nginx -t
   ```

## 7. 性能优化

### 7.1 数据库优化

1. **添加索引**：根据查询模式为常用字段添加索引
2. **优化查询**：避免N+1查询问题，使用select_related和prefetch_related
3. **定期清理**：定期清理无用数据，优化数据库性能
4. **配置连接池**：使用数据库连接池管理数据库连接

### 7.2 缓存优化

1. **启用Redis缓存**：
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://localhost:6379/0',
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
           }
       }
   }
   ```

2. **缓存常用视图**：
   ```python
   from django.views.decorators.cache import cache_page
   
   @cache_page(60 * 15)  # 缓存15分钟
   def community_list(request):
       # 视图逻辑
   ```

3. **缓存模板片段**：
   ```html
   {% load cache %}
   {% cache 3600 community_stats %}
       <!-- 需要缓存的模板片段 -->
   {% endcache %}
   ```

### 7.3 Gunicorn优化

1. **调整workers数量**：
   ```python
   # gunicorn_config.py
   workers = 4  # 一般设置为CPU核心数 * 2 + 1
   ```

2. **使用异步worker**：
   ```python
   # gunicorn_config.py
   worker_class = "gevent"  # 使用gevent异步worker
   workers = 10
   ```

### 7.4 Nginx优化

1. **启用gzip压缩**：
   ```nginx
   # 在http块中添加
   gzip on;
   gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
   ```

2. **启用缓存**：
   ```nginx
   # 在server块中添加
   location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

3. **调整worker_processes**：
   ```nginx
   # 在nginx.conf的http块中
   worker_processes auto;  # 设置为CPU核心数
   ```

## 8. 安全配置

### 8.1 基础安全配置

1. **禁用调试模式**：
   ```python
   DEBUG = False
   ```

2. **设置允许的主机**：
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

3. **启用HTTPS**：
   ```python
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

4. **设置安全头**：
   ```python
   SECURE_BROWSER_XSS_FILTER = True
   SECURE_CONTENT_TYPE_NOSNIFF = True
   X_FRAME_OPTIONS = 'DENY'
   ```

### 8.2 定期安全更新

1. **定期更新系统**：每月至少更新一次系统依赖
2. **定期更新应用依赖**：使用`pip-audit`或`safety`检查依赖漏洞
   ```bash
   pip install pip-audit
   pip-audit
   ```

3. **定期扫描安全漏洞**：使用OWASP ZAP或其他安全扫描工具定期扫描系统

## 9. 监控与告警

### 9.1 系统监控

1. **安装监控工具**：
   ```bash
   # 安装Prometheus和Grafana
   # 参考官方文档：https://prometheus.io/docs/introduction/overview/
   # 参考官方文档：https://grafana.com/docs/grafana/latest/setup-grafana/
   ```

2. **配置应用监控**：
   ```bash
   # 安装django-prometheus
   pip install django-prometheus
   ```

3. **配置Prometheus**：
   ```yaml
   # prometheus.yml
   scrape_configs:
     - job_name: 'community_management'
       static_configs:
         - targets: ['localhost:8000']
   ```

### 9.2 告警配置

1. **配置Grafana告警**：
   - 设置CPU使用率告警
   - 设置内存使用率告警
   - 设置磁盘空间告警
   - 设置应用响应时间告警

2. **配置日志告警**：
   - 使用ELK Stack或Graylog收集和分析日志
   - 设置错误日志告警
   - 设置安全事件告警

## 10. 扩容计划

### 10.1 垂直扩容

1. **增加CPU和内存**：根据系统负载增加服务器的CPU和内存
2. **使用高性能存储**：将HDD更换为SSD，提高I/O性能
3. **优化数据库**：升级数据库版本，优化数据库配置

### 10.2 水平扩容

1. **负载均衡**：使用Nginx或其他负载均衡器实现多节点负载均衡
2. **数据库主从复制**：实现数据库主从复制，提高数据库读取性能
3. **分布式缓存**：使用Redis集群，提高缓存性能
4. **容器化部署**：使用Docker和Kubernetes实现容器化部署和自动扩缩容

## 11. 总结

本文档详细描述了社区管理系统的部署流程，包括生产环境要求、部署前准备、部署步骤、配置说明和维护指南等内容。通过遵循本指南，系统管理员可以将社区管理系统部署到生产环境，并确保系统的稳定运行。

系统部署后，建议定期进行系统维护和安全更新，确保系统的安全性和可靠性。同时，建议配置监控和告警系统，及时发现和解决系统问题。

如果在部署过程中遇到问题，可以参考本文档的常见问题排查部分，或联系技术支持团队获取帮助。