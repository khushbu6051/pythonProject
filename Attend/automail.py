import yagmail
import os
import datetime
date = datetime.date.today().strftime("%B %d, %Y")
path = 'Attendance'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
filename = newest
sub = "Attendance Report for " + str(date)
# mail information
yag = yagmail.SMTP(user="i4usmriti@gmail.com",  password='10419922')
body= "kindly Find Attachment"
# sent the mail
yag.send(
    to="i4usmriti@gmail.com",
    subject=sub, # email subject
    contents=body,  # email body
    attachments= filename  # file attached
)
print("Email Sent!")
