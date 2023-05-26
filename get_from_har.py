import json
import urllib.request
from haralyzer import HarParser
import os
import constants

print("You must have folder named 'harfiles' that has har files in your execution path ...")

flag = False
for path in os.listdir('./'):
    if path == "harfiles":
        flag = True
        break

if not flag:
    print("Folder named 'harfiles' doesn't exist")
    exit(1)


for path in os.listdir('./harfiles'):
    if len(path) > 4 and path[-3:] == 'har':

        if not os.path.exists('images'):
            os.makedirs('images')

        harname = path[:-4]
        folder_name = f'images/{harname}'
        
        f = open(f'./harfiles/{harname}.har', 'r', encoding="UTF-8")
        har_parser = HarParser(json.loads(f.read()))

        data = har_parser.har_data

        if data:
            entries = data['entries']
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            for entry in entries:
                try:
                    if '_resourceType' in entry and entry['_resourceType'] == 'image':
                        query = entry['request']['queryString']
                        if len(query) > 3 and query[0]['value'] != constants.PROFILE_IMAGE and query[0]['name'] == 'stp':
                            # Get request url
                            url = entry['request']['url']
                            # Unique name
                            name = query[3]['value']
                            if not os.path.exists(folder_name):
                                os.makedirs(folder_name)

                            print(f"Download {name}.jpg")
                            urllib.request.urlretrieve(
                                url, f"{folder_name}/{name}.jpg")

                except:
                    print(f"Faile to download {name}.jpg ...")
