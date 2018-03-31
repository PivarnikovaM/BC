import math
from collections import Counter

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


with open('/Users/martinapivarnikova/Downloads/zeus_dga_domains.txt') as f:
    for line in f:
        print('Domain: ',line)
        print('Entropy: ',entropy(line),'\n','Frequency: ',frequency(line),'\n','Numbers: ',numbers(line),'\n','Dashes: ',dashes(line))
        print('\n')
        #print(line)