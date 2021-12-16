from flask import Flask, render_template, request
import json
from flask_mysqldb import MySQL
import yaml

app=Flask(__name__)

db=yaml.safe_load(open('db.yaml'))

# app.config['MySQL_HOST']='127.0.0.1'
# app.config['MySQL_USER']='root'
# app.config['MySQL_PASSWORD']='root'
# app.config['MySQL_DB']='flaskapp'
app.config['MySQL_HOST']=db['mysqlHost']
app.config['MySQL_USER']=db['mysqlUser']
app.config['MySQL_PASSWORD']=db['mysqlPassword']
app.config['MySQL_DB']=db['mysqlDb']

mysql=MySQL(app)


#Given a bank branch IFSC code, get branch details
@app.route('/ifsc/<ifsc_code>')
def ifsc_get(ifsc_code):
	conn = mysql.connection.cursor()
	cur = conn.cursor()
	cur.execute("SELECT * FROM bank_branches where ifsc=?;", (ifsc_code,) )
	branch = cur.fetchall()
	conn.commit()
	return json.dumps(branch)

#Given a bank name and city, gets details of all branches of the bank in the city
@app.route('/bank_name/<bank_name>/city/<city>')
def branch_city_get(bank_name,city):
	conn = mysql.connection.cursor()
	cur = conn.cursor()
	cur.execute("SELECT * FROM bank_branches where bank_name=? and city=?;", (bank_name,city,) )
	branches = cur.fetchall()
	conn.commit()
	return json.dumps(branches)

if __name__=='__main__':
	app.run(debug=True)

