from bs4 import BeautifulSoup
from selenium import webdriver
import json
import requests
from datetime import datetime, timedelta
import time
import pandas as pd
from tqdm import tqdm

number_days = 1
url_head = 'https://gestion.pe'

# make sure your version of webdriver is the same of your current Chrome
# https://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/
driver = webdriver.Chrome(executable_path=r"C:\dchrome\chromedriver_v114.exe")

# list all the dates
current_date = datetime.now()
dates = []
for i in range(number_days):
    current_date -= timedelta(days=1)
    # starts the day before
    before_day = current_date.strftime('%Y-%m-%d %H:%M:%S')[:10]
    dates.append(before_day)
print(dates)

records = []
for date in dates:
    print(date)
    url_day = 'https://gestion.pe/archivo/todas/' + date
    driver.get(url_day)
    
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break
            
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    content = soup.find('div', attrs={'class': "content-sidebar flex mt-20 mb-20"} )
    news = content.find_all('div', attrs={'class': "story-item__information-box w-full"})
    dates_content = content.find_all('p', class_="story-item__date font-thin ml-5 text-xs text-gray-300 md:mt-5 md:ml-0")

    for idx, new in enumerate(news):
        title = new.find('a').text
        url = new.find('a')['href']
        date = dates_content[idx].text

        if '2022' not in date:
            # when is the current day, the date is in hours yet.
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:10]
        try:
            rx = requests.get(url_head + url)
            soupx = BeautifulSoup(rx.text, 'html.parser')
            data = json.loads(soupx.find_all('script', type='application/ld+json')[1].string)
            text = data['articleBody']

            if len(text) > 2:
                records.append((date, title, text, url))
        except:
            # could be because of video new
            continue

# Save extracted news as .csv
df = pd.DataFrame(records, columns=['date', 'title', 'text', 'url'])
print(df.shape[0])
df.to_csv('data/{}_{}-news.csv'.format(dates[0], number_days), index=False)