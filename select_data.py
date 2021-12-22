import mysql.connector

connection = mysql.connector.connect(host='localhost',
                                     port='3306',
                                     user='root',
                                     password='0000',
                                     database='test')

cursor = connection.cursor()


cursor.execute('SELECT * FROM `test`;')

records = cursor.fetchall()
for r in records:
    print(r)

cursor.close()
connection.close()
