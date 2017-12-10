import pymysql
import requests


def removefromBL(r):
    db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
    cursor = db.cursor()
    for line in r.iter_lines():
        line = line.decode('utf-8')
        #print(line)
        split_dq = line.split("\t")
        print(split_dq[2])
        # try:
        cursor.execute('DELETE FROM Blacklist where domain_name LIKE(%s)', (split_dq[2],))
        # except pymysql.err.IntegrityError: print('ERROR: ' + split_dq[2])
        # # print(split_dq[5])

    db.commit()
    cursor.close()
    print("Deleted")


for j in range(1,12):
    for k in range(1,31):
        if(j < 10 & k < 10) :
            r = requests.get('http://mirror1.malwaredomains.com/files/removed-domains-' + str(2017) + '0' + str(j) + '0' + str(k) + '.txt')
            if (r.status_code == 200) : removefromBL(r)
            # print(r.status_code)
        if(j<10 & k >=10) :
            r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2017) + '0' + str(j) + str(k) + '.txt')
            if (r.status_code == 200): removefromBL(r)
            # print(r.status_code)
        if(j>=10 & k<10) :
            r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2017) + str(j) + '0' +str(k) + '.txt')
            if (r.status_code == 200): removefromBL(r)
        if(j>=10 & k >=10) :
            r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2017) + str(j) + str(k) + '.txt')
            if (r.status_code == 200): removefromBL(r)


# r = requests.get('http://mirror1.malwaredomains.com/files/' + str(2017) + '0' + str(1) + '0' + str(3) + '.txt', stream=True)
# importtoBL(r)



