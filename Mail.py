import smtplib

TO = 'm.pivarnikova1@gmail.com'
SUBJECT = 'TEST MAIL'
TEXT = 'Here is a message from python.'

# Gmail Sign In
gmail_sender = ''
gmail_passwd = ''

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()

server.login(gmail_sender, gmail_passwd)

BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])


server.sendmail(gmail_sender, [TO], BODY)
print ('email sent')

server.quit()