from flask import Flask, render_template, request
import json
from flask_mysqldb import MySQL
import yaml
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from numpy import genfromtxt
import csv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/flask_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Banks(db.Model):
    __tablename__="banks"
    bank_name=db.Column(db.String(49))
    bank_id=db.Column(db.BigInteger, nullable=False, primary_key=True)
    branch = db.relationship('Branches')
    def __repr__(self) -> str:
        return "<{}:{}>"


class Branches(db.Model):
    __tablename__="branches"
    ifsc= db.Column(db.String(11), nullable= False,primary_key=True)
    bank_id=db.Column(db.BigInteger, db.ForeignKey('banks.bank_id'))
    branch = db.Column(db.String(74), unique=False)
    address = db.Column(db.String(195), unique=False)
    city = db.Column(db.String(50), unique=False)
    district = db.Column(db.String(50), unique=False)
    state = db.Column(db.String(26), unique=False)

# if not (db.engine.has_table('banks') and db.engine.has_table('branches')):
#         db.create_all()
        


# class bank_branches(mysql.Model):

# df = pd.read_csv('bank_branches.csv', delimiter=',')

col_list = ["bank_name", "bank_id"]
df = pd.read_csv('bank_branches.csv', delimiter=",", usecols=col_list).unique()
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/flask_app_db')
df.to_sql("banks", engine)
#specified columns we want to import and covert it to list
# columns=df.columns
# df_data=df[columns]
# # records=df_data.values.tolist()
# print(df)
# for row in records:
#     db.session.add(Banks(bank_name=row[7],bank_id=row[1]))
#     db.session.commit()
    




# abc = Banks(bank_name=temp[7],  bank_id=temp[1])
# db.session.add(abc)
# db.session.commit()
# Given a bank branch IFSC code, get branch details
# @app.route('/ifsc/<ifsc_code>')
# def ifsc_get(ifsc_code):
# 	conn = mysql.connection.cursor()
# 	cur = conn.cursor()
# 	cur.execute("SELECT * FROM bank_branches where ifsc=?;", (ifsc_code,) )
# 	branch = cur.fetchall()
# 	conn.commit()
# 	return json.dumps(branch)

# #Given a bank name and city, gets details of all branches of the bank in the city
# @app.route('/bank_name/<bank_name>/city/<city>')
# def branch_city_get(bank_name,city):
# 	conn = mysql.connection.cursor()
# 	cur = conn.cursor()
# 	cur.execute("SELECT * FROM bank_branches where bank_name=? and city=?;", (bank_name,city,) )
# 	branches = cur.fetchall()
# 	conn.commit()
# 	return json.dumps(branches)

# if __name__=='__main__':
# 	app.run(debug=True)





