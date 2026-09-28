// Applies the external-links switch to a page mirrored from redis.io.
//
// Loaded by every mirrored page after /runtime-config.js (the chart's
// runtime config). The pages are redis.io's own Next.js build, so they carry
// no data-external-link attributes the way the documentation's templates do;
// links are classified here by where they lead instead:
//
//   - the documentation (/docs/latest/...) becomes this site's own path;
//   - a mirrored section, or "/", stays on this site;
//   - anything else on redis.io, or on another host, leaves the site.
//
// With externalLinks["marketing-offsite"] disabled -- the airgap default --
// a link that leaves the site is hidden when it is part of the page's frame
// (menus, footer, buttons) and turned into plain text inside prose, so no
// sentence loses a word. The page is never restructured: React owns this DOM,
// and removing nodes from under it breaks hydration.
(function () {
  var config = window.RUNTIME_CONFIG || {};
  var offsite = (config.externalLinks || {})['marketing-offsite'] || {};
  var offsiteEnabled = offsite.enabled !== false;
  var sections = ((config.mirror || {}).paths || []).concat(['glossary']);

  // Parts of redis.io's pages that only lead off the site: share buttons, the
  // "summarize with AI" prompts, the announcement bar, the cookie settings and
  // language selector, and footer columns left with nothing on this site.
  // Matched on the stable part of redis.io's CSS-module class names.
  var OUTWARD = [
    '*:has(> [class*="__shareTitle"])',
    '[class*="__aiPromptButtons"]',
    'body > [class*="__wrapper"]:has(a[class*="__button"])',
    '[class*="__sitemapGroup"]:not(:has(a[data-marketing-link="local"]))',
    '[class*="__cookiePreferencesButton"]',
    '[class*="__languageSelector"]'
  ];

  if (!offsiteEnabled) {
    var style = document.createElement('style');
    style.textContent = OUTWARD.join(',\n') + ' { display: none !important; }';
    document.head.appendChild(style);
  }

  function withSlash(path) {
    return path.charAt(path.length - 1) === '/' ? path : path + '/';
  }

  function isMirrored(path) {
    if (path === '/') return true;
    var candidate = withSlash(path);
    for (var i = 0; i < sections.length; i++) {
      if (candidate.indexOf('/' + sections[i] + '/') === 0) return true;
    }
    return false;
  }

  function isDirectory(path) {
    var last = path.split('/').pop();
    return last !== '' && last.indexOf('.') === -1;
  }

  function isFrame(link) {
    if (link.closest('p, td, blockquote, figcaption')) return false;
    if (/__button\b/.test(link.className || '')) return true;
    return !!link.closest('header, footer, nav, [role="dialog"]');
  }

  function hide(link) {
    (link.closest('li') || link).style.setProperty('display', 'none', 'important');
  }

  function unlink(link) {
    link.removeAttribute('href');
    link.style.setProperty('pointer-events', 'none');
    link.style.setProperty('color', 'inherit');
    link.style.setProperty('text-decoration', 'none');
  }

  function classify(link) {
    if (link.dataset.marketingLink) return;
    var raw = link.getAttribute('href');
    if (!raw || raw.charAt(0) === '#' || raw.indexOf('mailto:') === 0) return;
    var url;
    try { url = new URL(raw, location.href); } catch (e) { return; }

    var onRedisIo = url.hostname === 'redis.io' || url.hostname === 'www.redis.io';
    var here = url.origin === location.origin || onRedisIo;
    var path = url.pathname;
    if (here && path.indexOf('/en/') === 0) path = path.slice(3);
    var rest = url.search + url.hash;

    if (here && path.indexOf('/docs/latest/') === 0) {
      link.dataset.marketingLink = 'local';
      link.setAttribute('href', path.slice('/docs/latest'.length) + rest);
      return;
    }
    if (here && isMirrored(path)) {
      link.dataset.marketingLink = 'local';
      link.setAttribute('href', (isDirectory(path) ? withSlash(path) : path) + rest);
      return;
    }

    link.dataset.marketingLink = 'offsite';
    if (here) link.setAttribute('href', 'https://redis.io' + path + rest);
    if (offsiteEnabled) return;
    if (isFrame(link)) hide(link); else unlink(link);
  }

  function classifyWithin(root) {
    var links = root.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) classify(links[i]);
  }

  // Next.js navigates between pages by fetching them from its own server,
  // which does not exist here. A full page load always works.
  document.addEventListener('click', function (event) {
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link || link.target === '_blank') return;
    event.preventDefault();
    event.stopPropagation();
    location.assign(link.href);
  }, true);

  function start() {
    classifyWithin(document);
    new MutationObserver(function (records) {
      for (var i = 0; i < records.length; i++) {
        var added = records[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var node = added[j];
          if (node.nodeType !== 1) continue;
          if (node.matches('a[href]')) classify(node);
          classifyWithin(node);
        }
      }
    }).observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
