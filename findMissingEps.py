import makeMetaData as mmd
from dotenv import load_dotenv
import os

load_dotenv(override=True)
mmd.initData()

plex = mmd.PlexServer(os.getenv('PLEX_URL'),os.getenv('PLEX_TKN'))
one_piece = plex.library.section('TV Shows').get('One Piece')

hasMissing = False
presentEpisodes = []

for season in one_piece.seasons():
    for episode in season.episodes():
        presentEpisodes.append(os.path.splitext(os.path.basename(episode.media[0].parts[0].file))[0])

for epName in mmd.EPISODE_DICT.keys():
    if(not epName in presentEpisodes):
        if(not hasMissing):
            print("You are missing the following episodes:")
            hasMissing = True
        
        print(f"\t{mmd.BLUE}{epName}{mmd.RESET}")

if(not hasMissing):
    print("All episodes present")