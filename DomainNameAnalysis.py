import pymysql
import publicsuffixlist
import math
from collections import Counter
import os


def entropy(s):

    if s is not None:
        p, lns = Counter(s), float(len(s))
        return -sum(count/lns * math.log(count/lns, 2) for count in p.values())
    else: return None

def frequency(dn):
    freq = eval(open("/Users/martinapivarnikova/Documents/freq.txt").read())

    sum = 0
    # spocita sa suma frekvencii pismen v danom dn
    for letter in dn:
        sum += freq[letter.lower()]
    # spocita sa weight
    w = (sum / len(dn)) * 1000

    return w;

def numbers(dn):
    sum = 0;
    for letter in dn:
        if letter.isdigit():
            sum += 1;

    return sum;

def dashes(dn):
    sum = 0;
    for letter in dn:
        if letter=='-':
            sum += 1;

    return sum;


db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()

file = os.popen('sed -n "40300,2701400p" /Users/martinapivarnikova/Documents/anonymized_queries')
#with open('/Users/martinapivarnikova/Documents/anonymized_queries') as f:
for line in file:
    split_dq = line.split(" ")
    dn = split_dq[8]
    # print(poc)
    subdomain = publicsuffixlist.PublicSuffixList().subdomain(dn, 0)

    cursor.execute('INSERT IGNORE INTO Results(domain_name,subdomain,entropy,frequency_an,numbers,dash) VALUES(%s,%s,%s,%s,%s,%s)',(dn,subdomain,entropy(subdomain),frequency(dn),numbers(dn),dashes(dn)))
    db.commit()