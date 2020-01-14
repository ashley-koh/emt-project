let config = {}
let curIndex = 0;

function get_config() {
  eel.get_config()()
    .then( res =>{
      config = res 
      console.log(config)

      let { maxWhite, brightness, threshold, size, dot, noise } = config[0];

      $('#maxWhite').val(maxWhite);
      $('#brightness').val(brightness);
      $('#canny').val(threshold);
      $('#size').val(size);
      $('#dot').val(dot);
      $('#noise').val(noise);
    })
    .catch(err => console.log(err))
} 

function updateConfig() {

  let curConfig = {
    'maxWhite': parseInt($('#maxWhite').val()),
    'brightness': parseInt($('#brightness').val()),
    'threshold': parseInt($('#canny').val()),
    'size': parseInt($('#size').val()),
    'dot': parseInt($('#dot').val()),
    'noise': parseInt($('#noise').val())
  }

  console.log(curConfig)

  eel.update_config(curConfig);

  $('#updated-config-toast').toast('show')
}
