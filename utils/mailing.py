import os
import smtplib
from config import config
# os.environ['DEBUG'] = '1'

def send_mail(mail_sub='', mail_body='', sender='', receivers=list()):

    # print mail_sub
    # print mail_body
    # print sender
    # print receivers

    # we need the receivers.
    print 222222222222222222222222222222222
    if not receivers:
        return 'No receivers found, aborting mailing process.'
    # if no senders specified then take the local user as the sender.
    if not sender:
        user_name = os.environ['USERNAME']
        sender = '%s@mail.pcgi.com' % user_name
    debug = 0
    debug = int(os.getenv('DEBUG', 0))
    print debug
    if not mail_sub or not mail_body:
        return 'No Subject or the mail body provided, aborting mailing process.'

    message = 'From: %s\nTo: %s\nSubject: %s\n%s.' % (sender, receivers[0], mail_sub, mail_body)

    # if debug:
    #     print 'Mailing : \n {} \n\n From : {} \n To : {}'.format(message, sender, receivers)
    #     return True

    try:
        print 'sender', sender
        print 'receivers', receivers
        print 'message', message
        smtp_obj = smtplib.SMTP(config.mailHost)
        smtp_obj.sendmail(sender, receivers, message)
        smtp_obj.quit()
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"


if __name__ == '__main__':
    # print os.environ['DEBUG']
    # pass
    # print send_mail(mail_sub='test', mail_body='Hi', receivers=['durgesh.n@mail.pcgi.com'], sender='durgesh.n@mail.pcgi.com')
    print send_mail(mail_sub='test', mail_body='Hi', receivers=['durgesh.n@pcgi.com'], sender='')
