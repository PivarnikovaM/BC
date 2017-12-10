import pymysql
import publicsuffixlist

db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()
#poc = 0;
with open('/Users/martinapivarnikova/Documents/anonymized_queries') as f:
    for line in f:
        #poc = poc+1
        split_dq = line.split(" ")
        dn = split_dq[8]
        #print(poc)
        domain_name = publicsuffixlist.PublicSuffixList().subdomain(dn, 0)
        cursor.execute("SELECT 'true' FROM Whitelist WHERE domain_name LIKE %s", (domain_name,))
        result = cursor.fetchone()
        if not result:
            print (domain_name)


        #else:
             #print('true')
    #break #v cykle prerusi vykonavanie




print(result)
cursor.close()
print("Done")
