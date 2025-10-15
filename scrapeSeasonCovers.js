var elements = [...document.querySelector(".grid-cols-2").children];
const script = document.createElement("script");
script.src = "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js";
document.head.appendChild(script);

var urlRe = '.*url=(.*)';

var imageUrls = [];

elements.map((item)=>{
    var link = decodeURIComponent(item.querySelector("img").getAttribute("src").match(urlRe)[1]);
    imageUrls.push(link);
})

const zip = new JSZip();
let completed = 0;

imageUrls.map((item,index)=>{

    fetch(item)
    .then(res => res.blob())
    .then(blob =>{
        const fileName = "One Piece (1999) - Season Cover - "+ (index-1).toString() + ".jpg";
        console.log("Fetching image "+fileName);
        zip.file(fileName,blob);
        completed++;

        if (completed==imageUrls.length){
            zip.generateAsync({type: "blob"}).then(
                zipBlob => {
                    const link = document.createElement("a");
                    link.href = URL.createObjectURL(zipBlob);
                    link.download = "One_Piece_Cover_Images.zip";
                    link.click();
                }
            )
        }
    }).catch(err => console.log("failed to download",item,err));
});