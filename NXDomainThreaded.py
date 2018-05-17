import threading
from datetime import timedelta
from datetime import datetime
from queue import *
import pymysql
import time

BUF_SIZE = 10000
q = Queue(BUF_SIZE)

class ProducerThread(threading.Thread):
    def __init__(self, target=None, name=None):
        super(ProducerThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        db = pymysql.connect(host='localhost',
                             user='root', passwd='root', db="Bakalarka")
        cursor = db.cursor()

        cursor.execute('SELECT DISTINCT query_address FROM Data3 WHERE rcode = "NXDOMAIN"')
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
    def __init__(self, target=None, name=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        self.db = pymysql.connect(host='localhost',
                             user='root', passwd='root', db="Bakalarka")
        self.cursor = self.db.cursor()
        return

    def nxdomain(self, results):
        # s = open('/Users/martinapivarnikova/Downloads/nxdomainRes.txt', 'a')
        count = 1
        data = []
        i = 0
        for r in results:
            if (i < len(results)-1):

                pom = results[i + 1]
                t = r[1].replace("\n", "")
                time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')

                t2 = pom[1].replace("\n", "")
                time2 = datetime.strptime(t2, '%Y-%m-%d %H:%M:%S.%f')

                if time2 < time + timedelta(minutes=10):
                    data.append(results[i])
                    count += 1
                else:
                    data.append(results[i])
                    if (count >= 10):
                        for d in data:
                            self.cursor.execute("INSERT INTO NXDomainResults(type_rq,time_of,query_address,rcode,id_q,domain_name) "
                                                 "VALUES (%s,%s,%s,%s,%s,%s)",(d[0],d[1],d[2],d[3],d[4],d[5]))
                            self.db.commit()
                        #s.write(str(data))
                        #print(data)
                        #s.write('------\n')

                    count = 0
                    data = []

                i += 1
            else:
                if (count >= 10):
                    for d in data:
                        self.cursor.execute(
                            "INSERT INTO NXDomainResults(type_rq,time_of,query_address,rcode,id_q,domain_name) "
                            "VALUES (%s,%s,%s,%s,%s,%s)", (d[0], d[1], d[2], d[3], d[4], d[5]))
                        self.db.commit()
                    #s.write(str(data))
                    # print(data)
                    # s.write('------\n')
                    return


    def run(self):
        db = pymysql.connect(host='localhost',
                             user='root', passwd='root', db="Bakalarka")
        cursor = db.cursor()

        while True:
            if not q.empty():
                item = q.get()
                cursor.execute("SELECT * FROM Data3 WHERE rcode = 'NXDOMAIN' and query_address like %s order by time_of asc",(item,))
                results = cursor.fetchall()

                self.nxdomain(results)
            else:  break
        cursor.close()
        return


if __name__ == '__main__':

    start_time = time.time()
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    time.sleep(2)
    for i in range(1):
        c = ConsumerThread(name='consumer')
        c.start()

    print("--- %s seconds ---" % (time.time() - start_time))