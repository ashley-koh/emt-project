let currentPage = 'video-page';
let status = "Initializing";

let config = {}
let colour = {}

function py_video() {
  eel.video_feed()()
  eel.get_data()()
    .then(res => {
      config = res.config
      colour = res.colour
    })
}

eel.expose(updateImageSrc);
function updateImageSrc(val) {
  $('.loading').hide();
  $('.video-page').css('visibility', 'visible');
  let elem = document.getElementById('bg');
  elem.src = "data:image/jpeg;base64," + val;
  $('#bg')
    .css('width', '100%')
    .css('height', 'auto')
    .css('border-radius', '5px')
    .css('border', '1px solid #333');

  eel.get_status()()
    .then(status => {
      console.log(status)
      $('.status .stick-status').html(status)
    })
    .catch(err => console.log(err))
}

let captureActive = true;

$(window).keypress(function(e) {
  if (e.key === ' ') {
    if (captureActive) {
      eel.stop_video_feed();
      captureActive = false;
    } else {
      eel.restart_video_feed();
      captureActive = true;
    }
  }
});

$(window).keypress(function(e) {
  let number = e.key

  if (number === '1' || number === '2' || number === '3' || number === '4')
    eel.select_frame(parseInt(number) - 1)
})