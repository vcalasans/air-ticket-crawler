#!/usr/bin/env python
import os
import json
import psycopg2
import pandas as pd
from seleniumwire import webdriver


currentDate = pd.datetime.today()
date = currentDate + pd.offsets.Week()
formattedDate = date.strftime('%Y-%m-%d')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)

# Go to the page
driver.get(f"https://www.decolar.com/shop/flights/search/oneway/RIO/SAO/{formattedDate}/1/0/0/NA/NA/NA/NA/?from=SB&di=1-0")

# Access requests via the `requests` attribute
matchingRequest = [ request for request in driver.requests if
                    request.path.startswith('https://www.decolar.com/shop/flights-busquets/api/v1/web/search') ][0]
dataClusters = json.loads(matchingRequest.response.body)['clusters']
bestCluster = list(filter(lambda x: x['bestCluster'] is True, dataClusters))[0]
bestPrice = bestCluster['priceDetail']['totalFare']['amount']
print(f"The best price is: R$ {bestPrice}")

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute(
    f"""insert into prices (date, flightdate, departure, arrival, price)
    values ('{pd.to_datetime(currentDate).round('H')}', '{pd.to_datetime(date).date()}', 'RIO', 'SAO', {bestPrice});"""
)
cur.execute("select * from prices;")
conn.commit()
print(cur.fetchall())
cur.close()