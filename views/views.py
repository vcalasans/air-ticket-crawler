import os
import pandas as pd
from django.http import FileResponse
import psycopg2


def index(request):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("select date,flightdate,departure,arrival,price from prices;")
    allEntries = cur.fetchall()
    df = pd.DataFrame(allEntries)
    df.to_excel(
        'file.xlsx',
        index=False,
        header=['Date', 'Flight Date', 'Departure', 'Arrival', 'Price (BRL)']
    )
    return FileResponse(
        open('file.xlsx', 'rb'),
        as_attachment=True,
        filename='prices.xlsx'
    )
