from selenium import webdriver
from bs4 import BeautifulSoup
from time import *
import re
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from DB import *


async def get_ichunqiu():
    db = connect()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10)  # 留出js解析时间
    bot = nonebot.get_bot()
    try:
        send = {"platform": "ichunqiu"}
        driver.get('https://www.ichunqiu.com/competition/all')
        sleep(5)
        source = driver.page_source
        soup = BeautifulSoup(source, "lxml")
        msg = soup.find_all("big")
        for i in msg:
            driver.get(i.a["href"])
            sleep(5)
            url = driver.page_source
            urltext = BeautifulSoup(url, "lxml")
            send.update(name=i.find("h2").text)
            send.update(url=urltext.find("dl", class_="box_shadow").dt.a.text)
            for element, t in enumerate(i.find_all("b")):
                if element == 1:
                    send.update(format=t.text)
                elif element == 2:
                    TimeGroup = re.search(r"(.*)\s-\s(.*)", t.text)
                    send.update(start_time=TimeGroup.group(1))
                    send.update(end_time=TimeGroup.group(2))
                else:
                    continue
            if insert(db, send) == True:
                await bot.send_private_msg(user_id=ME, message="增加")


    except CQHttpError:
        pass

    driver.quit()
