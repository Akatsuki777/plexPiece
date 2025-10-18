#Only has thumbnails till episode 54
#Thumbnails has not been implemented in main
import requests
import json
import time
from urllib.error import HTTPError

BASE_URL = 'https://kitsu.io/api/edge/anime/12/episodes?page%5Blimit%5D=20&page%5Boffset%5D={page_offset}&fields%5Bepisodes%5D=number,thumbnail'

with open('onePieceMetaData.json','r') as f:
    episode_data = json.load(f)

i=0

while True:
    try:
        response = requests.get(BASE_URL.format(page_offset=i))
        response.raise_for_status()

        data = json.loads(response.text)
        if(len(data['data'])==0):
            print("End of episode data:")
            break
        else:
            print("Fetched thumbnails from episodes {start} to {end}".format(start=i,end=i+len(data['data'])))
        
        for items in data['data']:
            if(not str(items['attributes']['number']) in episode_data.keys()):
                print("The end of episodes has reached in onePieceEpisodeMetaData.")
                break
            episode_data[str(items['attributes']['number'])]['thumbnail']=items['attributes']['thumbnail']['original'] if items['attributes']['thumbnail'] else None
        
        time.sleep(0.1)

        i += 20
    
    except HTTPError as e:
        print("Some error occured! If were less lazy, I would identify and handle the error here!\n"+e.code)
        break

with open('newOnePieceMetaData.json','w') as f:
    json.dump(episode_data,f)
