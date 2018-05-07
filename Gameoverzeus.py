import math
from collections import Counter
import numpy

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

#entropyr = []
with open('/Users/martinapivarnikova/Downloads/zeus_dga_domains.txt','r') as f:
    # s = open('/Users/martinapivarnikova/Documents/banjoriRes.txt','w')
    for line in f:
        ent = entropy(line)
        freq = frequency(line)
        num = numbers(line)
        d = dashes(line)
        if ent > 3.761 and freq < 46.994:
            # s.write(line)
            # s.write(str(ent) + " ")
            # s.write(str(freq))
            # s.write("\n")
            print(line,ent,freq,num,d)

#print(numpy.mean(entropyr))