from flask import Flask, render_template, request
import json
from flask_mysqldb import MySQL
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app=Flask(__name__)

#configuring MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_app_db'
 
mysql = MySQL(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/flask_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Populating the csv data in the mysql db
def populate_bank_data():
	col_list = ["ifsc","bank_id","branch","address","city","district","state","bank_name"]
	df = pd.read_csv('bank_branches.csv', delimiter=",", usecols=col_list)
	engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/flask_app_db')
	df.to_sql("banks_branches", engine)


#Given a bank branch IFSC code, get branch details
@app.route('/ifsc/<string:ifsc_code>')
def ifsc_get(ifsc_code):
    limit = request.args.get('limit', default = 100, type = int)
    offset = request.args.get('offset', default = 0, type = int)
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM banks_branches where ifsc=%(ifsc)s LIMIT %(limit)s OFFSET %(offset)s;", { 'ifsc': ifsc_code, 'limit': limit, 'offset': offset })
    branch_details = cur.fetchall()
    conn.commit()
    return json.dumps(branch_details)

# Given bank name and city , get bank branches
@app.route('/bank_name/<string:bank_name>/city/<string:city>')
def branch_city_get(bank_name,city):
    limit = request.args.get('limit', default = 100, type = int)
    offset = request.args.get('offset', default = 0, type = int)
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM banks_branches where bank_name=%(name)s and city=%(city)s LIMIT %(limit)s OFFSET %(offset)s;", {'name': bank_name, 'city': city, 'limit':limit,'offset':offset})
    branches = cur.fetchall()
    conn.commit()
    return json.dumps(branches)

if __name__=='__main__':
    app.run(host='localhost', port=5000,debug=True)





