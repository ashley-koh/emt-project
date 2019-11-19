let currentPage = 'video-page';

function py_video() {
  eel.video_feed()()
}

eel.expose(updateImageSrc);
function updateImageSrc(val) {
  $('.loading').hide();
  $('.video-page').css('visibility', 'visible');
  let elem = document.getElementById('bg');
  elem.src = "data:image/jpeg;base64," + val;
  $('#bg')
    .css('width', '70%')
    .css('height', 'auto')
    .css('border-radius', '5px')
    .css('border', '1px solid #333');
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