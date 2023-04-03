# lucky
# 一、项目安装及启动
#### 1. 将代码拉到本地：git clone https://gitlab.sy.soyoung.com/wuchaofan/automatic.git
#### 2. 进入到automatic（项目根目录）目录下

### 后端
#### 3. 安装依赖包：pip3 install -r requirements.txt
###### 遇到某个包安装失败，可以先将对应包注释掉，后面单独安装
#### 4. 默认使用10.10.20.84公用数据库，如果需要配置本地数据库，将application/env.py的DATABASE_TYPE改成"SQLITE"即可，同时执行python3 manager.py makemigrations & python3 manager.py & migrate执行数据库同步
#### 5. 启动服务：python3 manager.py runserver 127.0.0.1:8000
#### 6. 启动celery: celery -A application worker -l info --logfile=celery.log
#### 7. 启动celery: celery -A application beat -l info --logfile=celery.log

### 前端
#### 6. automatic/web目录下
#### 7. 安装依赖包：npm install(安装失败，删掉web目录下node_modules重试一下)
#### 8. 启动服务：npm run dev
#### 9. 默认localhost:8080访问（登录账号：admin/123456）

# 二、新建项目
### 后端
#### 1. 创建项目
#### 2. 创建model
#### 3. 创建序列化方法
#### 4. 创建过滤方法
#### 5. 创建model
#### 6. 创建视图
#### 7. 新建url路由
#### 8. 将项目加入到Django install_apps中

### 前端


