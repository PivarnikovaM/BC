import pymysql
from datetime import timedelta
from datetime import datetime

db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()

cursor.execute("select * from Data where rcode = 'NXDOMAIN' order by query_address desc,time_of asc")
results = cursor.fetchall()
s = open('/Users/martinapivarnikova/Downloads/nxdomainRes.txt', 'w')
count = 0
data = []
i = 0
for r in results:
    if (i<len(results)-1):
        ip = r[3]
        pom = results[i+1]
        ip2 = pom[3]
        t = r[2].replace("\n","")
        time = datetime.strptime(t,'%Y-%m-%d %H:%M:%S.%f')

        t2 = pom[2].replace("\n","")
        time2 = datetime.strptime(t2,'%Y-%m-%d %H:%M:%S.%f')

        if ip == ip2 and time2 < time + timedelta(minutes = 10):
            data.append(results[i])
            count += 1
        else:

            if(count > 10):
                s.write(str(data))
                s.write('------\n')

                # print('\n')
            count = 0
            data = []

        i +=1