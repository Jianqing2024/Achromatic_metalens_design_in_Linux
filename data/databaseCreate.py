import sqlite3
import os

# 获取当前脚本所在目录
project_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(project_dir, "structures.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建表（如果不存在）
cursor.execute("""
CREATE TABLE IF NOT EXISTS structures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baseValue INTEGER NOT NULL,
    P REAL NOT NULL,
    H REAL NOT NULL,
    L REAL NOT NULL,
    W REAL NOT NULL,
    R REAL NOT NULL,
    angleIn532 REAL NOT NULL,
    transIn532 REAL NOT NULL,
    angleIn800 REAL NOT NULL,
    transIn800 REAL NOT NULL
)
""")

cursor.execute("DELETE FROM structures;")

# 提交更改并关闭连接
conn.commit()
conn.close()
print(f"数据库已创建在：{db_path}")
