# AI学习任务管理器 V2（MySQL版）

这是 V1 JSON 文件版升级后的数据库版，适合在 PyCharm 中学习 Python + MySQL + CRUD。

## 1. 项目结构

```text
AI学习任务管理器_V2/
├── main.py
├── task_manager.py
├── database.py
├── requirements.txt
├── init_database.sql
└── README.md
```

## 2. 使用环境

- Windows
- PyCharm
- Python 3.10+
- MySQL 8.x（其他较新版本一般也可以）

## 3. 第一次运行前

### 第一步：确认 MySQL 已启动

可以在 Windows 服务中启动 MySQL，或者使用 MySQL Workbench / 其他 MySQL 管理工具。

### 第二步：创建数据库

打开 MySQL，执行：

```sql
CREATE DATABASE IF NOT EXISTS ai_study_manager
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

也可以直接运行项目中的 `init_database.sql`。

### 第三步：修改数据库密码

打开 `database.py`：

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "ai_study_manager",
    "charset": "utf8mb4",
}
```

把：

```python
"password": "123456"
```

改成你自己 MySQL 的 root 密码。

## 4. 安装依赖

在 PyCharm Terminal 中执行：

```bash
pip install -r requirements.txt
```

也可以：

```bash
python -m pip install mysql-connector-python
```

## 5. 运行

在 PyCharm 中右键 `main.py`：

```text
Run 'main'
```

程序菜单：

```text
1. 添加学习任务
2. 查看全部任务
3. 搜索任务
4. 完成任务
5. 删除任务
0. 退出
```

## 6. 本项目练习到的知识

- Python 函数
- 类与对象
- MySQL 连接
- SQL INSERT
- SQL SELECT
- SQL UPDATE
- SQL DELETE
- LIKE 模糊查询
- 主键、自增
- 数据库持久化
- Python 项目模块拆分

## 7. 和后面的 Agent 怎么连接？

后面学习 Agent 后，可以把这个项目继续升级：

```text
用户
 ↓
AI Agent
 ↓
判断用户意图
 ↓
调用任务管理工具
 ↓
MySQL
 ↓
返回结果
```

例如用户说：

> 帮我添加一个明天学习高数极限 2 小时的任务

Agent 可以自动调用：

```text
add_task(...)
```

再例如：

> 我今天有哪些数学任务？

Agent 调用：

```text
search_tasks("数学")
```

这就是 Tool Calling + 数据库 + Agent 的结合。
