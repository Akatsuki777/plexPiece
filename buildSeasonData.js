var els = document.querySelectorAll("h4");
const seasonList = ['Romance Dawn', 'Orange Town', 'Syrup Village', 'Baratie', 'Arlong Park', 'Loguetown', 'Reverse Mountain', 'Whisky Peak ', 'Little Garden', 'Drum Island', 'Arabasta', 'Jaya', 'Skypiea', 'Long Ring Long Land ', 'Water Seven', 'Enies Lobby', 'Post-Enies Lobby ', 'Thriller Bark  ', 'Sabaody Archipelago ', 'Amazon Lily ', 'Impel Down ', 'Marineford', 'Post-War', 'Return to Sabaody', 'Fishman Island ', 'Punk Hazard ', 'Dressrosa ', 'Zou ', 'Whole Cake Island', 'Reverie', 'Wano ', 'Egghead '];

let output = {};


[...els].slice(0,-4).map((item,index)=>{
    output[(index<3)?index+1:index+2] = {
        "title": seasonList[index],
        "summary": item.nextElementSibling.innerText.replaceAll('\"','"')
    };
})

var jsonOutput = JSON.stringify(output);
var blob = new Blob([jsonOutput],{type:'application/json'})

var link = document.createElement("a");
link.href = URL.createObjectURL(blob);
link.download = "onePieceSeasonData.json";


link.click();