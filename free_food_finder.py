import email
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
import time
import pyperclip
import smtplib
from email.message import EmailMessage


driver = webdriver.Edge()
driver.get("https://stthomas.campuslabs.com/engage/events?perks=FreeFood")

element = driver.find_element(By.TAG_NAME, 'body')
time.sleep(10)
element.send_keys(Keys.CONTROL+'a')
element.send_keys(Keys.CONTROL+'c')

lines = pyperclip.paste().splitlines()
events = []
event = []
start_printing = False
counter = 0

today = date.today()
d = today.strftime("%B %d")

for idx, line in enumerate(lines):
    if '1-15' in line:
        start_printing = False
    elif start_printing:
        if counter == 0:
            counter += 1
            continue
        elif counter % 4 == 1:
            line = "Name: " + line
        elif counter % 4 == 2:
            line = "Time: " + line
        elif counter % 4 == 3:
            line = "Location: " + line
        elif counter % 4 == 0:
            line = "Club: " + line
        event.append(line)
        if counter != 0 and counter % 4 == 0:
            events.append(event)
            event = []
        counter += 1
    elif '15 out of' in line:
        start_printing = True

email_str = ""

for event in events:
    if d in " ".join(event):
        for line in event:
            if 'Time: ' in line:
                email_str = email_str + '\t' + "Time: " + line.split(' at ')[1] + '\n'
            else:
                email_str = email_str + '\t' + line + '\n'
        email_str = email_str + '\n'
print(email_str)
driver.close()

if email_str != "":
    email_str = '"So, whether you eat or drink, or whatever you do, do everything for the glory of God." 1 Corinthians 10:31\n\nEvents with Free Food Today:\n\n' + email_str
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('free.food.ust@gmail.com', 'ytldnjyaedqmiycv')
    msg = EmailMessage()
    message = f'{email_str}\n'
    msg.set_content(message)
    msg['Subject'] = today.strftime('%A') + ' Free Food Report'
    msg['From'] = 'free.food.ust@gmail.com'
    msg['To'] = ['audi3920@stthomas.edu', 'voge8911@stthomas.edu']
    server.send_message(msg)
    print("Email sent.")
else:
    print("No free food events today.")
