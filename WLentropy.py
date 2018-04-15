import pymysql
import math
from collections import Counter
import numpy

def entropy(s):

    if s is not None:
        p, lns = Counter(s), float(len(s))
        return -sum(count/lns * math.log(count/lns, 2) for count in p.values())
    else: return None

entropyr = []
db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()

cursor.execute("SELECT domain_name FROM Whitelist")
results = cursor.fetchall()


for r in results:
    entropyr.append(entropy(r[0]))

print(numpy.mean(entropyr))
