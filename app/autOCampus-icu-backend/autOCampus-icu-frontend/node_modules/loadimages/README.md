# loadimages

This is a JavaScript micro-library for **preloading images** before use. The preloading allows you to read image.width, image.height, and other properties consistently without caring if the browser has cached the images or not. Simply: give the function `loadimages` one or multiple image URLs and a callback function. The callback will be called after all the images are downloaded, cached, and their properties ready to use. If any of the images fail to load, an error is given to the callback.

Based on [load-images](https://www.npmjs.com/package/load-images). The main difference is that where load-images always returns a map, we return an array of images if an array of URLs was given, and a single image if a single URL was given.



## Install

    $ npm install loadimages

If you need a stand-alone bundle to be used without browserify or webpack, run `$ npm run build:bundle`.



## Usage

    var loadimages = require('loadimages');

    // Load single image
    loadimages('img/lego.png', function (err, image) {
      // Loading errors might occur, e.g. if the image was not found (404).
      if (err) { throw err; }
      // do stuff with your freshly loaded HTMLImageElement
      image.style.margin = '1.618em';
      document.body.appendChild(image);
    });

    // Load multiple images in parallel
    var srcs = ['img/lego.png', 'http://i.imgur.com/Hbtar04.jpg'];
    loadimages(srcs, function (err, images) {
      // Non-null error is given if any of the images failed to load.
      if (err) { throw err; }
      // Now you have an array of images to do stuff with:
      var lego = images[0];
      var stephen = images[1];
      ...
    });



## For developers

Run lint & build browserify bundle & run unit tests:

    $ npm run build



## Versioning

[Semantic Versioning 2.0.0](http://semver.org/)



## License

[MIT License](../blob/master/LICENSE)
