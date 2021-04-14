import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

df = pd.read_csv('list.csv')
font = ImageFont.truetype('arial.ttf',60)
for index,j in df.iterrows():
    img = Image.open('certificate.jpg')
    draw = ImageDraw.Draw(img)
    draw.text(xy=(725,760),text='{}'.format(j['name']),fill=(0,0,0),font=font)
    img.save('pictures/{}.jpg'.format(j['name']))

fromaddr = "EMAIL address of the sender"

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = fromaddr

for index,j in df.iterrows():
    toaddr = j['email']

# storing the receivers email address
    msg['To'] = toaddr

# storing the subject
    msg['Subject'] = "Subject of the Mail"

# string to store the body of the mail
    body = "Body_of_the_mail"

# attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

# open the file to be sent
    filename = j['name'] + ".jpg"
    open_file = "pictures/" + filename
    attachment = open(open_file, "rb")

# instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
    p.set_payload((attachment).read())

# encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
    msg.attach(p)

# creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
    s.starttls()

# Authentication
    password = "password of the email-id"
    s.login(fromaddr, password)

# Converts the Multipart msg into a string
    text = msg.as_string()

# sending the mail
    s.sendmail(fromaddr, toaddr, text)

# terminating the session
    s.quit()
