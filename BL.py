from pybloom import BloomFilter
import pymysql
import os

f = BloomFilter(capacity=12000,error_rate=0.00001)
db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()
cursor.execute("SELECT domain_name,type FROM Blacklist")
results = cursor.fetchall()


for r in results:
    f.add(r[0])

file = open('/Users/martinapivarnikova/Documents/anonymized_queries')
s = open('/Users/martinapivarnikova/Documents/blacklisteddomains.txt', 'w')
for line in file:
    split_dq = line.split(" ")
    dn = split_dq[8]
    if (dn in f):
        s.write(dn)
        s.write('\n')