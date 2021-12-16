from flask import Flask
from flask_mysqldb import MySQL 
import pandas as pd
df = pd.read_csv('bank_branches.csv', delimiter=',')

#specified columns we want to import and covert it to list
columns=df.columns
df_data=df[columns]
records=df_data.values.tolist()
print(records[1])

#creating MySQL server connection

# app=Flask(__name__)

# app.config['MySQL_HOST']='127.0.0.1'
# app.config['MySQL_USER']='root'
# app.config['MySQL_PASSWORD']='root'
# app.config['MySQL_DB']='flaskapp'

# mysql=MySQL(app)
# print(mysql)
# print(mysql.connection)


# # @app.route('/')
# # def index():
# #     cur=mysql.connection.cursor()
# # if __name__ == '__main__':
# #     app.run()

# # print(mysql)
# # query='INSERT INTO bank_branches(ifsc,bank_id,branch,address,city,district,state,bank_name)' 'values(%s,%s,%s,%s,%s,%s,%s,%s)'
# # conn = mysql.cursor()
# # # conn.executemany(query,records)
# # # mysql.connection.commit()
# # # conn.close()

# # db = mysql.connect('localhost', 'root', 'password', 'db')
# # cursor = db.cursor()