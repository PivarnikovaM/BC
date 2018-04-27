import threading
from datetime import timedelta
from datetime import datetime
from queue import *
import pymysql
import time

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

        cursor.execute('select distinct query_address from Data where rcode = "NXDOMAIN"')
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

    def nxdomain(self, results):
        s = open('/Users/martinapivarnikova/Downloads/nxdomainRes.txt', 'a')
        count = 0
        data = []
        i = 0
        for r in results:
            if (i < len(results) - 1):
                ip = r[2]
                pom = results[i + 1]
                ip2 = pom[2]
                t = r[1].replace("\n", "")
                time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')

                t2 = pom[1].replace("\n", "")
                time2 = datetime.strptime(t2, '%Y-%m-%d %H:%M:%S.%f')

                if ip == ip2 and time2 < time + timedelta(minutes=10):
                    data.append(results[i])
                    count += 1
                else:

                    if (count > 10):
                        s.write(str(data))
                        print(data)
                        s.write('------\n')

                        # print('\n')
                    count = 0
                    data = []

                i += 1

    def run(self):
        db = pymysql.connect(host='localhost',
                             user='root', passwd='root', db="Bakalarka")
        cursor = db.cursor()

        while True:
            if not q.empty():
                item = q.get()
                cursor.execute("SELECT * FROM Data WHERE rcode = 'NXDOMAIN' and query_address like %s",(item,))
                results = cursor.fetchall()

                self.nxdomain(results)
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
