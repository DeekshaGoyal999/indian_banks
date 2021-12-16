
from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import csv
import yaml

app=Flask(__name__)

app.config['MySQL_HOST']='127.0.0.1'
app.config['MySQL_USER']='root'
app.config['MySQL_PASSWORD']='root'
app.config['MySQL_DB']='flaskapp'

mysql=MySQL(app)

with open('bank_branches.csv',encoding="utf8") as csv_file:
    csvfile=csv.reader(csv_file, delimiter=',')
    all_value=[]
    for row in csvfile:
        value=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        all_value.append(value)

query='insert into bank_branches(ifsc,bank_id,branch,address,city,district,state,bank_name)' 'values(%s,%s,%s,%s,%s,%s,%s,%s)',row
@app.route('/')
def hello():
    conn = mysql.connection.cursor()
    conn.executemany(query,all_value)
    mysql.connection.commit()
    conn.close()

if __name__ == '__main__':
    app.run()
