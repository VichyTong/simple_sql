from flask import Flask, jsonify, request
import psycopg2
from pgvector.psycopg2 import register_vector

app = Flask(__name__)

# 设置 PostgreSQL 数据库连接参数
DATABASE = {
    'database': 'postgres',
    'host': '47.93.47.3',
    'user': 'postgres',
    'password': '',
    'port': '5433'
}


# API 接口，查询离指定经纬度最近的 N 个结果
@app.route('/api/get_nearest_N', methods=['GET'])
def get_nearest_N():
    # 获取请求参数
    vector = request.args.get('vector')
    n = request.args.get('n')

    # 执行 SQL 查询
    conn = psycopg2.connect(**DATABASE)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(cur)
    cur.execute(f"SELECT * FROM law ORDER BY embedding <-> %s LIMIT %s", (vector, n))
    results = cur.fetchall()

    cur.close()
    conn.close()

    # 将结果转换为 JSON 格式并返回
    return jsonify(results)


if __name__ == '__main__':
    app.run()
