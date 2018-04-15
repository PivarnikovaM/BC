import pymysql
import requests


def importtoBL(r):
    db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
    cursor = db.cursor()
    for line in r.iter_lines():
        line = line.decode('utf-8')
        #print(line)
        split_dq = line.split("\t")
        #print(split_dq[2])
        try:
            cursor.execute('INSERT INTO Blacklist(domain_name,type) VALUES(%s,%s)', (split_dq[2],split_dq[3]))
        except pymysql.err.IntegrityError: print('ERROR: ' + split_dq[2])
        # print(split_dq[5])

    db.commit()
    cursor.close()
    print("Imported")



# with open('/Users/martinapivarnikova/Documents/immortal_domains.txt') as f:
#     for line in f:
#         cursor.execute('INSERT INTO Blacklist(domain_name) VALUES (%s)', (line,))


# for i in range(2016,2017):
for j in range(1,12):
    for k in range(1,31):
        if(j < 10 & k < 10) :
            r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2018) + '0' + str(j) + '0' + str(k) + '.txt')
            if (r.status_code == 200) : importtoBL(r)
            # print(r.status_code)
        if(j<10 & k >=10) :
            r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2018) + '0' + str(j) + str(k) + '.txt')
            if (r.status_code == 200): importtoBL(r)
            # print(r.status_code)
        if(j>=10 & k<10) :
            r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2018) + str(j) + '0' +str(k) + '.txt')
            if (r.status_code == 200): importtoBL(r)
        if(j>=10 & k >=10) :
            r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2018) + str(j) + str(k) + '.txt')
            if (r.status_code == 200): importtoBL(r)


# r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2017) + '0' + str(1) + '0' + str(3) + '.txt', stream=True)
# importtoBL(r)



