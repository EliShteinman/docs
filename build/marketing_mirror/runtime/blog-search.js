// The blog's search page, /blog/search/?s=<words> (build/marketing_mirror/blog_search.py).
//
// The page is the blog index with its Next.js scripts removed, so nothing
// hydrates it and this script owns the post list. It asks this site's search
// service for blog posts only, and draws each as a copy of the page's own first
// row, filled from _mirror/blog-posts.json (date, categories, authors).
(function () {
  var SEARCH = '/convai/api/search-service';
  var POSTS = '/_mirror/blog-posts.json';
  var LIMIT = 100;
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  // A CSS-module class ends in "__<name>"; matching that exactly keeps
  // "title" from finding "titleCol" and "author" from finding "authorsCol".
  function part(root, name) {
    var exact = new RegExp('__' + name + '(\\s|$)');
    var candidates = root.querySelectorAll('[class*="__' + name + '"]');
    for (var i = 0; i < candidates.length; i++) {
      if (exact.test(candidates[i].className)) return candidates[i];
    }
    return null;
  }

  function formatDate(iso) {
    var bits = (iso || '').split('-');
    if (bits.length !== 3) return iso || '';
    return MONTHS[parseInt(bits[1], 10) - 1] + ' ' + bits[2] + ',' + bits[0];
  }

  function withSlash(url) {
    var path = url.split('?')[0].split('#')[0];
    return path.charAt(path.length - 1) === '/' ? path : path + '/';
  }

  function fillRow(template, url, title, post) {
    var row = template.cloneNode(true);
    row.removeAttribute('style');
    var link = part(row, 'linkOverlay');
    link.setAttribute('href', url);
    link.setAttribute('aria-label', title);
    part(row, 'title').textContent = title;

    var authors = part(row, 'authorsCol');
    var sample = part(authors, 'author');
    authors.innerHTML = '';
    ((post && post.authors) || []).forEach(function (author) {
      if (!sample || !author.image) return;
      var copy = sample.cloneNode(true);
      var img = copy.querySelector('img');
      img.setAttribute('src', author.image);
      img.removeAttribute('srcset');
      img.setAttribute('alt', author.name);
      img.style.backgroundImage = 'none';
      authors.appendChild(copy);
    });

    var categories = part(row, 'categoryCol');
    var chip = part(categories, 'chip');
    categories.innerHTML = '';
    ((post && post.categories) || []).slice(0, 1).forEach(function (name) {
      var copy = chip.cloneNode(true);
      copy.querySelector('span').textContent = name;
      categories.appendChild(copy);
    });

    var date = part(row, 'dateCol');
    date.querySelector('span').textContent = formatDate(post && post.date);
    return row;
  }

  function message(feed, text) {
    var note = document.createElement('p');
    note.textContent = text;
    note.style.padding = '2rem 0';
    feed.appendChild(note);
  }

  // Next.js animates much of the page in from opacity 0; with no React here
  // nothing would ever animate it back.
  function revealStatic() {
    var style = document.createElement('style');
    style.textContent = '[style*="opacity:0"] { opacity: 1 !important; transform: none !important; }';
    document.head.appendChild(style);
  }

  function start() {
    revealStatic();
    var words = (new URLSearchParams(location.search).get('s') || '').trim();
    var feed = part(document, 'feed');
    var first = feed && part(feed, 'BlogFeedCard');
    if (!feed || !first) return;
    var template = first.parentElement;

    ['featuredPostSection', 'loadingContainer'].forEach(function (name) {
      var el = part(document, name);
      if (el) el.remove();
    });
    feed.innerHTML = '';

    var input = document.querySelector('input[name="Search"]');
    if (input) {
      input.value = words;
      input.form.addEventListener('submit', function (event) {
        event.preventDefault();
        var next = input.value.trim();
        if (next.length >= 2) location.assign('/blog/search/?s=' + encodeURIComponent(next));
      });
    }
    if (words.length < 2) return message(feed, 'Enter at least 2 characters to search the blog.');

    var query = SEARCH + '?q=' + encodeURIComponent(words) + '*&p=all&source=blog&limit=' + LIMIT;
    Promise.all([
      fetch(query).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }),
      fetch(POSTS).then(function (r) { return r.ok ? r.json() : {}; })
    ]).then(function (answers) {
      var results = answers[0].results || [];
      var posts = answers[1];
      if (!results.length) return message(feed, 'No blog posts found for "' + words + '".');
      results.forEach(function (result) {
        var url = withSlash(result.url);
        var title = (result.title || '').replace(/<[^>]+>/g, '');
        feed.appendChild(fillRow(template, url, title, posts[url]));
      });
    }).catch(function () {
      message(feed, 'Search is not available on this site.');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
