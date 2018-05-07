import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymysql


def nlist_to_html(list2):
    #bold header
    htable=u'<table border="1" bordercolor=000000 cellspacing="0" cellpadding="1" style="table-layout:fixed;vertical-align:bottom;font-size:10px;font-family:consolas,monaco,monospace;border-collapse:collapse;border:1px solid rgb(130,130,130)" >'

    list2d = list(list2)
    list2d[0] = [u'<b>' + str(i) + u'</b>' for i in list2d[0]]
    for r in list2d:
        newrow = u'<tr>'
        row = list(r)
        newrow += u'<td align="left" style="padding:1px 4px">'+str(row[0])+u'</td>'

        row.remove(row[0])
        newrow = newrow + ''.join([u'<td align="right" style="padding:1px 4px">' + str(x) + u'</td>' for x in row])
        newrow += '</tr>'
        htable+= newrow
    htable += '</table>'
    return htable


fromaddr = "5183328@upjs.sk"
toaddr = "m.pivarnikova1@gmail.com"

db = pymysql.connect(host='localhost',
                     user='root', passwd='root', db="Bakalarka")
cursor = db.cursor()



body = '<b> <font size = 5 face = monaco> Blacklist: </font> </b> <br>'

cursor.execute("SELECT * FROM BLResults")
res = cursor.fetchall()

res = (('type_rq','time_of','query_address','rcode','id_q','domain_name','type'),) + res
tab = nlist_to_html(res)
body = body + tab

body = body + "<b> <font size = 5 face = monaco> Analýza doménových mien: </font> </b> <br>"
cursor.execute("SELECT * FROM DNResults")
res = cursor.fetchall()

res = (('domain_name','entropy','frequency','numbers','dashes','ip'),) + res
tab = nlist_to_html(res)
body = body + tab

body = body + "<b> <font size = 5 face = monaco>  Analýza DNS odpovedí: </font>  </b> <br>"
cursor.execute("SELECT time_of,query_address,domain_name FROM NXDomainResults")
res = cursor.fetchall()

res = (("timestamp","ip","domain_name"),) + res
tab = nlist_to_html(res)
body = body + tab

msg = MIMEMultipart("alternative")
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Mail"

msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP('smtp.office365.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

server.login(fromaddr, "***")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
