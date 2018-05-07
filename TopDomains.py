import json
import pymysql
import operator

db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()

cursor.execute("SELECT domain_name FROM Data")
result = cursor.fetchall()


#Vypocita pocet vyskytov pismen
hits={}
pocet_vsetkych = 0;

for line in result:
    if line[0] in hits: hits[line[0]] += 1
    else: hits[line[0]] = 1



sorted_x = sorted(hits.items(), key=operator.itemgetter(1))

with open('/Users/martinapivarnikova/Documents/freq2.txt', 'w') as file:
    file.write(str(sorted_x))
#Vypocita frekvenciu vyskytov
# freq={}

# for key in hits:
#     if key not in freq : freq[key] = hits[key]/pocet_vsetkych
#
#
# print(freq)
#
# with open('/Users/martinapivarnikova/Documents/freq2.txt', 'w') as file:
#      file.write(json.dumps(freq))
