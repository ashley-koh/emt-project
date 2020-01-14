let config = {}
let curIndex = 0;

let colour = {
  blue: {
    lower: { b: 0, g: 0, r: 0, },
    upper: { b: 0, g: 0, r: 0 }
  },

  purple: {
    lower: { b: 0, g: 0, r: 0, },
    upper: { b: 0, g: 0, r: 0 }
  },

  orange: {
    lower: { b: 0, g: 0, r: 0, },
    upper: { b: 0, g: 0, r: 0 }
  },

  red: {
    lower: { b: 0, g: 0, r: 0, },
    upper: { b: 0, g: 0, r: 0 }
  },

  yellow: {
    lower: { b: 0, g: 0, r: 0, },
    upper: { b: 0, g: 0, r: 0 }
  },

  green: {
    lower: { b: 0, g: 0, r: 0, },
    upper: { b: 0, g: 0, r: 0 }
  },
}

function get_data() {
  eel.get_data()()
    .then( res =>{
      config = res.config
      colour = res.colour
      console.log(config)
      console.log(colour)

      let { maxWhite, brightness, threshold, size, dot, noise } = config[0];

      $('#maxWhite').val(maxWhite);
      $('#brightness').val(brightness);
      $('#canny').val(threshold);
      $('#size').val(size);
      $('#dot').val(dot);
      $('#noise').val(noise);

      Object.keys(colour).map(colourName => {
        $(`#${colourName}-lower-B`).val(colour[colourName].lower.b)
        $(`#${colourName}-lower-G`).val(colour[colourName].lower.g)
        $(`#${colourName}-lower-R`).val(colour[colourName].lower.r)
        $(`#${colourName}-upper-B`).val(colour[colourName].upper.b)
        $(`#${colourName}-upper-G`).val(colour[colourName].upper.g)
        $(`#${colourName}-upper-R`).val(colour[colourName].upper.r)
      })

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

function updateColour(colourName) {

  colour[colourName] = {

    lower: {
      b: parseInt($(`#${colourName}-lower-B`).val()),
      g: parseInt($(`#${colourName}-lower-G`).val()),
      r: parseInt($(`#${colourName}-lower-R`).val()),
    },

    upper: {
      b: parseInt($(`#${colourName}-upper-B`).val()),
      g: parseInt($(`#${colourName}-upper-G`).val()),
      r: parseInt($(`#${colourName}-upper-R`).val()),
    }
  }

  console.log(colour)

  eel.update_colour(colour)
  
  $('#updated-colour-toast').toast('show')

}