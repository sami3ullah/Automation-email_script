import pandas
import smtplib
from chameleon import PageTemplate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# read csv file, containing the emails, name, passwords
file = pandas.read_csv("email_list.csv")

# read from template file
template_file = open('email-templates.html')
template = PageTemplate(template_file.read().encode('utf-8'))
template_file.close()

# extraction emails, sent
emails = file['Email'].values
sents = file['Sent'].values
usernames = file['Name'].values
passwords = file['Password'].values

server = smtplib.SMTP('smtp.gmail.com', 587)
# starting the server
server.starttls()

server.login('email', '*******')

done = False

# very poor time complexity, not optimized for data rows larger than 10^6
while not done:

    # O(emails) time complexity assuming sendmail function is O(1)
    for email in range(len(emails)):
        if sents[email] != "Yes":
            try:
                message = MIMEMultipart('alternative')
                message["Subject"] = 'Test Subject'
                message["From"] = 'xxxx@xxx.com'
                message.attach(MIMEText(template(username=usernames[email],user_email=emails[email], user_password=passwords[email]), "html"))
                message["To"] = emails[email]
                server.sendmail("mohsin@laam.pk", emails[email], message.as_string())
                sents[email] = "Yes"
                print("Email sent to: ", emails[email])
            except:
                print("Email not sent to: ", emails[email])
        else:
            print("Email already sent to: ", emails[email], " skipping...")
    
    done = True

    # O(emails) same as above time complexity
    for sent in sents:
        if sent != "Yes":
            done = False


# writing back in the csv file in the last column
pandas.DataFrame(file).to_csv('example.csv')

# quitting the server
server.quit()