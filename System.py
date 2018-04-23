import pymysql
from pybloom import BloomFilter
import publicsuffixlist

def filter_ext():
    str = ''
    cnt = 0
    test = False
    with open('/Users/martinapivarnikova/Downloads/dns-ext2.txt', 'r') as file:
        s = open('/Users/martinapivarnikova/Downloads/filteredDNS.txt', 'w')
        for line in file:
            cnt += 1
            str = str + line
            if cnt==5:
                if 'CLIENT' in line:
                    test = True
            if '---' in line:
                if test:
                    s.write(str)
                str = ''
                cnt = 0
                test = False

def check_whitelist(dn):
    f = BloomFilter(capacity=1000000, error_rate=0.001)
    db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
    cursor = db.cursor()
    cursor.execute("SELECT domain_name FROM Whitelist")
    results = cursor.fetchall()

    for r in results:
        f.add(r[0])

    cursor.close()

    domain_name = publicsuffixlist.PublicSuffixList().subdomain(dn, 0)
    if (domain_name not in f):
        return True
    else: return False

def check_blacklist(dn):
    f = BloomFilter(capacity=12000, error_rate=0.00001)
    db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
    cursor = db.cursor()
    cursor.execute("SELECT domain_name,type FROM Blacklist")
    results = cursor.fetchall()

    cursor.close()
    for r in results:
        f.add(r[0])

    if (dn in f): return True
    else: return False


def save_db():
    db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
    cursor = db.cursor()

    cnt = 0
    ans = False
    str = ''
    ip=''
    with open('/Users/martinapivarnikova/Downloads/filteredDNS.txt', 'r') as file:
        for line in file:
            cnt += 1
            split_dq = line.split(" ")
            if cnt==5:
                type = split_dq[3]
            if cnt==6:
                time_of = '' + split_dq[4] + ' ' + split_dq[5]
            if cnt == 9:
                query_address = split_dq[3]
            if cnt == 10:
                response_address = split_dq[3]
            if cnt == 14:
                rcode = split_dq[9]
                rcode = rcode.replace(",","")
                id_q = split_dq[11]
            if cnt == 18:
                domain = split_dq[4]
                domain_name = domain.split('\t')
                dn = domain_name[0]
                dn = dn.replace(";", "")
            if cnt == 21:
                if type == 'CLIENT_RESPONSE\n' and rcode == 'NOERROR':
                    ans = True
            if ans is True:
                if line != '\n':
                    str = str + line
                else:
                    ans = False
                    answers = str.split(' ')
                    a = answers[len(answers)-1]
                    ipa = a.split('\t')
                    ip = ipa[len(ipa)-1]
            if '---' in line:
                cnt = 0
                # if check_blacklist(dn): insert into db
                # domain name must contain at least two dots to be normal (cause DNS generates weird domains)
                if dn.count('.') > 1 and check_whitelist(dn):
                    cursor.execute('INSERT INTO Data(type_rq,time_of,query_address,response_address,rcode,id_q,domain_name,ip) '
                                   'VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                                   (type,time_of,query_address,response_address,rcode,id_q,dn,ip))
                    db.commit()
                response_address = None




# save_db()
