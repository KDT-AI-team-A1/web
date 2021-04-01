var video = document.querySelector("#videoElement");
var video2 = document.querySelector("#videoElement2");
  
if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
      video2.srcObject = stream;
    })
    .catch(function (err0r) {
      console.log("Something went wrong!");
    });
}
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

document.getElementById("clicker1").addEventListener("click", function() {
  context.drawImage(video, 0, 0, 500, 375);
});

document.getElementById("clicker2").addEventListener("click", function() {
  // get image data as string
  const imageString = canvas.toDataURL();

  // send image to server
  let url = "check_no_mask";
  $.post('/'+url,
        JSON.stringify({imageString: imageString}),
        function(data){
          console.log(data);

          bboxDraw(context, data);

          alert(data.msg);
          
          if (data.url) {
            window.location.href = data.url
          }
        },
        "json"
  )
});

var canvas2 = document.getElementById('canvas2');
var context2 = canvas2.getContext('2d');
var captureTime = 1000;

document.getElementById("clicker3").addEventListener("click", function() {
  startAlert = setInterval(function() {
    context2.drawImage(video2, 0, 0, 500, 375);

    const imageString = canvas2.toDataURL();

    let url = 'alert_no_mask';
    $.post('/'+url,
          JSON.stringify({imageString: imageString}),
          function(data){
            console.log(data);
            const element = document.getElementById('result-in');
            element.innerHTML = '<p>' + '현재 카운트 : ' + data.nm_cnt + '<br> 알람 역치 : ' + data.nm_cntMax + '</p>';

            for(var idx=0; idx < data.boxes.length; idx++) {
              if (data.classes[idx]) {
                context2.strokeStyle = 'red';
              }
              else {
                context2.strokeStyle = 'green';
              }
              context2.lineWidth = 5;
              const width1 = data.boxes[idx][2] - data.boxes[idx][0]
              const hieght1 = data.boxes[idx][3] - data.boxes[idx][1]
              const x = data.boxes[idx][0]
              const y = data.boxes[idx][1]
              context2.strokeRect(x,y,width1,hieght1);
            }

            if (data.isAlert) {
              alert("마스크 미착용 안내방송")
            }
          },
          "json"
    );
  }, captureTime);

});

document.getElementById("clicker4").addEventListener("click", function() {
  alert('종료');
  clearInterval(startAlert);
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
  alert('파일이 성공적으로 업로드되었습니다');
  window.location.href = "savevideo"
}

function bboxDraw(context, data) {
  for(var idx=0; idx < data.boxes.length; idx++) {
    if (data.classes[idx]) {
      context.strokeStyle = 'red';
    }
    else {
      context.strokeStyle = 'green';
    }
    context.lineWidth = 5;
    const width1 = data.boxes[idx][2] - data.boxes[idx][0]
    const hieght1 = data.boxes[idx][3] - data.boxes[idx][1]
    const x = data.boxes[idx][0]
    const y = data.boxes[idx][1]
    context.strokeRect(x,y,width1,hieght1);
  }
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