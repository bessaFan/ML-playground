// set visibility with javascript

(function() {
  var desktopSize = window.innerWidth > 980;

  var appContainer = document.getElementById('app-container');
  var pageLoader   = document.getElementById('page-loader');

  var animationDuration = 800;

  setTimeout(function() {
    if (desktopSize) {
      pageLoader.classList.add('stop');
    } else {
      scroll(animationDuration);
    }
  }, animationDuration);

  function scroll(scrollDuration) {
    var scrollHeight = appContainer.scrollHeight,
        scrollStep  = Math.PI / ( scrollDuration / 15 ),
        cosParameter = scrollHeight / 2;
    var scrollCount = 0,
        scrollMargin;

    requestAnimationFrame(step);

    function step () {
      setTimeout(function() {
        if (appContainer.scrollTop != scrollHeight / 2) {
          requestAnimationFrame(step);

          scrollCount = scrollCount + 1;
          scrollMargin = cosParameter - cosParameter * Math.cos( scrollCount * scrollStep );

          appContainer.scrollTop = scrollMargin;
        }
      }, 15 );
    }
  }
})();


