from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv(verbose=True)
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def hello():
    API_KEY = os.getenv('API_KEY')
    return render_template('food.html', API_KEY = API_KEY)

@app.route('/admin')
def admin():
    return render_template('admin.html')


def store_to_db(name, address, category):
    conn = sqlite3.connect("address.db")
    c = conn.cursor()

    # 테이블이 없으면 생성
    c.execute('CREATE TABLE IF NOT EXISTS table_name (name TEXT, address TEXT, category TEXT)')
    
    # 데이터 삽입
    c.execute('INSERT INTO table_name VALUES (?, ?, ?)', (name, address, category))

    conn.commit()
    conn.close()

@app.route('/store', methods=['POST'])
def store():
    name = request.form['name']
    address = request.form['address']
    category = request.form['category']
    store_to_db(name, address, category)  # 저장 함수
    return '식당 정보가 저장 되었습니다. <br><a href="/admin">뒤로가기<a>'

def get_data_from_db():
    conn = sqlite3.connect('address.db')  # DB에 연결
    c = conn.cursor()

    # 모든 데이터 가져오기
    c.execute('SELECT * FROM table_name')
    data = c.fetchall()

    conn.close()

    return data

# def edit_db(name, new_name, new_address):
#     conn = sqlite3.connect('address.db')  # DB에 연결
#     c = conn.cursor()

#     # 데이터 수정
#     c.execute('UPDATE table_name SET name = ?, address = ? WHERE name = ?', (new_name, new_address, name))

#     conn.commit()  # 변경사항 저장
#     conn.close()

def edit_name_in_db(old_name, new_name):
    conn = sqlite3.connect('address.db')  # DB에 연결
    c = conn.cursor()

    # 상호명 수정
    c.execute('UPDATE table_name SET name = ? WHERE name = ?', (new_name, old_name))

    conn.commit()  # 변경사항 저장
    conn.close()

def edit_address_in_db(name, new_address):
    conn = sqlite3.connect('address.db')  # DB에 연결
    c = conn.cursor()

    # 주소 수정
    c.execute('UPDATE table_name SET address = ? WHERE name = ?', (new_address, name))

    conn.commit()  # 변경사항 저장
    conn.close()

def edit_category_in_db(name, new_category):
    conn = sqlite3.connect('address.db')  # DB에 연결
    c = conn.cursor()

    # 카테고리 수정
    c.execute('UPDATE table_name SET category = ? WHERE name = ?', (new_category, name))

    conn.commit()  # 변경사항 저장
    conn.close()

def delete_from_db(name):
    conn = sqlite3.connect('address.db')  # DB에 연결
    c = conn.cursor()

    # 데이터 삭제
    c.execute('DELETE FROM table_name WHERE name = ?', (name,))

    conn.commit()  # 변경사항 저장
    conn.close()


@app.route('/data')
def data_page():
    data = get_data_from_db()  # DB에서 데이터를 가져오는 함수
    return render_template('address.html', data=data)  # HTML 템플릿에 데이터 전달

# @app.route('/edit', methods=['POST'])
# def edit():
#     name = request.form['name']
#     new_name = request.form['new_name']
#     new_address = request.form['new_address']
#     edit_db(name, new_name ,new_address)  # 수정 함수
#     return 'Data updated.'

@app.route('/edit_name', methods=['POST'])
def edit_name():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    edit_name_in_db(old_name, new_name)  # 상호명 수정 함수
    return '상호명이 업데이트 되었습니다. <br><a href="/data">뒤로가기<a>'

@app.route('/edit_address', methods=['POST'])
def edit_address():
    name = request.form['name']
    new_address = request.form['new_address']
    edit_address_in_db(name, new_address)  # 주소 수정 함수
    return '주소가 업데이트 되었습니다.<br><a href="/data">뒤로가기<a>'

@app.route('/edit_category', methods=['POST'])
def edit_category():
    name = request.form['name']
    new_category = request.form['new_category']
    edit_category_in_db(name, new_category)  # 카테고리 수정 함수
    return '카테고리가 업데이트 되었습니다.<br><a href="/data">뒤로가기<a>'

@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    delete_from_db(name)  # 삭제 함수
    return '식당 정보가 삭제되었습니다.<br><a href="/data">뒤로가기<a>'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)