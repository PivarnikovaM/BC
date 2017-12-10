import pymysql
import requests
import datetime


def updateBL(r,d):
    db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
    cursor = db.cursor()
    for line in r.iter_lines():
        line = line.decode('utf-8')
        split_dq = line.split("\t")
        try:
            cursor.execute('INSERT INTO Blacklist(domain_name,type) VALUES(%s,%s)', (split_dq[2], split_dq[3]))
        except pymysql.err.IntegrityError:
            print('ERROR: ' + split_dq[2])

    for line in d.iter_lines():
        line = line.decode('utf-8')
        # print(line)
        split_dq = line.split("\t")
        print(split_dq[2])
        # try:
        cursor.execute('DELETE FROM Blacklist where domain_name LIKE(%s)', (split_dq[2],))
        # except pymysql.err.IntegrityError: print('ERROR: ' + split_dq[2])
        # # print(split_dq[5])

    db.commit()
    cursor.close()
    print("Updated")


# with open('/Users/martinapivarnikova/Documents/immortal_domains.txt') as f:
#     for line in f:
#         cursor.execute('INSERT INTO Blacklist(domain_name) VALUES (%s)', (line,))

now = datetime.datetime.now()

if (now.month < 10 & now.day < 10):
    r = requests.get('http://mirror1.malwaredomains.com/files/' + str(now.year) + '0' + str(now.month) + '0' + str(now.day) + '.txt')
    d = requests.get('http://mirror1.malwaredomains.com/files/removed-domains-' + str(now.year) + '0' + str(now.month) + '0' + str(now.day) + '.txt')
    if (r.status_code == 200): updateBL(r,d)
    # print(r.status_code)
if (now.month < 10 & now.day >= 10):
    r = requests.get('http://mirror1.malwaredomains.com/files/' + str(now.year) + '0' + str(now.month) + str(now.day) + '.txt')
    d = requests.get('http://mirror1.malwaredomains.com/files/removed-domains-' + str(now.year) + '0' + str(now.month) + str(now.day) + '.txt')
    if (r.status_code == 200): updateBL(r,d)
    # print(r.status_code)
if (now.month >= 10 & now.day < 10):
    r = requests.get('http://mirror1.malwaredomains.com/files/' + str(now.year) + str(now.month) + '0' + str(now.day) + '.txt')
    d = requests.get('http://mirror1.malwaredomains.com/files/removed-domains-' + str(now.year) + str(now.month) + '0' + str(now.day) + '.txt')
    if (r.status_code == 200): updateBL(r,d)
if (now.month >= 10 & now.day >= 10):
    r = requests.get('http://mirror1.malwaredomains.com/files/' + str(now.year) + str(now.month) + str(now.day) + '.txt')
    d = requests.get('http://mirror1.malwaredomains.com/files/removed-domains-' + str(now.year) + str(now.month) + str(now.day) + '.txt')
    if (r.status_code == 200): updateBL(r,d)
