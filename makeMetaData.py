import re
import os
import json
from types import SimpleNamespace
from plexapi.server import PlexServer
from datetime import datetime
from dotenv import load_dotenv

#TEXT FORMATS
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"
BOLD = "\033[1m"

#GLOBAL VARIABLES
HAS_VALID_FILE = False
CUR_DIR = ""
TITLE_LANG= "eng"
SEASON_DICT = {}
EPISODE_DICT = {}
EPISODE_META_DICT = {}
EPISODE_RE = re.compile(r"(?P<season>[A-Za-z' ]+?)\s+(?P<episode>\d{1,3})(?:\s|\.|$)")
SEASON_RE = re.compile(r"Season ([0-9]{1,2})")
VALID_EPISODES = re.compile(r"One Piece \(1999\) - S[0-9]{2}E[0-9]{2}\.[A-Za-z0-9]+")
POSTER_PATTERN = re.compile(r"Season ([0-9]{2}).*")
VIDEO_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm"}
STRINGS = SimpleNamespace(
    exitMessage=f"\n{BOLD}No Changes were made\n\n{RESET}{RED}{BOLD}EXITING...{RESET}",
    showNotFound=f"\n{RED}{BOLD}ERROR: {RESET}The show was not found in your plex library. Please ensure the current folder as a source in the 'TV Shows' category in plex settings",
    noFiles=f"\n{YELLOW}{BOLD}Warning:{RESET} No suitable files were found",
    noProcessedAdvance=f"{YELLOW}{BOLD}Warning:{RESET} Do you still want to proceed with adding metadata for the files in your current directory? (y/n):\t",
    moveMessage=f"\nDo you want to proceed with renaming and moving the files to the structure shown above? (y/n):\t",
    inputMessage = f"Do you want to skip this file(y) or exit(n)? (y/n)\t:",
    skippingFiles=f"{BLUE}{{EPISODE_NAME}} {RESET} is already formatted, so skipping the file.",
    fileNameFormatError=f"{RED}{BOLD}ERROR: {RESET}The file name {BLUE}{{CUR_EPISODE}}{RESET} is not in a recognizable format. Please rename everything to match the following format:\n\n\t\t______SEASON NAME___XX___.___\n\n\t\tXX\t-\tEpisode number within the season.",
    seasonNameError=f"{RED}{BOLD}ERROR: {RESET}The season name {BLUE}{{CUR_SEASON}}{RESET} couldn't be matched with the season database. Please rename the seasons to match the ones in {BLUE}One Pace Episode Guide - Season Sheet.csv{RESET}. ",
    processSuccess=f"{GREEN}FILES PROCESSED SUCCESSFULLY{RESET}\n\nThe following files have been processed successfully:",
    successSeasonName=f"\t├--{{Season_Name}}",
    successEpisodeName=f"\t|\t├--{{Episode_Name}}",
    successMove=f"{GREEN}All Files have been successfully renamed and moved.",
    metadataUpdated=f"{GREEN}{BOLD}Added: {RESET}The metadata for {{DATA_NAME}} has been successfully added!",
    finalSuccess=f"{GREEN}{BOLD}SUCCESS!{RESET} All data has been added and locked to prevent plex from autoupdating it. \n{GREEN}{BOLD}EXITING...{RESET}"
)

##
#Main Functions
##

#Retrieve adapted episode info from the episode csv to facilitate the metadata generation
def getEpisodes():

    episode_data = {}
    with open('onePieceMetaData.json','r') as f:
        episode_data = json.load(f)

    with open('One Pace Episode Guide - Meta.csv','r') as f:
       
        rePattern = r'One Pace (S\d{2}E\d{2}) - (.*)\.mkv'
        for lines in f.readlines():

            match = re.match(rePattern,lines)
            
            if(match):
                #Extract episode data from metadata based on the episodes used to adapt the paced version
                adaptedEpisodeList = re.split(r'[,\-\s]',match.group(2).replace(" ",""))
                epTimestamp = episode_data.get(adaptedEpisodeList[0]).get("release_date")
                epTitle = episode_data.get(adaptedEpisodeList[0]).get("title_"+TITLE_LANG)
                epSummary = ""
                for eps in adaptedEpisodeList:
                    if(episode_data[eps]):
                            epSummary += episode_data[eps]["summary"]

                EPISODE_DICT['One Piece (1999) - '+match.group(1)] = {
                    "title": epTitle,
                    "release_date":epTimestamp,
                    "summary": epSummary
                }


#Retrieve season names from the csv and store in the global val
def getSeasons():

    season_posters = {}

    for files in os.listdir(os.path.join(CUR_DIR,"One_Piece_Cover_Images")):
        match = re.match(POSTER_PATTERN,files)
        if not os.path.isdir(files) and match:
            season_posters[match.group(1)] = os.path.join(CUR_DIR,"One_Piece_Cover_Images",files)

    seasonData = {}
    with open('onePieceSeasonData.json','r') as f:
        seasonData = json.load(f)
        
    with open('One Pace Episode Guide - Season Sheet.csv','r') as f:
        rePattern = '(.*),(.*),(.*)'
        for lines in f.readlines():
            match = re.match(rePattern,lines)
            if(match):
                #Stores the 
                imageLoc = season_posters.get(prependZero(match.group(1)))

                SEASON_DICT[match.group(2).lower().strip()] = {
                    'season_number' : prependZero(match.group(1)),
                    'season_summary' : seasonData[match.group(1)]["summary"],
                    'season_image' : imageLoc
                }
                SEASON_DICT[match.group(1)] = {
                    'season_title' : seasonData[match.group(1)]["title"],
                    'season_summary': seasonData[match.group(1)]["summary"],
                    'season_image' : imageLoc
                }

#Check if the given file is a valid one pace file of a certain format
def validateEpisodes(epName):
    epData = EPISODE_RE.search(epName)
    if (VALID_EPISODES.search(epName)):
        print(STRINGS.skippingFiles.format(EPISODE_NAME=epName))
        HAS_VALID_FILE = True
        return None
    elif not epData:
        print(STRINGS.fileNameFormatError.format(CUR_EPISODE=epName))
        choice = input(STRINGS.inputMessage)
        if(choice[0]=='y' or choice[0]=='Y'):
            return None
        else:
            exit(1)
    else:
        return epData.groupdict()

#Build a dictionary of all feasible files, seasons, their paths and extensions
def organizeFiles():

    fileNameDict = {}
    for root,dirs,file in os.walk(os.getcwd()):
        for files in file:
            extension = os.path.splitext(files)[1].lower()
            if extension in VIDEO_EXTS:
                fileNameDict[files] = {}
                epInfo = validateEpisodes(files)
                if(epInfo!=None):
                    CUR_SEASON = epInfo["season"]
                    try:
                        seasonNum = SEASON_DICT[CUR_SEASON.lower().strip()]["season_number"]
                        fileNameDict[files]['season'] = seasonNum
                        fileNameDict[files]['episode'] = prependZero(epInfo["episode"])
                        fileNameDict[files]['path'] = os.path.abspath(os.path.join(root,files,os.path.pardir))
                        fileNameDict[files]['extension'] = extension
                    except:
                        print(STRINGS.seasonNameError.format(CUR_SEASON=CUR_SEASON))
                        choice = input(STRINGS.inputMessage)
                        if(choice[0]=='y' or choice[0]=='Y'):
                            del fileNameDict[files]
                        else:
                            exit(1)
                else:
                    del fileNameDict[files]
    
    return fileNameDict

#Print the files that have been indexed
def displayDict(fileDict):

    seasonFlag = False
    curSeason = ''
   
    
    
    for key,data in sorted(fileDict.items(),key=lambda x :x[1]["season"]):
        if(data['season']!=curSeason):
            seasonFlag = True

        if(seasonFlag):
            print(STRINGS.successSeasonName.format(Season_Name="Season "+data['season']))
            seasonFlag = False


        print(STRINGS.successEpisodeName.format(Episode_Name=getNewEpName(data['season'],data['episode'],data['extension'])))
        curSeason = data['season']

#Check for existing folders and create if necessary, rename/move files into folders and cleanup empty folders
def setupFiles(fileDict):

    oldFolders = []

    for key,data in fileDict.items():
        if(not os.path.isdir("Season "+data["season"])):
            os.mkdir("Season "+data["season"])
            if not data['path'] in oldFolders:
                oldFolders.append(data['path'])

        os.rename(os.path.join(data['path'],key),os.path.join(os.getcwd(),"Season "+data["season"],getNewEpName(data['season'],data['episode'],data['extension'])))  

    for folders in oldFolders:
        if not os.listdir(folders):
            os.rmdir(os.path.join(folders))  

#Sets metadata to a Plex media object
def setMetaData(baseObj,data):
    
    dataProps = ["title","summary","originallyAvailableAt"]
    unlocked = False
    metaData = {}
    if(len(data)==0):
        data = ["","",datetime(1999,1,1)]
        unlocked = True
    
    i=0
    for items in data:
        metaData[dataProps[i]+".value"] = items
        metaData[dataProps[i]+".locked"] = 0 if unlocked else 1
        i += 1

    baseObj.edit(**metaData)

#Remove all metadata and refresh
def resetMetadata(series):

    for season in series.seasons():
        setMetaData(season,[])
        for episode in season.episodes():
            setMetaData(episode,[])

##
#Helpers
##

#Build the episode name
def getNewEpName(season,episode,extension):
    return "One Piece (1999) - S"+season+"E"+episode+extension

#Add zero if only single digit
def prependZero(num):
    if(len(num.strip())<2):
        return '0'+num
    else:
        return num

#Get episode release date from an episode name and returns '1999-1-1' if there is no release date
def getDate(epName):

    timestamp = EPISODE_DICT.get(epName).get("release_date")
    if(timestamp):
        return datetime.fromtimestamp(timestamp/1000)
    else:
        return datetime(1999,1,1)

#Organize initiation functions
def initData():
    global CUR_DIR
    CUR_DIR = os.getcwd()
    getSeasons()
    getEpisodes()
    os.chdir('..')

##
#Main Function
##

if __name__ == '__main__':

    load_dotenv()
    initData()

    fileDict = organizeFiles()

    if (len(fileDict.items())<1):

        if(not HAS_VALID_FILE):
            print(STRINGS.noFiles)

        choice = input(STRINGS.noProcessedAdvance)

        if(not choice[0]=='y' and not choice=='Y'):
            print(STRINGS.exitMessage)
            exit(1)
    else:
        print(STRINGS.processSuccess)
        displayDict(fileDict)
        #Ask for input and rename files, make/check season folders and move files.
        user_choice = input(STRINGS.moveMessage)

        if(user_choice[0]=='y' or user_choice[0]=='Y'):
            setupFiles(fileDict)
            print(STRINGS.successMove)
        else:
            print(STRINGS.exitMessage)
            exit(1)

    #Load metadata from json
    metaData = {}

    with open(os.path.join(CUR_DIR,'onePieceMetaData.json'),'r') as f:
        metaData = json.load(f)
    
    
    #Connecting to Plex
    PLEX_HOST = os.getenv('PLEX_URL')
    PLEX_TKN = os.getenv('PLEX_TKN')

    plex = PlexServer(PLEX_HOST,PLEX_TKN)

    #Selecting One Piece
    tv_shows = plex.library.section('TV Shows')
    tv_shows.refresh()
    
    one_piece_name = tv_shows.search("One Piece")
    one_piece = None

    if(one_piece_name):
        one_piece = plex.fetchItem(one_piece_name[0].ratingKey)
    else:
        print(STRINGS.showNotFound)
        print(STRINGS.exitMessage)
        exit(1)

    resetMetadata(one_piece)
    tv_shows.refresh()
    
    #Updating Metadata
    for season in one_piece.seasons():
        
        #Extracting Season data
        match = re.match(SEASON_RE,season.title)
        eps = season.episodes()
        first_ep = None
        
        
        #Episode data is searched for retrieving the first episode's release date
        if(eps):
            first_ep = os.path.splitext(os.path.basename(eps[0].media[0].parts[0].file))

        #In case the episode is discovered
        if(match):
            seasonNum = match.group(1)

            #Update metadata
            setMetaData(season,[SEASON_DICT[seasonNum]["season_title"],SEASON_DICT[seasonNum]["season_summary"],getDate(first_ep[0])])

            #Upload the poster if a season poster is available
            if(SEASON_DICT[seasonNum]["season_image"]):
                season.uploadPoster(filepath=SEASON_DICT[seasonNum]["season_image"])

            print(STRINGS.metadataUpdated.format(DATA_NAME=season.title))

        for episode in eps:

            #Grab the episode name
            epName = os.path.splitext(os.path.basename(episode.media[0].parts[0].file))

            #Update episode metadata
            setMetaData(episode,[EPISODE_DICT[epName[0]]["title"],EPISODE_DICT[epName[0]]["summary"],getDate(epName[0])])

            print("\t"+STRINGS.metadataUpdated.format(DATA_NAME="".join(epName)))
    
    tv_shows.refresh()
    print(STRINGS.finalSuccess)