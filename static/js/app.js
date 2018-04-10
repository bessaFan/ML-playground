// set visibility with javascript

(function() {
  var desktopSize = window.innerWidth > 980;

  var appContainer = document.getElementById('app-container');
  var pageLoader   = document.getElementById('page-loader');

  var animationDuration = 800;
  var bbox, radii, svg, target;

  svg = d3.select('svg');
  bbox = svg[0][0].getBoundingClientRect
  radii = [12, 24, 32, 48, 60, 80, 120, 210];
  target = svg.append('g').attr('transform', "translate(" + (bbox.width / 2) + "," + (bbox.height / 2) + ")");
  target.selectAll('circle').data(radii).enter().append('circle').attr('r', function(d) {return d;});

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
}

)();



