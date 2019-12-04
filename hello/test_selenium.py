import pandas as pd
import json
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.keys import Keys


date = pd.datetime.today() + pd.offsets.Week()
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
