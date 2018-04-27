import threading
from queue import *
import time
import pymysql
import math
from collections import Counter



BUF_SIZE = 10000
q = Queue(BUF_SIZE)


class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        db = pymysql.connect(host='localhost',
                             user='root', passwd='root', db="Bakalarka")
        cursor = db.cursor()

        cursor.execute('select distinct domain_name from Data2')
        while True:
            if not q.full():
                res = cursor.fetchone()
                if res is None:
                    cursor.close()
                    return
                q.put(res)

        cursor.close()
        return


class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        return

    def entropy(self,s):

        if s is not None:
            p, lns = Counter(s), float(len(s))
            return -sum(count / lns * math.log(count / lns, 2) for count in p.values())
        else:
            return None

    def frequency(self,dn):
        freq = eval(open("/Users/martinapivarnikova/Documents/freq.txt").read())

        sum = 0
        # spocita sa suma frekvencii pismen v danom dn
        for letter in dn:
            sum += freq[letter.lower()]
        # spocita sa weight
        w = (sum / len(dn)) * 1000

        return w;

    def numbers(self,dn):
        sum = 0;
        for letter in dn:
            if letter.isdigit():
                sum += 1;

        return sum;

    def dashes(self,dn):
        sum = 0;
        for letter in dn:
            if letter == '-':
                sum += 1;

        return sum;

    def analyse(self,dn):
        s = open('/Users/martinapivarnikova/Downloads/dnAnalysisRes.txt', 'a')

        ent = self.entropy(dn)
        freq = self.frequency(dn)
        num = self.numbers(dn)
        d = self.dashes(dn)
        string = ' '
        if ent > 3.761 and freq < 46.994:
            # string = string + dn + ' ' + str(ent) + ' ' + str(freq) + ' ' + str(num) + ' ' + str(d) + '\n'
            s.write(dn)
            s.write('\n')

    def run(self):
        db = pymysql.connect(host='localhost',
                             user='root', passwd='root', db="Bakalarka")
        cursor = db.cursor()

        while True:
            if not q.empty():
                item = q.get()
                self.analyse(item[0])
            else:  break
        cursor.close()
        return


if __name__ == '__main__':
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    time.sleep(2)
    for i in range(4):
        c = ConsumerThread(name='consumer')
        c.start()
