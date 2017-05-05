import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
fromaddr = "indiancouncilmedicalresearch@gmail.com"
toaddr = "kevintonb@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test"
body = "Test mail1"
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "icmr@123")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()