

with open('/Users/martinapivarnikova/Documents/WL_freq.txt') as f:
    s = open('/Users/martinapivarnikova/Documents/WLfreqGood','w')
    for line in f :
        if '.' in line and 'cloudfront' not in line and 'amazonaws' not in line and 'ip6.arpa' not in line and 'in-addr.arpa' not in line:
            s.write(line)
        else: next(f)