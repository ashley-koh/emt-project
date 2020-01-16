let currentPage = 'video-page';
let status = "Initializing";

let config = {}
let colourData = {}

let selectedColour = 'blue';

function py_video() {
  eel.get_data()()
    .then(res => {
      colourData = res.colour;
      config = res.config;
    })
    .then(res => {
      eel.video_feed()()
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
      $('.status .stick-status').html(status)
    })
    .catch(err => console.log(err))

  eel.get_colour()()
    .then(colour => {

      let ranges = colourData[selectedColour];

      if (colour[0] > ranges.lower.b && colour[0] < ranges.upper.b) {
        if (colour[1] > ranges.lower.g && colour[1] < ranges.upper.g) {
          if (colour[2] > ranges.lower.r && colour[2] < ranges.upper.r) {
            $('.stick-colour').text("True")
          } else {
            $('.stick-colour').text("NG")
          }
        } else {
          $('.stick-colour').text("NG")
        }
      } else {
        $('.stick-colour').text("NG")
      }
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

function selectColour() {
  selectedColour = $('#colourSelect').val()
}