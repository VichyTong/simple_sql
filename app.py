import json
from json import JSONEncoder
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from pgvector.psycopg2 import register_vector
import openai
import numpy as np

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API_KEY')


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def embedding(words):
    response = openai.Embedding.create(
        input=words,
        engine="text-embedding-ada-002"
    )
    vector = np.array(response.data[0].embedding)
    return vector


# API 接口，查询离指定经纬度最近的 N 个结果
@app.route('/api/get_nearest_N', methods=['POST'])
def get_nearest_N():
    # 获取请求参数
    words = request.json.get('words')
    n = request.json.get('n')

    vector = embedding(words)

    # 执行 SQL 查询
    conn = psycopg2.connect(
        database='postgres',
        host='47.93.47.3',
        user='postgres',
        password='',
        port='5433'
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(cur)
    cur.execute(f"SELECT * FROM law ORDER BY embedding <-> %s LIMIT %s", (vector, n))
    results = cur.fetchall()

    cur.close()
    conn.close()

    # 将结果转换为 JSON 格式并返回
    return json.dumps(results, cls=NumpyArrayEncoder)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2409)
