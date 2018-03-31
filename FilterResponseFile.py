
str = ''
cnt = 0
test = False
with open('/Users/martinapivarnikova/Downloads/dns-ext2.txt', 'r') as file:
    s = open('/Users/martinapivarnikova/Downloads/filteredDNS.txt', 'w')
    for line in file:
        cnt += 1
        str = str + line
        if cnt==5:
            if 'CLIENT' in line:
                test = True
        if '---' in line:
            if test:
                s.write(str)
            str = ''
            cnt = 0
            test = False


