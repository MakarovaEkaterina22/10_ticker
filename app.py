from flask import Flask, jsonify, request
import psycopg2
import pandas as pd
from psycopg2 import sql
import datetime

app = Flask(__name__)

# Конфигурация БД
DATABASE_URL = "postgresql://postgres:password@db:5432/demand_db"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/api/demand/all', methods=['GET'])
def get_all_demands():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM products ORDER BY date DESC", conn)
    conn.close()
    return jsonify(df.to_dict('records'))

@app.route('/api/demand/avg-by-category', methods=['GET'])
def avg_demand_by_category():
    try:
        conn = get_db_connection()
        
        # Используем pandas для анализа с актуальными данными
        query = """
        SELECT category, AVG(demand) as avg_demand 
        FROM products 
        GROUP BY category
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': df.to_dict('records')
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/demand/add', methods=['POST'])
def add_demand_record():
    try:
        data = request.get_json()
        required_fields = ['category', 'product_name', 'demand', 'date']
        
        if not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Проверка формата даты
        try:
            datetime.datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO products (category, product_name, demand, date) VALUES (%s, %s, %s, %s)",
            (data['category'], data['product_name'], data['demand'], data['date'])
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Record added successfully',
            'data': data
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)