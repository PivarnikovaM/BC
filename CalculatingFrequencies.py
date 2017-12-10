import json
import pymysql

db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()

cursor.execute("SELECT domain_name FROM Whitelist")
result = cursor.fetchall()


#Vypocita pocet vyskytov pismen
hits={}
pocet_vsetkych = 0;

for line in result:
    for letter in (" | ".join(line)):
        pocet_vsetkych += 1
        if letter in hits: hits[letter] += 1
        else: hits[letter] = 1

print(pocet_vsetkych)

#Vypocita frekvenciu vyskytov
freq={}

for key in hits:
    if key not in freq : freq[key] = hits[key]/pocet_vsetkych


print(freq)

with open('/Users/martinapivarnikova/Documents/freq.txt', 'w') as file:
     file.write(json.dumps(freq))
