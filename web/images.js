eel.retrieve_images()()
  .then(data => {
    data.map(path => $("#image-gallery").append(
      "<div class='col-3 picture'>" +
        "<img src='./images/" + path + "' style='width: 100%; height: 100%;'>" +
        "<div class='btn-group'>" +
          `<button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton${path}" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">` +
          '</button>' +
          `<div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton${path}">` +
            '<a class="dropdown-item" href="#">Save</a>' +
            '<a class="dropdown-item" href="#">Delete</a>' +
          '</div>' +
        "</div>" +
      "</div>"))
  })
  .catch(err => console.log(err))