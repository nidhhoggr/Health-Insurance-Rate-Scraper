#!/usr/bin/python
import smtplib

class CrawlerNotifier:
 
    def __init__(self):
        self.to_notify = ('zmijevik@hotmail.com','persie.joseph@gmail.com')
        self.fromaddr = 'joseph@skysoftinc.com'


    def notify(self, notification_type, round=None):
        smtpserver = smtplib.SMTP('localhost')
        smtpserver.set_debuglevel(1)
        if notification_type == 'error':
            content = 'Error crawling round# ' + str(round)
        elif notification_type == 'success':
            content = 'successfully crawled every round'

        for toaddr in self.to_notify:
            header = 'To:' + toaddr + '\n' + 'From: ' + self.fromaddr + '\n' + 'Subject:healthtrustinsurance scraping ' + notification_type  + ' \n'        
            msg = header + '\n ' + content  + ' \n\n'
            smtpserver.sendmail(self.fromaddr, toaddr, msg)
