eel.retrieve_images()()
  .then(data => {
    data.map(path => $("#image-gallery").append(
      "<div class='col-3 picture'>" +
        "<img src='./images/" + path + "' width='450'>" +
      "</div>"))
  })
  .catch(err => console.log(err))