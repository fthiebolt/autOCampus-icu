/*jshint expr: true*/ // prevent error in ...be.a.Function

describe('loadimages', function () {

  var src = 'assets/img.png';

  it('should load single image', function (done) {
    loadimages(src, function (err, img) {
      // True src is absolute path. Compare that relative part match
      expect(img.src).to.have.string(src);
      done();
    });
  });

  it('should load single array image', function (done) {
    loadimages([src], function (err, img) {
      expect(img.length).equal(1);
      expect(img[0].src).to.have.string(src);
      done();
    });
  });

  it('should throw error if no callback given', function () {
    expect(function () {
      loadimages(src);
    }).to.throw(Error, /callback/);
  });

  it('should force consistent execution order', function (done) {
    var cacheFlag = false;

    // Image should not be in the cache yet.

    loadimages(src, function (err, img) {
      expect(cacheFlag).equal(true);

      // Now the image is loaded and in the cache.
      // We ensure that execution order remains the same.
      var cacheFlag2 = false;

      loadimages(src, function (err, img2) {
        expect(cacheFlag2).equal(true);

        done();
      });

      cacheFlag2 = true;
    });

    cacheFlag = true;
  });
});
