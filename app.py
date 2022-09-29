#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from flask import flash, request
import pymysql

app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'user'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/', methods=['GET'])
def query_records():
    name = ""
    if request.args.get('name'):
        name = request.args.get('name')
        print(name)

    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        if name:
            for record in records:
                print(record)
                if record['name'] == name:
                    return jsonify(record)
            return jsonify({'error': 'data not found'})
        else:
            return jsonify(records)

@app.route('/', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    with open('data.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)

@app.route('/', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['name'] == record['name']:
            r['email'] = record['email']
        new_records.append(r)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)
    
@app.route('/', methods=['DELETE'])
def delte_record():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['name'] == record['name']:
                continue
            new_records.append(r)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)

@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		return not_found()
        
@app.route('/add', methods=['POST'])
def add_user():
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		conn = mysql.connect()
		cursor = conn.cursor()
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = _password
			# save edits
			sql = "INSERT INTO users(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		return not_found()
		
@app.route('/users/<int:id>')
def get_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE id=%s", id)
		row = cursor.fetchone()
		if row is None:
			return not_found()
		else:
			resp = jsonify(row)
			resp.status_code = 200
			return resp
	except Exception as e:
		return not_found()
        
@app.route('/update', methods=['POST'])
def update_user():
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		conn = mysql.connect()
		cursor = conn.cursor()
		# validate the received values
		if _name and _email and _password and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = _password
			# save edits
			sql = "UPDATE users SET user_name=%s, user_email=%s, user_password=%s WHERE id=%s"
			data = (_name, _email, _hashed_password, _id,)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
			return not_found()
		
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE id=%s", id)
		row = cursor.fetchone()
		if row is None:
			return not_found()
		else:
			cursor.execute("DELETE FROM users WHERE user_id=%s", (id,))
			conn.commit()
			resp = jsonify('User deleted successfully!')
			resp.status_code = 200
			return resp
	except Exception as e:
		return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
		
if __name__ == "__main__":
	app.run(debug=True,port=5010)