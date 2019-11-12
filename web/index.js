function py_video() {
  eel.video_feed()()
}

eel.expose(updateImageSrc);
function updateImageSrc(val) {
  $('.loading').hide();
  let elem = document.getElementById('bg');
  elem.src = "data:image/jpeg;base64," + val;
}
