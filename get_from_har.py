import json
import urllib.request
from haralyzer import HarParser
import os

PROFILE_IMAGE = ''

harname = ''
folder_name = ''

with open(f'{harname}.har', 'r') as f:
    har_parser = HarParser(json.loads(f.read()))

data = har_parser.har_data

if data:
    entries = data['entries']
    for entry in entries:
        if entry['_resourceType'] == 'image':
            query = entry['request']['queryString']
            if len(query) > 3 and query[0]['value'] != PROFILE_IMAGE and query[0]['name'] == 'stp':
                url = entry['request']['url']
                name = query[3]['value']
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                try:
                    print(f"Download {name}.jpg")
                    urllib.request.urlretrieve(
                        url, f"{folder_name}/{name}.jpg")
                except:
                    print(f"Faile to download {name}.jpg ...")
