import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymysql

fromaddr = "5183328@upjs.sk"
toaddr = "m.pivarnikova1@gmail.com"

db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()


msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Mail"

body = '' + "Blacklist: \n"
cursor.execute("SELECT * FROM BLResults")
res = cursor.fetchall()

for s in res:
    for x in s:
        body = body + "\t\t" + str(x)
body = body + "\n"

body = body + "Analýza doménových mien: \n"
cursor.execute("SELECT * FROM DNResults")
res = cursor.fetchall()

for s in res:
    for x in s:
        body = body + "\t\t" + str(x)
body = body + "\n"

body = body + "Analýza DNS odpovedí: \n"
cursor.execute("SELECT time_of,query_address,domain_name FROM NXDomainResults")
res = cursor.fetchall()

for s in res:
    for x in s:
        body = body + "\t\t" + str(x)
body = body + "\n"

msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.office365.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

server.login(fromaddr, "***")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
