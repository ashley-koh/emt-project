eel.retrieve_images()()
  .then(data => {
    data.map(path => $("#image-gallery").append(
      "<div class='col-sm'>" +
        "<img src='./images/" + path + "' height='250'>" +
      "</div>"))
  })
  .catch(err => console.log(err))