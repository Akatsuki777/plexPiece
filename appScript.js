//This is the script to strip the data on episodes and seasons from the google sheet database of One Pace
function onOpen(){
  var ui = SpreadsheetApp.getUi();
  ui.createMenu("Extract Tool")
    .addItem('Extract Metadata','extractEpisodeName')
    .addSeparator()
    .addItem('Extract Season Data','extractSeasons')
    .addToUi();
}

function extractSeasons(){
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Arc Overview');

  var seasonSheet = ss.getSheetByName("Season Sheet");
  if(!seasonSheet){
    seasonSheet = ss.insertSheet("Season Sheet");
  }

  seasonSheet.getRange(1,1).setValue("Season Number");
  seasonSheet.getRange(1,2).setValue("Season Name");
  seasonSheet.getRange(1,3).setValue("Season Status");

  let sRow = 2;
  let row = 2

  while(parseFloat(sheet.getRange(row,1).getValue())&&sheet.getRange(row,2).getValue()){
    
    if(parseFloat(sheet.getRange(row,1).getValue())%1==0){
      seasonSheet.getRange(sRow,1).setValue(sheet.getRange(row,1).getValue());
      seasonSheet.getRange(sRow,2).setValue(sheet.getRange(row,2).getValue());
      let name = sheet.getRange(row,2).getValue();
      let match = name.match('\\(.*\\)');
      seasonSheet.getRange(sRow,2).setValue(name.replace(match?match[0]:"",""));
      seasonSheet.getRange(sRow,3).setValue(match?match[0]:"Completed");
      sRow++;
    } 
    row++;
  }
  
}

function extractEpisodeName(){

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheetList = ss.getSheets().slice(1,);

  var curSeasonEpCount = 0;

  var metaSheet = ss.getSheetByName("Meta");
  if(!metaSheet){
    metaSheet = ss.insertSheet("Meta");
  }
  var metaRow = 1;

  sheetList.map((sheet)=>{
    let row = 2;
    let seasonNum = getSeason(ss.getSheetByName('Arc Overview'),sheet.getName());

    if (seasonNum){
      while(sheet.getRange(row,2).getValue()!=""){
        let realEpisodes = sheet.getRange(row,4).getValue();
        realEpisodes = [...realEpisodes.matchAll('\\d+')];
        let episodeNum = sheet.getRange(row,2).getValue();
        
        //For single chapter seasons
        try{
          episodeNum = parseInt(episodeNum.match('\\d+')[0]);
        } catch(e){
          episodeNum = 1;
        }

        if(seasonNum%1!=0){
          seasonNum = Math.floor(seasonNum);
          episodeNum += curSeasonEpCount;
        } else {
          curSeasonEpCount = episodeNum;
        }
        
        switch (realEpisodes.length){
          case 1:
            realEpisodes = realEpisodes[0].toString();
            break;
          case 2:
            realEpisodes = realEpisodes[0].toString()+" - "+realEpisodes[1].toString();
            break;
          default:
            tmpString = '';
            realEpisodes.map((item)=>{
              tmpString+=item[0].toString()+","
            })
            realEpisodes=tmpString.slice(0,-1);
        }
        metaSheet.getRange(metaRow,1).setValue("".concat("One Pace S",prependZero(seasonNum),"E",prependZero(episodeNum)," - ",realEpisodes+'.mkv'));
        metaRow ++;
        row++;
      }
    }
  });

}

function getSeason(sheet,seasonName){
  let textFinder = sheet.getRange(1,2,sheet.getLastRow(),1).createTextFinder(seasonName);
  let match = textFinder.findAll();

  if (match.length>0){
    return sheet.getRange(match[0].getRow(),1).getValue();
  }
  return null;
}

function prependZero(item){
  if(parseInt(item)<10){
    return "0"+item.toString();
  } else {
    return item.toString();
  }
}