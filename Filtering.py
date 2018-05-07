import pymysql
from pybloom import BloomFilter
import os

# filter an extended DNSTAP file
def filter_ext():
    str = ''
    cnt = 0
    test = False
    with open('/Users/martinapivarnikova/Downloads/dns-ext2.txt', 'r') as file:
        s = open('/Users/martinapivarnikova/Downloads/filteredDNS.txt', 'w')
        for line in file:
            cnt += 1
            str = str + line
            if cnt == 5:
                if 'CLIENT' in line:
                    test = True
            if '---' in line:
                if test:
                    s.write(str)
                str = ''
                cnt = 0
                test = False


f = BloomFilter(capacity=5000000, error_rate=0.00001)
db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()
cursor.execute("SELECT domain_name FROM Whitelist")

res = cursor.fetchall()
for r in res:
    f.add(r[0])

cursor.close()
print("Done")


# Whitelist comparision using Bloom filter
def check_whitelist(dn):
    domain_name = dn.split('.')
    pp = None
    for i in range(len(domain_name)):
        pp = ".".join((domain_name[-(i + 1)], pp) if pp is not None else (domain_name[-(i + 1)],))
        if pp in f:
            return True

    return False

fblack = BloomFilter(capacity=12000, error_rate=0.00001)
cursor_bl = db.cursor()
cursor_bl.execute("SELECT domain_name,type FROM Blacklist")
results_bl = cursor_bl.fetchall()
cursor_bl.close()

# Blacklist comparision using Bloom filter
def check_blacklist(dn):

    for r in results_bl:
        fblack.add(r[0])

    if dn in fblack:
        return True
    else:
        return False


# parsing DNSTAP data and saving into db (WL/BL filtered)
def save_db():
    db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
    cursor = db.cursor()

    cnt = 0
    ans = False
    str = ''
    ip = ''
    batch = 0
    with os.popen('sed -n "6956670,11323532p" /Users/martinapivarnikova/Downloads/filteredDNS.txt', 'r') as file:
        for line in file:
            cnt += 1
            split_dq = line.split(" ")
            if cnt == 5:
                type = split_dq[3]
            if cnt == 6:
                time_of = '' + split_dq[4] + ' ' + split_dq[5]
            if cnt == 9:
                query_address = split_dq[3]
            if cnt == 14:
                rcode = split_dq[9]
                rcode = rcode.replace(",", "")
                id_q = split_dq[11]
            if cnt == 18:
                domain = split_dq[4]
                domain_name = domain.split('\t')
                dn = domain_name[0]
                dn = dn.replace(";", "")
                dn = dn[:-1]
            if cnt == 21:
                if type == 'CLIENT_RESPONSE\n' and rcode == 'NOERROR':
                    ans = True
            if ans is True:
                if line != '\n':
                    str = str + line
                else:
                    ans = False
                    answers = str.split(' ')
                    a = answers[len(answers) - 1]
                    ipa = a.split('\t')
                    ip = ipa[len(ipa) - 1]
            if '---' in line:
                cnt = 0
                if check_blacklist(dn):
                    cursor.execute('SELECT type FROM Blacklist WHERE domain_name = %s', (dn,))
                    type = cursor.fetchone()[0]
                    cursor.execute('INSERT INTO BLResults(type_rq,time_of,query_address,rcode,id_q,domain_name,ip,type) '
                        'VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                        (type, time_of, query_address, rcode, id_q, dn, ip,type))
                    db.commit()
                if dn.count('.') > 1 and not check_whitelist(dn):
                    batch += 1
                    cursor.execute(
                        'INSERT INTO Data3(type_rq,time_of,query_address,rcode,id_q,domain_name,ip) '
                        'VALUES(%s,%s,%s,%s,%s,%s,%s)',
                        (type, time_of, query_address, rcode, id_q, dn, ip))
                    if batch % 1000 == 0:
                        db.commit()
                ip = None

    db.commit()
    cursor.close()
    db.close()

save_db()
