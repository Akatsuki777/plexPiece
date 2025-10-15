//PLEASE DO NOT USE THIS. 
//I WROTE IT LATE AT NIGHT AFTER LOOSING ALL MOTIVATION. 
//WOULD SOMEONE BE KIND ENOUGH TO IMPLEMENT THIS IS PYTHON API OF WIKIPEDIA
// Content from Wikipedia, licensed under CC BY-SA 4.0.

let baseURL = "https://en.wikipedia.org/wiki/One_Piece_season_";
let epMatch = /(.*)Transliteration:(.*)\(Japanese:(.*)\)/;
let dateMatch = /\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b/;
let printVal = {};

function makeUrls(baseURL){

    retVal = [];

    for(i=1;i<22;i++){
        retVal.push(baseURL+i.toString());
    }

    return retVal
}

function grabPageData(tableEl,link){

    var retVal = {}

    var epTable = [...tableEl.querySelectorAll(".vevent")];
    var descTable = tableEl.querySelectorAll(".expand-child")
    var allChildren = [...tableEl.children[0].children[0].children];
    var dateEl = null;

    allChildren.map((item)=>{
        if(item.innerText.includes("Original release date")){
            dateEl = item;
        }
    })

    let dateIndex = allChildren.indexOf(dateEl);

    epTable.map((item)=>{
        if(!item.querySelector(".summary")){
            item.remove();
        }
    })

    epTable = tableEl.querySelectorAll(".vevent");
    

    for(let i=0;i<descTable.length;i++){
        
        let titleArray = epTable[i].querySelector(".summary").innerText.replaceAll('\"',"").replaceAll('\n'," ").match(epMatch);
        let releaseDate = epTable[i].children[dateIndex].innerText;
        let dateMatched = releaseDate.match(dateMatch);
        
        if (!dateMatched){
            dateMatched = ['January 1, 1900'];
        }

        retVal[epTable[i].children[0].innerText] = {
            'title_eng': titleArray[1],
            'title_romanji': titleArray[2],
            'title_jap': titleArray[3],
            'release_date': new Date(dateMatched[0].replace(/\s+/g, ' ').trim()).getTime(),
            'summary': descTable[i].innerText.replace("\n","").trim()
        }
    }
    return retVal

}

var urlList = makeUrls(baseURL)

const promises = urlList.map((item, index) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      fetch(item)
        .then(response => response.text())
        .then(html => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          var dict = grabPageData(doc.querySelector('.wikitable'), item);
          Object.assign(printVal, dict);
          resolve();
        })
        .catch(error => {
          console.error(error);
          resolve(); 
        });
    }, index * 1000); 
  });
});

Promise.allSettled(promises).then(results=>{

    var textData = JSON.stringify(printVal);
    var textBlob = new Blob([textData],{type: 'text/plain;charset=utf-8'});

    var link = document.createElement("a");
    link.href = URL.createObjectURL(textBlob);
    link.download = "onePieceMetaData.json"
    
    link.click();
})
