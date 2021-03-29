var video = document.querySelector("#videoElement");
    
if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
    })
    .catch(function (err0r) {
      console.log("Something went wrong!");
    });
}
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.querySelector("#videoElement");

document.getElementById("clicker1").addEventListener("click", function() {
  context.drawImage(video, 0, 0, 500, 375);
});

document.getElementById("clicker2").addEventListener("click", function() {
  // get image data as string
  const imageString = canvas.toDataURL();

  // send image to server
  fetch('/show_map', {
    method: "POST",
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({
      imageString: imageString, 
    }),
  })
  window.location.href = "show_map"
});

async function uploadFile() {
  let formData = new FormData();           
  formData.append("file", fileupload.files[0]);
  await fetch('/savevideo', {
    method: "POST", 
    cache: "no-cache",
    credentials: "same-origin",
    body: formData
  });    
  alert('The file has been uploaded successfully.');
  window.location.href = "savevideo"
}

var webTitle          = $(".web-title");
var webTitleText      = $(".web-title h1");
var webContent        = $(".web-content");
var webBack           = $(".back-web");

var officeTitle       = $(".office-title");
var officeTitleText   = $(".office-title h1");
var officeContent     = $(".office-content");
var officeBack        = $(".back-office");

webTitle.click(function(){
  webTitle.css("z-index", "10");
  officeTitle.css("z-index", "0");
  webTitle.animate({width:"100%"}, 600);
  webTitle.animate({height:"20vh"}, 600);
  webTitleText.delay(600).animate({lineHeight:"20vh"}, 600);
  officeTitle.delay(600).fadeOut(600);
  webContent.delay(400).fadeIn(200);
  webBack.delay(1200).fadeIn("slow");
});

officeTitle.click(function(){
  officeTitle.css("z-index", "10");
  webTitle.css("z-index", "0");
  officeTitle.animate({width:"100%"}, 600);
  officeTitle.animate({height:"20vh"}, 600);
  officeTitleText.delay(600).animate({lineHeight:"20vh"}, 600);
  webTitle.delay(600).fadeOut(600);
  officeContent.delay(400).fadeIn(200);
  officeBack.delay(1200).fadeIn("slow");
});

webBack.click(function() {
  webBack.fadeOut("slow");
  webContent.delay(600).fadeOut(200);
  officeTitle.delay(600).fadeIn(200);
  webTitle.animate({height:"100vh"}, 600);
  webTitleText.animate({lineHeight:"100vh"}, 600);
  webTitle.animate({width:"50%"}, 600);
});

officeBack.click(function() {
  officeBack.fadeOut("slow");
  officeContent.delay(600).fadeOut(200);
  webTitle.delay(600).fadeIn(200);
  officeTitle.animate({height:"100vh"}, 600);
  officeTitleText.animate({lineHeight:"100vh"}, 600);
  officeTitle.animate({width:"50%"}, 600);
});