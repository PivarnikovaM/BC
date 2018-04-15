import pymysql
import publicsuffixlist
import os
db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()
#poc = 0;
f = os.popen('sed -n "40300,2701400p" /Users/martinapivarnikova/Documents/anonymized_queries')
for line in f:
        #poc = poc+1
        split_dq = line.split(" ")
        dn = split_dq[8]
        #hash = split_dq[5]
        #print(poc)
        # domain_name = publicsuffixlist.PublicSuffixList().subdomain(dn, 0)
        cursor.execute("SELECT 'true' FROM Blacklist WHERE domain_name LIKE %s", (dn,))
        result = cursor.fetchone()
        if result:

           print (dn)


        #else:
             #print('true')s
    #break #v cykle prerusi vykonavanie




print(result)
cursor.close()
print("Done")
