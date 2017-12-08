#
# Install: sudo pip install flask
# Run: python -m flask run  --host=0.0.0.0
# Inspiration from: https://onepagelove.com/isis-cocco
#

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return """

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Isis Cocco</title>

  <meta charset="utf-8">
  <meta content="width=device-width,initial-scale=1,maximum-scale=1,initial-scale=1,shrink-to-fit=no" name="viewport">

  <meta name="msapplication-TileColor" content="#FAFAFA">
  <meta name="theme-color" content="#FAFAFA">
  <meta name="format-detection" content="telephone=no">
  <meta name="apple-mobile-web-app-status-bar-style" content="white-translucent" />
  <meta name="apple-mobile-web-app-capable" content="yes">

  <meta name="description" content="A product designer based in London.">
  <meta name="application-name" content="Isis Cocco">

  <meta property="og:locale" content="en_GB">
  <meta property="og:title" content="Isis Cocco">
  <meta property="og:description" itemprop="description" content="A product designer based in London.">
  <meta property="og:site_name" content="Isis Cocco">
  <meta property="og:url" content="https://isiscocco.com">
  <meta property="og:image" content="https://isiscocco.com/ogimage.jpg">
  <meta property="og:type" content="website">

  <meta name="twitter:title" content="Isis Cocco">
  <meta name="twitter:description" content="">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="Isis Cocco">
  <meta name="twitter:creator" content="sisi_maia88">
  <meta name="twitter:url" content="https://isiscocco.com">
  <meta name="twitter:image" content="https://isiscocco.com/ogimage.jpg">

  <link rel="icon" type="image/png" href="favicon.png">
  <link rel='stylesheet' href='https://d33wubrfki0l68.cloudfront.net/css/27dd7a77c1056ecf77c70cb16c52c87d2cdee867/styles.css'/>

  <script>
    (function (i, s, o, g, r, a, m) {
      i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
        (i[r].q = i[r].q || []).push(arguments)
      }, i[r].l = 1 * new Date(); a = s.createElement(o),
        m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
    })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');
    ga('create', 'UA-49205356-1', 'auto');
    ga('set', 'anonymizeIp', true);
    ga('send', 'pageview');
  </script>
</head>

<body>

  <div class="content">
    <h1 class="title">Bessa Fan</h1>
    <p class="bio">A product designer based in Toronto.</p>
    <ul class="links">
      <li class="links__item">
        <a href="mailto:hello@isiscocco.com">hello at isiscocco dot com</a>
      </li>
      <li class="links__item">
        <a href="https://www.linkedin.com/in/isis-cocco-a52a521a" target="_blank" rel="noopener noreferrer">linkedin</a>
      </li>
    </ul>
  </div>

</body>

</html>

    """

if __name__ == "__main__":
    app.run()
