import pymysql
import publicsuffixlist
from pybloom import BloomFilter

# def parse_subdomain(domain_name):


db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()

f = BloomFilter(capacity=1000000,error_rate=0.001)
db = pymysql.connect(host='localhost',
                         user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()
cursor.execute("SELECT domain_name FROM Whitelist")
results = cursor.fetchall()

for r in results:
    f.add(r[0])

#file = os.popen('sed -n "40300,2701400p" /Users/martinapivarnikova/Documents/anonymized_queries')
file = open('/Users/martinapivarnikova/Documents/anonymized_queries')
s = open('/Users/martinapivarnikova/Documents/WLfiltered.txt', 'w')
for line in file:
        split_dq = line.split(" ")
        dn = split_dq[8]
        domain_name = publicsuffixlist.PublicSuffixList().subdomain(dn, 0)
        if (domain_name not in f):
            s.write(line)


cursor.close()
print("Done")
