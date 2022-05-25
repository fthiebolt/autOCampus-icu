module.exports = function loadimages(imgSrcs, then) {
  // Parameters
  //   imgSrcs
  //     array of image source paths OR single source path string.
  //   then(err, imgElements)
  //     Will be called after all the images are loaded. If string was given,
  //     imgElements is an Image instead of array of Images.

  var numberOfImages, stringGiven, thereWasSuccess, thereWasError, imgs;
  var onloadsCalled, onload, onerror;

  if (typeof then !== 'function') {
    throw new Error('callback should be a function: ' + then);
  }

  if (typeof imgSrcs === 'string') {
    numberOfImages = 1;
    stringGiven = true;
    imgSrcs = [imgSrcs]; // Normalize
  } else {
    // Array of images
    numberOfImages = imgSrcs.length;
    stringGiven = false;
  }
  thereWasSuccess = false;
  thereWasError = false;

  imgs = [];

  onloadsCalled = 0;
  onload = function () {
    // Note:
    //   this = Image
    if (!thereWasError) {
      onloadsCalled += 1;
      var isFinalImage = (onloadsCalled === numberOfImages);
      if (isFinalImage) {
        thereWasSuccess = true;
        if (stringGiven) {
          then(null, imgs[0]);
        } else {
          then(null, imgs);
        }
      }
    }
  };

  onerror = function (errMsg) {
    // Note:
    //   this = Image

    // No errors after success.
    if (!thereWasSuccess) {
      thereWasError = true;
      then(errMsg, null);
    }

    // Prevent firing the default event handler
    // https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers.onerror#Parameters
    return true;
  };

  for (i = 0; i < imgSrcs.length; i += 1) {
    imgs.push(new Image());
    imgs[i].onload = onload;
    imgs[i].onabort = onerror;
    imgs[i].onerror = onerror;
    imgs[i].src = imgSrcs[i];
  }
};
