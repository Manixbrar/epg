import gzip
import json
import re
import pytz
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import zipfile
import time
stime = time.time()

# Create an XML root element
root = ET.Element('tv')
root.set('generator-info-name', 'samoz')
root.set('generator-info-url', 'https://epg.samoz.cf')
root.text='\n'
root.tail='\n'
channel = ET.SubElement(root, 'channel', {'id': 'indtvprogram'})
channel.text='\n'
channel.tail='\n'
display_name = ET.SubElement(channel, 'display-name')
display_name.text = 'Indtvprogram'
display_name.tail='\n'

# -------------------------------------------------------- Jio start here ----------------------------
json_file_path = 'jio.json'
with open(json_file_path, 'r') as json_file:
    data = json_file.read()
data = data.replace("&", "And")
result = json.loads(data)
LANG_MAP = {
    6: "English", 1: "Hindi", 2: "Marathi", 3: "Punjabi", 4: "Urdu", 5: "Bengali", 7: "Malayalam", 8: "Tamil",
    9: "Gujarati", 10: "Odia", 11: "Telugu", 12: "Bhojpuri", 13: "Kannada", 14: "Assamese", 15: "Nepali", 16: "French",
}
# Iterate through the JSON data and create XML elements
for page in result:
    channel_element = ET.SubElement(root, 'channel')
    channel_element.set('id', str(page["channel_id"]))
    channel_element.text = '\n'
    channel_element.tail = '\n'
    display_name_element = ET.SubElement(channel_element, 'display-name')
    display_name_element.text = page["channel_name"]
    display_name_element.tail = '\n'
    icon_element = ET.SubElement(channel_element, 'icon')
    icon_element.set('src', f'http://jiotv.catchup.cdn.jio.com/dare_images/images/{page["logoUrl"]}')
    icon_element.tail='\n'

   
    

# -------------------------------------------------------- Tata Starts Here ----------------------------
# Read the JSON file
with open('tata.json', 'r') as file:
    data = json.load(file)

# Replace '&' with 'And' in the JSON string
json_string = json.dumps(data).replace("&", "And")
result = json.loads(json_string)

# Extract the desired data
JSON = result['data']['list']


for page in JSON:
    channel = ET.SubElement(root, 'channel', {'id': f'ts{page["id"]}'})
    channel.text='\n'
    channel.tail='\n'
    display_name = ET.SubElement(channel, 'display-name')
    display_name.text = page['title']
    display_name.tail='\n'
    icon = ET.SubElement(channel, 'icon', {'src': page['boxCoverImage']})
    icon.tail='\n'
#--------------------------------------------------------- Zee Starts Here------------------------------

with open('zee.json', 'r') as file:
    json_data = file.read()
json_data = json_data.replace("&", "And")
result = json.loads(json_data)

for page in result:
    channel = ET.SubElement(root, "channel")
    channel.text='\n'
    channel.tail='\n'
    channel.set("id", page["channel_id"])
    channel.tail='\n'
    display_name = ET.SubElement(channel, "display-name")
    display_name.text = page["channel_name"]
    display_name.tail='\n'


#----------------------------------------------------Astro Starts here--------------------------------
with open('astro.json', 'r') as file:
    data = file.read()
data = data.replace('&', 'And')
result = json.loads(data)
for page in result:
    channel = ET.SubElement(root, 'channel', id=f'astro_{page["channel_id"]}')
    channel.text='\n'
    channel.tail='\n'
    display_name = ET.SubElement(channel, 'display-name')
    display_name.text = page["channel_name"]
    display_name.tail='\n'

#-------------------------------------------------------- Main Programmee XML Starts from Here-------------------------------------------------------
# -------------------------------------------------------- Jio Starts Here Again ------------------------
london_tz = pytz.timezone("Europe/London")

with open('jio.json', 'r') as json_file:
    result = json.load(json_file)

# Define the language map
LANG_MAP = {
    6: "English", 1: "Hindi", 2: "Marathi", 3: "Punjabi", 4: "Urdu", 5: "Bengali", 7: "Malayalam", 8: "Tamil",
    9: "Gujarati", 10: "Odia", 11: "Telugu", 12: "Bhojpuri", 13: "Kannada", 14: "Assamese", 15: "Nepali", 16: "French",
}
# Iterate through the result data
for page in result:
    for x in range(2):  # Change the range as needed
        # Make a GET request to fetch data
        url = f"https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?offset={x}&channel_id={page['channel_id']}&langId=6"
        response = requests.get(url)
        raw_data = response.text
        if raw_data != 'Params Incorrect\n' and raw_data != '':
            raw_data = raw_data.replace("&", "And")
            jSON = json.loads(raw_data)
            epg = jSON['epg']

            for jio in epg:
                try:
                    original_start_string = jio['startEpoch']
                    original_end_string = jio['endEpoch']
                    trimmed_start = str(original_start_string)[:-3]
                    trimmed_end = str(original_end_string)[:-3]
                    start_timestamp = int(trimmed_start) - 0
                    end_timestamp = int(trimmed_end) - 0
                    start_dt = datetime.fromtimestamp(start_timestamp, london_tz)
                    end_dt = datetime.fromtimestamp(end_timestamp, london_tz)
                    start = start_dt.strftime('%Y%m%d%H%M%S')
                    end = end_dt.strftime('%Y%m%d%H%M%S')
                   
                except ValueError:
                    # Handle invalid timestamp values here
                    start = end = "InvalidTimestamp"

                programme = ET.SubElement(root, 'programme', {
                    'channel': str(jio["channel_id"]),
                    'start': f'{start} +0000',
                    'stop': f'{end} +0000',
                    'catchup-id': str(jio["srno"])
                })
                programme.text = '\n'
                programme.tail='\n'
                title = ET.SubElement(programme, "title", {'lang': 'en'})
                title.text = jio["showname"]
                title.tail = '\n'
                desc = ET.SubElement(programme, "desc", {'lang': 'en'})
                desc.text = jio["description"]
                desc.tail='\n'
                icon = ET.SubElement(programme, "icon", {'src': f"http://jiotv.catchup.cdn.jio.com/dare_images/shows/{jio['episodeThumbnail']}"})
                icon.tail='\n'

#Additional loops
for x in range(2):  # Change the range as needed
    url = f"https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?offset={x}&channel_id=1301&langId=6"
    response = requests.get(url)
    raw_data = response.text
    raw_data = raw_data.replace("&", "And")
    jSON = json.loads(raw_data)
    dummy = jSON['epg']

    for jio in dummy:
        try:
                    original_start_string = jio['startEpoch']
                    original_end_string = jio['endEpoch']
                    trimmed_start = str(original_start_string)[:-3]
                    trimmed_end = str(original_end_string)[:-3]
                    start_timestamp = int(trimmed_start) - 0
                    end_timestamp = int(trimmed_end) - 0
                    start_dt = datetime.fromtimestamp(start_timestamp, london_tz)
                    end_dt = datetime.fromtimestamp(end_timestamp, london_tz)
                    start = start_dt.strftime('%Y%m%d%H%M%S')
                    end = end_dt.strftime('%Y%m%d%H%M%S')
                    
            
        except ValueError:
            # Handle invalid timestamp values here
            start = end = "InvalidTimestamp"

        programme = ET.SubElement(root, "programme", {
            "channel": "indtvprogram",
            "start": f"{start} +0000",
            "stop": f"{end} +0000",
        })
        programme.text = '\n'
        programme.tail='\n'
        title = ET.SubElement(programme, "title", {"lang": "en"})
        title.text = "Program"
        title.tail = '\n'
        desc = ET.SubElement(programme, "desc", {"lang": "en"})
        desc.text = "Program"
        desc.tail='\n'




#---------------------------------------------TATA Again Start from here---------------------------------------------------------
# Loop through the TATA JSON data
with open('tata.json', 'r') as file:
    data = json.load(file)

# Replace '&' with 'And' in the JSON string
json_string = json.dumps(data).replace("&", "And")
result = json.loads(json_string)

# Extract the desired data
JSON = result['data']['list']
for page in JSON:
    for x in range(2):  # Repeat for 2 days
        date = (datetime.now() + timedelta(days=x)).strftime('%d-%m-%Y')

        # Make an HTTP request
        url = f"https://tm.tapi.videoready.tv/content-detail/pub/api/v2/channels/schedule?date={date}"
        payload = {"id": page["id"], "timeSlots": []}
        headers = {
            "Authority": "tm.tapi.videoready.tv",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()
        code = response_json.get('code')

        # Process the response JSON if code is 0
        if code == 0:
            epg_list = response_json['data']['epg']

            for epg in epg_list:
                start_org = str(epg['startTime'])[:-3]
                end_org = str(epg['endTime'])[:-3]
                start_timestamp = int(start_org) - 0
                end_timestamp = int(end_org) - 0
                start_dt = datetime.fromtimestamp(start_timestamp, london_tz)
                end_dt = datetime.fromtimestamp(end_timestamp, london_tz)
                start = start_dt.strftime('%Y%m%d%H%M%S')
                end = end_dt.strftime('%Y%m%d%H%M%S')

                # Convert integer values to strings
                page_id_str = str(page["id"])
                epg_id_str = str(epg['id'])
                # Create XML elements for each program
                programme = ET.SubElement(root, 'programme', {
                    'channel': f'ts{page_id_str}',
                    'start': f'{start} +0000',
                    'stop': f'{end} +0000',
                    'catchup-id': epg_id_str
                })
                programme.text = '\n'
                programme.tail='\n'
                title = ET.SubElement(programme, 'title', {'lang': 'en'})
                title.text = epg['title']
                title.tail = '\n'
                desc = ET.SubElement(programme, 'desc', {'lang': 'en'})
                desc.text = epg['desc']
                desc.tail = '\n'
                icon = ET.SubElement(programme, 'icon', {'src': epg['boxCoverImage']})
                icon.tail = '\n'
#-----------------------------------------------------------------Zee Xml start Again----------------------------

with open('zee.json', 'r') as file:
    json_data = file.read()
result = json.loads(json_data)
for page in result:
    channel_id = page["channel_id"]
    url = f'https://contentapi.zee5.com/content/epg?channels={channel_id}&start=0&end=1'

    headers = {
        'Sec-Ch-Ua': '\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"',
        'Referer': 'https://www.zee5.com/',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Access-Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTA4LTEyVDAyOjI3OjMwLjczM1oiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5MTgwNzI1MH0.o6L60agR0xHRIKwI90thMBC-He7VZNqqnvm1l66GhKA',  # Your token here
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Sec-Ch-Ua-Platform': '\"Windows\"'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 403 and response.status_code != 502:
       raw_data = response.text
    json_data = json.loads(raw_data)
    if "items" in json_data and len(json_data["items"]) > 0 and "items" in json_data["items"][0]:
        items = json_data["items"][0]["items"]

    for zee in items:
        start_time = zee["start_time"]
        end_time = zee["end_time"]
        start_datetime = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
        end_datetime = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
        start_dt = start_datetime.replace(tzinfo=pytz.utc).astimezone(london_tz)
        end_dt = end_datetime.replace(tzinfo=pytz.utc).astimezone(london_tz)
        start = start_dt.strftime("%Y%m%d%H%M%S")
        end = end_dt.strftime("%Y%m%d%H%M%S")

        programme = ET.SubElement(root, "programme")
        programme.set("channel", channel_id)
        programme.set("start", f"{start} +0000")
        programme.set("stop", f"{end} +0000")
        programme.text='\n'
        programme.tail='\n'

        title = ET.SubElement(programme, "title")
        title.set("lang", "en")
        title.text = zee["title"]
        title.tail='\n'

        description = zee.get("description", "")
    if description:
        desc = ET.SubElement(programme, "desc")
        desc.set("lang", "en")
        desc.text = zee["description"]
        desc.tail='\n'

#-----------------------------------------------------------------Astro Xml start Again----------------------------

with open('astro.json', 'r') as json_file:
    ch = json_file.read()

# Replace '&' with 'And'
ch = ch.replace("&", "And")

# Parse the JSON data
result = json.loads(ch)

# Iterate over channel data
for page in result:
    # Make an HTTP GET request to retrieve channel data
    url = f'https://contenthub-api.eco.astro.com.my/channel/{page["channel_id"]}.json'
    response = requests.get(url)
    raw_data = response.json()

    for x in range(2):
        date = (datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d')
        jSON = raw_data['response']['schedule'].get(date, [])  # Use .get() to handle missing date

        for program in jSON:
            start = program['datetimeInUtc'].replace(' ', '').replace(':', '').replace('-', '').replace('.0', '')
            stop = program['duration']
            title = program['title']
            desc = program['title']
         
                # Calculate the timestamp
            timestamp = int(datetime.strptime(start, '%Y%m%d%H%M%S').timestamp())
            stop_time = datetime.strptime(stop, '%H:%M:%S')
            seconds = stop_time.hour * 3600 + stop_time.minute * 60 + stop_time.second

                # Calculate the stop time
            timestamp_one_hour_later = timestamp + seconds
            start6 = datetime.fromtimestamp(timestamp_one_hour_later).strftime('%Y%m%d%H%M%S')

            # Create XML elements
            programme = ET.Element('programme', channel=f'astro_{page["channel_id"]}', start=f'{start} +0000', stop=f'{start6} +0000')
            title_elem = ET.Element('title', lang='en')
            title_elem.text = title
            desc_elem = ET.Element('desc', lang='en')
            desc_elem.text = desc

            programme.append(title_elem)
            programme.append(desc_elem)
            root.append(programme)

tree = ET.ElementTree(root)

xml_data = ET.tostring(tree.getroot(), encoding='utf-8', xml_declaration=True)

with gzip.open("allepg.xml.gz", "wb") as file:
    file.write(xml_data)
    
# print("Update done")
    print("EPG updated", datetime.now())
    print(f"Took {time.time()-stime:.2f} seconds")
