from utils.dbHelper import ConnectDB
from utils.switch import Switch, case
from utils.mailing import send_mail


class Assignments(object):
    def __init__(self, project, episode, dept):
        self.project = project
        self.episode = episode
        self.dept = dept
        # for mailing purpose.
        self.sender = 'shiva.admin'
        self.receiver = ''
        self.commentDict = dict()
        self.shotLists = list()

    def assignShot(self, artistShotDict):
        """
        This will assign the shots to the artists.
        :param artistShotDict: 
        :type artistShotDict: 
        :return: 
        :rtype: 
        """
        self.commentDict = dict()
        for key, val in artistShotDict.iteritems():
            self.shotLists = list()
            artistName = key
            self.receiver = '{}@pcgi.com'.format(artistName)
            # self.commentDict[self.episode] = val
            self.shotLists = [x for x in val]
            for each in val:
                with ConnectDB(self.project) as newdBConn:
                    # shotName = val
                    msg = 'UPDATE `{0}` SET `{1}_artist_name`="{2}",`{3}_status`="NYS" WHERE `shots` = "{4}"'.format(
                        self.episode, self.dept, artistName, self.dept, each)
                    print '------------------------------------------------------'
                    print msg
                    print '------------------------------------------------------'
                    newdBConn.execute(msg)
            self.mailScenarios('Assign')

    def reassignShot(self, artistShotDict):
        """
        This will reassign the shots to the passed artists with a comment of why it's been reassigned.
        :param artistShotDict: 
        :type artistShotDict: 
        :return: 
        :rtype: 
        """
        self.commentDict = dict()
        for key, val in artistShotDict.iteritems():
            self.receiver = '{}@pcgi.com'.format(key)
            with ConnectDB(self.project) as newdBConn:
                artistName = key
                for each in val:
                    shotName, comment = each
                    self.commentDict[shotName] = comment
                    msg = 'UPDATE `{0}` SET `{1}_artist_name`="{2}", `{3}_comments`=CONCAT(COALESCE({4}_comments,' \
                          ' ""), "{5}"), `{7}_status`="TWIP" WHERE `shots` = "{6}"'.format(self.episode, self.dept,
                                                                                           artistName,
                                                                                           self.dept, self.dept,
                                                                                           comment,
                                                                                           shotName, self.dept)
                    newdBConn.execute(msg)
            self.mailScenarios('Reassign')

    def retakeShot(self, artistShotDict):
        """
        This will add a retake to the shots with the retake comments.
        :param artistShotDict: 
        :type artistShotDict: 
        :return: 
        :rtype: 
        """
        self.commentDict = dict()
        for key, val in artistShotDict.iteritems():
            artistName = key
            self.receiver = artistName
            with ConnectDB(self.project) as newdBConn:
                for each in val:
                    shotName, comment = each
                    self.commentDict[shotName] = comment
                    msg = 'UPDATE `{0}` SET `{1}_status`="TWIP", `{2}_comments`="{3}" WHERE `shots` = "{4}"'.format(
                        self.episode, self.dept, self.dept, comment, shotName)
                    newdBConn.execute(msg)
            self.mailScenarios('Retake')

    def approveShot(self, artistShotDict):
        """
        This will approve the shots.
        :param artistShotDict: 
        :type artistShotDict: 
        :return: 
        :rtype: 
        """
        self.commentDict = dict()
        for key, val in artistShotDict.iteritems():
            self.shotLists = list()
            artistName = key
            self.receiver = artistName
            self.shotLists = [x for x in val]
            with ConnectDB(self.project) as newdBConn:
                # shotName = val
                for each in val:
                    msg = 'UPDATE `{0}` SET `{1}_status`="APP" WHERE `shots` = "{2}"'.format(self.episode, self.dept,
                                                                                             each)
                    print msg
                    newdBConn.execute(msg)
            self.mailScenarios('Approve')

    def mailScenarios(self, scenario):
        """
        This will send mail with the scenario messages to the specific senders.
        :param scenario: 
        :type scenario: 
        :return: 
        :rtype: 
        """
        mailSubject = ''
        messageBody = ''
        while Switch(scenario):
            if case('Reassign'):
                print 'Reassigning shot(s)'
                mailSubject = '{} - {} Shot(s) Reassigned.'.format(self.project, self.dept.title())
                messageBody = 'Following shot(s) has been reassigned to you :\n'
                break
            if case('Retake'):
                print 'Retake for shot(s)'
                mailSubject = '{} - {} Shot(s) on Retake.'.format(self.project, self.dept.title())
                messageBody = 'Following shot(s) has been set back to retake :\n'
                break
            if case('Assign'):
                print 'Assigning shot(s)'
                mailSubject = '{} - {} Shot(s) Assigned.'.format(self.project, self.dept.title())
                messageBody = 'Following shot(s) has been assigned to you :\n'
                # messageBody = '\n'.join(self.shotLists)
                break
            if case('Approve'):
                print 'Assigning shot(s)'
                mailSubject = '{} - {} Shot(s) Approved.'.format(self.project, self.dept.title())
                messageBody = 'Following shot(s) has been approved :\n'
                # messageBody = '\n'.join(self.shotLists)
                break
            break

        if self.commentDict:
            for key, val in self.commentDict.iteritems():
                newVal = ''
                # if
                messageBody += '{} - {}\t:\t{}\n'.format(self.episode, key, val)

        if self.shotLists:
            for eachShot in self.shotLists:
                messageBody += '{} - {}\n'.format(self.episode, eachShot)


        print '<-----------------------------------------'
        print self.sender
        print self.receiver
        print messageBody
        print '<-----------------------------------------'

        # send_mail(mail_sub='', mail_body='', sender='', receivers=list()):
        send_mail(mail_sub=mailSubject, mail_body=messageBody, sender=self.sender, receivers=self.receiver)
