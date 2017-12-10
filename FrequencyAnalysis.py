import pymysql
import publicsuffixlist

db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()
#Otvori subor s frekvenciami a ulozi do premennej
freq = eval(open("/Users/martinapivarnikova/Documents/freq.txt").read())

with open('/Users/martinapivarnikova/Documents/anonymized_queries') as f:
    for line in f:

        split_dq = line.split(" ")
        dn = split_dq[8]
        #parsne to na 1 level domeny a porovna s Whitelistom
        domain_name = publicsuffixlist.PublicSuffixList().subdomain(dn, 0)
        cursor.execute("SELECT 'true' FROM Whitelist WHERE domain_name LIKE %s", (domain_name,))
        result = cursor.fetchone()
        #ak to nenaslo vo whiteliste, pocita sa weight pomocou frekvencii
        if not result:
            sum = 0
            #spocita sa suma frekvencii pismen v danom dn
            for letter in dn:
                sum += freq[letter.lower()]
            #spocita sa weight a ak je mensia ako nejaka hodnota, vypise sa dn a weight
            w = (sum / len(dn)) * 1000
            if (w < 49):
                print(dn)
                print(w)

