import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def sendEmail(email, password, message, recipients,
              subject, fl=None):
        server = smtplib.SMTP('smtp.gmail.com', 587)
	#server.starttls()
        server.connect("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
        recipients = ", ".join(recipients)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = recipients
        msg['Subject'] = subject

        part1 = MIMEText(message, 'plain')
        msg.attach(part1)
        if fl:
            with open(fl, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(fl)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(fl)
            msg.attach(part)

        server.sendmail(email, recipients, msg.as_string())
        server.quit()



