import re
import json
from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
import pandas as pd

from .models import Greeting


def index(request):
    date = pd.datetime.today() + pd.offsets.Week()
    formattedDate = date.strftime('%Y-%m-%d')
    htmlResponseText = requests.get(f"https://www.decolar.com/shop/flights/search/oneway/RIO/SAO/{formattedDate}/1/0/0/NA/NA/NA/NA/?from=SB&di=1-0").text
    soup = BeautifulSoup(htmlResponseText, 'html.parser')
    head = soup.head.text
    searchParamsPattern = re.compile(r"^searchQuery : ({.*?})\n,$", re.MULTILINE | re.DOTALL)
    searchParamsText = searchParamsPattern.search(head).group(1)
    searchParamsDict = json.loads(searchParamsText)
    print(searchParamsDict)
    specialHeadersPattern = re.compile(r"""headers : {"X-UOW": '(.*?)',""", re.DOTALL)
    XUOWHeader = specialHeadersPattern.search(head).group(1)
    specialHHeaderReplacementPattern = re.compile(r'if\(o\.h\)o\.h = o\.h\.replace\("(.*?)"', re.DOTALL)
    specialHHeaderReplacementScript = soup.find("script", text=specialHHeaderReplacementPattern).text
    print(specialHHeaderReplacementScript)
    specialHHeaderReplacement = specialHHeaderReplacementPattern.search(specialHHeaderReplacementScript).group(1)
    print("special H header replacement: " + specialHHeaderReplacement)
    searchParamsDict['h'] = searchParamsDict['h'].replace(specialHHeaderReplacement, "")
    # searchParamsDict['h'] = "44ce942fe9e06b835507a0a67900c1ba"
    # XUOWHeader = "results-17-1575343741175"
    print('xuow is' + XUOWHeader)
    searchParams = list(searchParamsDict.items())
    print(searchParams)

    searchHeaders = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6,de;q=0.5,es;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.decolar.com',
        'Pragma': 'no-cache',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-UOW': XUOWHeader,
        'XDESP-REFERRER': 'https://www.decolar.com/',
        'cache-control': 'no-cache',
    }
    response = requests.get(
        'https://www.decolar.com/shop/flights-busquets/api/v1/web/search',
        headers=searchHeaders,
        params=searchParams
    )
    print(response.json())
    return JsonResponse(response.json())

# def index(request):
    # # return HttpResponse('Hello from Python!')
    # return render(request, "index.html")


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})
