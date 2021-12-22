import mysql.connector


connection = mysql.connector.connect(host='localhost',
                                     port='3306',
                                     user='root',
                                     password='0000',
                                     database='test',)

cursor = connection.cursor()

# 新增
#cursor.execute("INSERT INTO `aaa` VALUES(2, '2', '2';")


# 修改
# cursor.execute('UPDATE `branch` SET `manager_id` = 206 WHERE `branch_id` = 4;')


# 刪除
# cursor.execute("DELETE FROM `branch` WHERE `branch_id` = 5;")
id = "20wrqrwqweqweqw001"
user = 'Bob'
age = 20
a = [20]
try:    
        for i in range(11):
            sql = 'INSERT INTO `test`.`toad` (`id`,`name`,`artist`) VALUES (%s,%s,%s);'
            cursor.execute(sql, (i,i,i))
            connection.commit()
except:
        print("錯誤")
        connection.rollback()
        #=====================================================================
        message = []
        cursor.close()
        connection.close()




