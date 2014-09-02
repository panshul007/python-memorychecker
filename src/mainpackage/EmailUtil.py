'''
Created on Sep 18, 2013

@author: panshul
'''
import smtplib

from email.mime.text import MIMEText


username="user@domain.com"
password="guessme"


def prepareMessage(dsf,recipients,machine):
    message = format("Hello,\n %r has become unstable due to dangerously low free memory (under 20%). Please restart the server urgently.\n The current stats are:\nMaximum Heap Space: %r MB Current Heap Space: %r MB Used Memory: %r MB  Free Memory: %r MB" %(machine,dsf[0],dsf[1],dsf[2],dsf[3]))
    msg = MIMEText(message)
    msg['Subject'] = format("ALERT: %r is unstable, free memory low" %(machine))
    msg['From'] = username
    msg['To'] = ','.join(recipients)
    return msg
 

def prepareConnectionMessage(recipients, machine):
    message = format("Hello,\n %r is unreachable or has become unresponsive or has encountered an error due to unknown reasons. Please take necessary actions to resolve this issue." %(machine))
    msg = MIMEText(message)
    msg['Subject'] = format("ALERT: %r is unreachable or has an error" %(machine))
    msg['From'] = username
    msg['To'] = ','.join(recipients)
    return msg


def sendServerAlertMail(dsf,recipients,machine,alertType):
    msg = ""
    if alertType=='memory':
        msg = prepareMessage(dsf,recipients,machine)
    elif alertType=='connection':
        msg = prepareConnectionMessage(recipients,machine)
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(username,password)
    s.sendmail(username, recipients, msg.as_string())
    s.quit()    

