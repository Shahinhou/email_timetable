#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
from main import send_mail


#s = input("Course Name: ")
today = str(datetime.datetime.now()).split()[0]
#print(today)

#url = f"https://mytimetable.dcu.ie/timetables?date={today}&view=week&timetableTypeSelected=525fe79b-73c3-4b5c-8186-83c652b3adcc&searchText=fn1&selections=525fe79b-73c3-4b5c-8186-83c652b3adcc__6032d0c5-1557-861e-cb85-6ece263aaaff_4eeae590-8339-eb25-ad27-39779001d766_fd5aca8a-2471-5733-d214-000999bceb44_14cf8892-6a93-2e18-b19e-76408275829d"
#url = f"https://mytimetable.dcu.ie/timetables?date={today}&view=agenda&timetableTypeSelected=525fe79b-73c3-4b5c-8186-83c652b3adcc&searchText=fn1&selections=525fe79b-73c3-4b5c-8186-83c652b3adcc__6032d0c5-1557-861e-cb85-6ece263aaaff_4eeae590-8339-eb25-ad27-39779001d766_fd5aca8a-2471-5733-d214-000999bceb44_14cf8892-6a93-2e18-b19e-76408275829d"
url = f"https://mytimetable.dcu.ie/timetables?date={today}&view=agenda&timetableTypeSelected=525fe79b-73c3-4b5c-8186-83c652b3adcc&selections=525fe79b-73c3-4b5c-8186-83c652b3adcc__6032d0c5-1557-861e-cb85-6ece263aaaff_4eeae590-8339-eb25-ad27-39779001d766_fd5aca8a-2471-5733-d214-000999bceb44_14cf8892-6a93-2e18-b19e-76408275829d_78db1e2a-2ff3-9d98-22d4-1d99f79f75ab_e198c955-47c6-43da-1d1f-32a3fefe47b0_f290f4d2-2e30-c7cb-48e3-00a7e0375317_b2cabe24-b2a6-bed3-cca3-315da3eca681_37ded32a-659c-148e-79a5-5dde2bf5e72b_5e98da33-25cd-e555-c644-1946002c8f51_d7598bc4-afce-efee-26ff-bbaaf8fc074a_b88f3119-b4fd-034a-8da6-92394a7db05a&searchText=hd110"
#options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
# agenda&timetable / week&timetable ??

driver = webdriver.Chrome() #options=options)

driver.implicitly_wait(10)
driver.get(url) #+"&searchText=comsci2")

search_bar = driver.find_elements(By.ID, "mat-input-0")[0]
#print(driver.current_url)

box = driver.find_elements(By.CLASS_NAME, "e-appointment")
places = driver.find_elements(By.CLASS_NAME, "scheduler-value.scheduler-value--location")
lengths = driver.find_elements(By.CLASS_NAME, "scheduler-value.scheduler-value--_duration")
times = driver.find_elements(By.CLASS_NAME, "scheduler-value.scheduler-value--_starttime")
days = driver.find_elements(By.CLASS_NAME, "scheduler-value.scheduler-value--_day")
dates = driver.find_elements(By.CLASS_NAME, "scheduler-value.scheduler-value--_date")
names = driver.find_elements(By.CLASS_NAME, "scheduler-value.scheduler-value--module.name")
#print(names)

i = 0
curr = 0
d = {n:[] for n in range(0,7)}
#print(d)
di = 0
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day = ""

while i < len(places) and day != "Friday":

    bus = ''
    title = box[i].get_attribute('aria-label').split('Begin')[0]
    
    x = places[i].find_elements(By.CLASS_NAME, "ng-star-inserted")[0]
    y = x.find_elements(By.TAG_NAME, 'p')[0].get_attribute("innerHTML")
    room = y

    x = dates[i].find_elements(By.CLASS_NAME, "ng-star-inserted")[0]
    y = x.find_elements(By.TAG_NAME, 'p')[0].get_attribute("innerHTML")
    date = y

    x = days[i].find_elements(By.CLASS_NAME, "ng-star-inserted")[0]
    y = x.find_elements(By.TAG_NAME, 'p')[0].get_attribute("innerHTML")
    day = y


    x = times[i].find_elements(By.CLASS_NAME, "ng-star-inserted")[0]
    y = x.find_elements(By.TAG_NAME, 'p')[0].get_attribute("innerHTML")
    time = y

    x = names[i].find_elements(By.CLASS_NAME, "ng-star-inserted")[0]
    y = x.find_elements(By.TAG_NAME, 'p')[0].get_attribute("innerHTML")
    name = y.split(' ',1)[1]

    x = lengths[i].find_elements(By.CLASS_NAME, "ng-star-inserted")[0]
    y = x.find_elements(By.TAG_NAME, 'p')[0].get_attribute("innerHTML")
    length = y

    if curr == 0:
        curr = day
        bus = f"GET BUS AT: {int(time.split(':')[0])-3}:{int(time.split(':')[1])+30}"


    elif curr != day:
        curr = day
        bus = f"GET BUS AT: {int(time.split(':')[0])-3}:{int(time.split(':')[1])+30}"
        print(day)
        print(bus)
        di += 1

    #print(day)
    
    d[di].append((f"{bus}\n<br>\n<em>{title}</em>\n<br>\n{name}, {date}, {day}, {time}, {room}, {length}").split(','))

    i += 1

#print(d)
with open('tmp.txt', 'w') as f:
    for i,n in enumerate(weekdays):

        f.write(f"<b>{n}</b>")
        f.write("<ul>")
        for s in d[i]:
            js = ', '.join(s)
            f.write(f"<li>{js}</li>")
        f.write("</ul><br>")

with open('tmp.txt') as f:
    lines = f.readlines()

send_mail(''.join(lines),"shahinhoushidari@gmail.com")
send_mail(''.join(lines),"roisindefaoite@yahoo.com")
send_mail(''.join(lines),"cebhanhoushidari@gmail.com")
send_mail(''.join(lines),"cebhan.houshidari2@mail.dcu.ie")
send_mail(''.join(lines),"kate.mckenna27@mail.dcu.ie")


print(''.join(lines))
