import requests
from dateutil.parser import parse as parse_date


DATETIME_FIELDS = [
    'created_at', 'updated_at', 'date_taken', 'date_received'
]


def fetch_images():
    url = 'https://mars.nasa.gov/api/v1/raw_image_items/?order=sol+desc%2C' + \
          'date_taken+desc&per_page=50&page=0&condition_1=insight%3Amission&search=&extended='

    res = requests.get(url)
    res.raise_for_status()
    items = res.json()['items']

    for item in items:
        for f in DATETIME_FIELDS:
            item[f] = parse_date(item[f])

    return sorted(items, key=lambda i: i['date_taken'], reverse=True)
