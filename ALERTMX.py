import smtplib
from email.mime.text import MIMEText
USERNAME = "your_username"
PASSWORD = "your_password"
DISPLAYNAME = "your_displayname"
MAILSERVER = "mail.your-website.com"

class AlertEmail:
    ''' AlertEmail. takes: to(addr), subject, message. '''

    def __init__(self, to, subject, message, **kwargs):
        self.from_ = (USERNAME, PASSWORD, DISPLAYNAME)
        self.to = to
        self.subject = subject
        self.message = message  
        self.smtp_server = MAILSERVER
        self.srv = smtplib.SMTP(self.smtp_server, 587)
        if kwargs:
            if "now" in kwargs:
                if kwargs['now'] is True:
                    self.send()
                else:
                    pass
        

    def send(self):
        ''' send(). takes no arguments.
        (to, subject, message) are already entered when the class is 
        initialized. '''
        ret_stat = ["Failed!", "Success.", "Unknown"]
        try:
            self.srv.ehlo()
            self.srv.starttls()
            self.srv.ehlo()
            self.srv.login(self.from_[0], self.from_[1])
            #print("Login OK.")
            msg = MIMEText(self.message, "html")
            msg['From'] = self.from_[2] + '<' + self.from_[0] + '>'
            msg['To'] = self.to
            msg['Subject'] = self.subject
            #print("From: {} To: {} Msg: {}".format(self.from_[0], self.to, msg))
            self.srv.sendmail(msg['From'], msg['To'], msg.as_string())
            #print(ret_stat[1])
            self.srv.quit()
            return(ret_stat[1])
        except Exception as e:
            print("Caugt exception: {}".format(e))
            print(ret_stat[0])
            self.srv.quit()
            return(ret_stat[0])

################## END CLASS ###########################
