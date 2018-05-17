from pybloom import BloomFilter
import pymysql
import time

start_time = time.time()


f = BloomFilter(capacity=5000000, error_rate=0.00001)
db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()
cursor.execute("SELECT domain_name FROM Whitelist")

res = cursor.fetchall()
for r in res:
    f.add(r[0])

def check_whitelist(dn):
    domain_name = dn.split('.')
    pp = None
    for i in range(len(domain_name)):
        pp = ".".join((domain_name[-(i + 1)], pp) if pp is not None else (domain_name[-(i + 1)],))
        if pp in f:
            return True

    return False

file = open('/Users/martinapivarnikova/Documents/anonymized_queries')
s = open('/Users/martinapivarnikova/Documents/bloom.txt', 'w')

for line in file:
    split_dq = line.split(" ")
    dn = split_dq[8]
    if not check_whitelist(dn):
        s.write(dn)
        s.write('\n')


print("--- %s seconds ---" % (time.time() - start_time))