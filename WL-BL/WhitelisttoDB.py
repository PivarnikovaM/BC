import csv
import pymysql


db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()
csv_data = csv.reader(open('/Users/martinapivarnikova/Documents/top-1m.csv'))
# next(csv_data)
for row in csv_data:
    # print (row[0])
    cursor.execute('INSERT INTO Whitelist(id,domain_name) VALUES(%s,%s)', row)

# cursor.execute('SELECT * FROM Whitelist')
# result = cursor.fetchall()
# print (result)
db.commit()
cursor.close()
print("Imported")
