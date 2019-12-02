from django.shortcuts import render
from django.http import JsonResponse
import requests
import pandas as pd

from .models import Greeting


def index(request):
    date = pd.datetime.today() + pd.offsets.Week()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6,de;q=0.5,es;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.decolar.com',
        'Postman-Token': '17b0d348-1049-45d3-83e2-1ef879f706c5,258e5d2d-cc81-4aeb-97ba-59ecd46a3e1f',
        'Pragma': 'no-cache',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'X-RequestId': 'aSgTfvwgRQ',
        'X-Requested-With': 'XMLHttpRequest',
        'X-UOW': 'results-03-1575259116296',
        'XDESP-REFERRER': 'https://www.decolar.com/',
        'cache-control': 'no-cache',
    }
    params = (
        ('adults', '1'),
        ('children', '0'),
        ('infants', '0'),
        ('limit', '4'),
        ('site', 'BR'),
        ('channel', 'site'),
        ('from', 'RIO'),
        ('to', 'SAO'),
        ('departureDate', date.strftime('%Y-%m-%d')),
        ('groupBy', 'default'),
        ('orderBy', 'total_price_ascending'),
        ('viewMode', 'CLUSTER'),
        ('language', 'pt_BR'),
        ('airlineSummary', 'false'),
        ('chargesDespegar', 'false'),
        ('user', 'b18f68ef-9226-4fd6-8f68-ef92266fd6f8'),
        ('h', 'b9684fdcf50f468ae9c40c481674b3b1'),
        ('flow', 'SEARCH'),
        ('di', '1-0'),
        ('clientType', 'WEB'),
        ('disambiguationApplied', 'false'),
        ('newDisambiguationService', 'true'),
        ('initialOrigins', 'RIO'),
        ('initialDestinations', 'SAO'),
        ('pageViewId', 'e68b5d87-e9e9-4ad3-b518-6069de46b303'),
    )
    response = requests.get(
        'https://www.decolar.com/shop/flights-busquets/api/v1/web/search',
        headers=headers,
        params=params
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
