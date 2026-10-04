// Puts the documentation's header and footer on a page mirrored from
// redis.io, in place of redis.io's own.
//
// Loaded by every mirrored page from <head>, so redis.io's header and footer
// are hidden before the browser paints them: their links lead to pages this
// site does not have. The documentation's are read from this site's home page
// and shown in shadow roots, where the documentation's stylesheets cannot
// reach redis.io's page and redis.io's cannot reach them. They are kept for
// the rest of the browser session, so the next page shows them at once.
//
// Both hosts are children of <html>, outside the <body> React renders into.
// The header is fixed over the slot redis.io's 70px sticky header keeps (the
// page is laid out under it); the footer follows <body>, where redis.io's
// footer was.
//
// Without the home page -- an error, or no network -- redis.io's header and
// footer come back, and marketing-links.js still hides what leads off the site.
(function () {
  var CACHE_KEY = 'mirror:docs-frame:v1';
  var SEARCH_URL = '/#search';
  var REDIS_HEADER = 'body > header[class*="__header"]';
  var REDIS_FOOTER = 'body > footer[class*="__footer"]';

  var hiding = document.createElement('style');
  hiding.textContent =
    REDIS_HEADER + ', ' + REDIS_HEADER + ' * {' +
    ' visibility: hidden !important; pointer-events: none !important; }\n' +
    REDIS_FOOTER + ' { display: none !important; }';
  document.head.appendChild(hiding);

  function readCache() {
    try {
      return JSON.parse(sessionStorage.getItem(CACHE_KEY));
    } catch (e) {
      return null;
    }
  }

  function writeCache(parts) {
    try {
      sessionStorage.setItem(CACHE_KEY, JSON.stringify(parts));
    } catch (e) {
      // Storage full or blocked: the next page reads the home page again.
    }
  }

  function sameOriginStylesheets(doc) {
    var links = doc.querySelectorAll('link[rel="stylesheet"][href]');
    var hrefs = [];
    for (var i = 0; i < links.length; i++) {
      var url = new URL(links[i].getAttribute('href'), location.href);
      if (url.origin === location.origin) hrefs.push(url.pathname + url.search);
    }
    return hrefs;
  }

  function fontFaces(doc) {
    var styles = doc.querySelectorAll('style');
    var faces = [];
    for (var i = 0; i < styles.length; i++) {
      if (styles[i].textContent.indexOf('@font-face') !== -1) {
        faces.push(styles[i].textContent);
      }
    }
    return faces.join('\n');
  }

  function fetchText(url) {
    return fetch(url, { credentials: 'same-origin' }).then(function (response) {
      if (!response.ok) throw new Error(url + ': HTTP ' + response.status);
      return response.text();
    });
  }

  // The stylesheets were written for a whole document; in a shadow root the
  // document's :root is the host.
  function forShadowRoot(css) {
    return css.replace(/:root\b/g, ':host');
  }

  function readHomePage() {
    return fetchText('/').then(function (html) {
      var doc = new DOMParser().parseFromString(html, 'text/html');
      var header = doc.querySelector('body > header');
      var footer = doc.querySelector('body > footer');
      if (!header || !footer) throw new Error('the home page has no header or footer');
      return Promise.all(sameOriginStylesheets(doc).map(fetchText)).then(
        function (sheets) {
          return {
            header: header.outerHTML,
            footer: footer.outerHTML,
            css: forShadowRoot(sheets.join('\n')),
            fonts: fontFaces(doc)
          };
        }
      );
    });
  }

  // The same switch the documentation's own pages apply (external-links.html).
  function applyExternalLinks(root) {
    var links = (window.RUNTIME_CONFIG || {}).externalLinks || {};
    var marked = root.querySelectorAll('[data-external-link]');
    for (var i = 0; i < marked.length; i++) {
      var cfg = links[marked[i].getAttribute('data-external-link')];
      if (!cfg) continue;
      if (cfg.url) marked[i].setAttribute('href', cfg.url);
      if (cfg.enabled === false) {
        var target = marked[i].closest('[data-external-card]') ||
          marked[i].closest('li') || marked[i];
        target.style.setProperty('display', 'none', 'important');
      }
    }
  }

  // The header's own buttons: the mobile menu opens in place; search opens
  // the documentation's search, which lives on its pages, not on this one.
  function wireHeaderButtons(root) {
    var toggle = root.querySelector('[data-menu-toggle]');
    var menu = root.querySelector('[data-menu]');
    if (toggle && menu) {
      toggle.addEventListener('click', function () {
        var open = menu.classList.toggle('hidden') === false;
        toggle.setAttribute('aria-expanded', String(open));
      });
    }
    var searches = root.querySelectorAll('#search-button, #search-button-mobile');
    for (var i = 0; i < searches.length; i++) {
      searches[i].addEventListener('click', function () {
        location.assign(SEARCH_URL);
      });
    }
  }

  function shadowHost(name, position, parts, markup) {
    var host = document.createElement('div');
    host.setAttribute(name, '');
    host.style.cssText = 'all: initial; display: block; ' + position;
    var root = host.attachShadow({ mode: 'open' });
    var style = document.createElement('style');
    style.textContent = parts.css;
    root.appendChild(style);
    var holder = document.createElement('div');
    holder.innerHTML = markup;
    while (holder.firstChild) root.appendChild(holder.firstChild);
    applyExternalLinks(root);
    return host;
  }

  function mount(parts) {
    if (parts.fonts) {
      var faces = document.createElement('style');
      faces.textContent = parts.fonts;
      document.head.appendChild(faces);
    }
    var header = shadowHost(
      'data-docs-header',
      'position: fixed; top: 0; left: 0; right: 0; z-index: 2147483000;',
      parts,
      parts.header
    );
    wireHeaderButtons(header.shadowRoot);
    var hosts = [header, shadowHost('data-docs-footer', '', parts, parts.footer)];
    // React owns <html> once it hydrates, and drops the children it did not
    // render; each is put back as soon as it goes.
    function attach() {
      for (var i = 0; i < hosts.length; i++) {
        if (!hosts[i].isConnected) document.documentElement.appendChild(hosts[i]);
      }
    }
    attach();
    new MutationObserver(attach).observe(document.documentElement, { childList: true });
  }

  function restoreRedisFrame(error) {
    if (window.console) console.warn('docs-frame:', error);
    if (hiding.parentNode) hiding.parentNode.removeChild(hiding);
  }

  var cached = readCache();
  if (cached) {
    mount(cached);
    return;
  }
  readHomePage().then(function (parts) {
    writeCache(parts);
    mount(parts);
  }).catch(restoreRedisFrame);
})();
