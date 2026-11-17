// Sends links to GitHub repositories to their internal GitLab copies.
//
// Reads window.RUNTIME_CONFIG.gitMirrors, a list of
//   { name, repos: ["owner/name", ...], to: "<GitLab project URL>" }
// built by templates/configmap-runtime.yaml from files/external-links.yaml
// and values.externalLinks.gitMirrors. Only enabled entries with a `to` reach
// the browser.
//
// A link is rewritten only when its owner/name equals one of an entry's repos,
// case-insensitively. Links to pages GitLab copies do not have (pull requests,
// issues, wiki, ...) are left on GitHub. Links added to the page later, by
// scripts, are rewritten too.
//
// Under Node (the tests) the file exports createTranslator and touches no DOM.
(function (root) {
  'use strict';

  var GITHUB_URL = /^https?:\/\/(?:www\.)?github\.com\/([^\/?#]+)\/([^\/?#]+)(.*)$/i;
  var RAW_FILE_URL = /^https?:\/\/raw\.githubusercontent\.com\/([^\/?#]+)\/([^\/?#]+)\/(.+)$/i;
  var FULL_REF_PREFIX = /^refs\/(?:heads|tags)\//;
  var GITHUB_LINE_RANGE = /^#L(\d+)-L(\d+)$/;
  var PAGES_UNDER_DASH = {
    blob: true, tree: true, raw: true, blame: true, commits: true,
    commit: true, tags: true, compare: true, branches: true
  };

  function repoKey(owner, name) {
    return (owner + '/' + name.replace(/\.git$/i, '')).toLowerCase();
  }

  function indexMirrors(mirrors) {
    var targetByRepo = {};
    (mirrors || []).forEach(function (mirror) {
      var target = String(mirror.to || '').replace(/\/+$/, '');
      if (!target) return;
      (mirror.repos || []).forEach(function (repo) {
        targetByRepo[String(repo).toLowerCase()] = target;
      });
    });
    return targetByRepo;
  }

  function splitQueryAndFragment(rest) {
    var cut = rest.search(/[?#]/);
    if (cut === -1) return { path: rest, tail: '' };
    return { path: rest.slice(0, cut), tail: rest.slice(cut) };
  }

  function translateLineRange(tail) {
    return tail.replace(GITHUB_LINE_RANGE, '#L$1-$2');
  }

  function translateReleasesPath(segments) {
    var kind = segments[1];
    if (!kind) return '/-/releases';
    if (kind === 'tag' && segments[2]) return '/-/tags/' + segments.slice(2).join('/');
    if (kind === 'latest' && segments.length === 2) return '/-/releases/permalink/latest';
    if (kind === 'download' && segments.length >= 4) {
      return '/-/releases/' + segments[2] + '/downloads/' + segments.slice(3).join('/');
    }
    return null;
  }

  // Returns the GitLab path for a GitHub repository path, or null when GitLab
  // has no copy of that page.
  function translateRepoPath(path) {
    if (path === '' || path === '/') return '';
    var segments = path.slice(1).split('/');
    var page = segments[0];
    if (PAGES_UNDER_DASH[page]) return '/-' + path;
    if (page === 'releases') return translateReleasesPath(segments);
    return null;
  }

  function translateGitHubLink(match, targetByRepo) {
    var target = targetByRepo[repoKey(match[1], match[2])];
    if (!target) return null;
    var parts = splitQueryAndFragment(match[3]);
    var path = translateRepoPath(parts.path);
    if (path === null) return null;
    return target + path + translateLineRange(parts.tail);
  }

  function translateRawFileLink(match, targetByRepo) {
    var target = targetByRepo[repoKey(match[1], match[2])];
    if (!target) return null;
    return target + '/-/raw/' + match[3].replace(FULL_REF_PREFIX, '');
  }

  function createTranslator(mirrors) {
    var targetByRepo = indexMirrors(mirrors);
    return function translate(href) {
      if (!href) return null;
      var github = GITHUB_URL.exec(href);
      if (github) return translateGitHubLink(github, targetByRepo);
      var raw = RAW_FILE_URL.exec(href);
      if (raw) return translateRawFileLink(raw, targetByRepo);
      return null;
    };
  }

  function rewriteAnchor(anchor, translate) {
    var rewritten = translate(anchor.getAttribute('href'));
    if (rewritten !== null) anchor.setAttribute('href', rewritten);
  }

  function rewriteWithin(node, translate) {
    if (node.nodeType !== 1) return;
    if (node.matches('a[href]')) rewriteAnchor(node, translate);
    var anchors = node.querySelectorAll('a[href]');
    for (var i = 0; i < anchors.length; i++) rewriteAnchor(anchors[i], translate);
  }

  function watchDocument(document, translate) {
    rewriteWithin(document.documentElement, translate);
    if (typeof MutationObserver === 'undefined') return;
    new MutationObserver(function (records) {
      records.forEach(function (record) {
        if (record.type === 'attributes') {
          rewriteWithin(record.target, translate);
          return;
        }
        record.addedNodes.forEach(function (added) { rewriteWithin(added, translate); });
      });
    }).observe(document.documentElement, {
      childList: true, subtree: true, attributes: true, attributeFilter: ['href']
    });
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { createTranslator: createTranslator };
    return;
  }

  var mirrors = (root.RUNTIME_CONFIG && root.RUNTIME_CONFIG.gitMirrors) || [];
  if (mirrors.length === 0) return;
  var translate = createTranslator(mirrors);
  if (root.document.readyState === 'loading') {
    root.document.addEventListener('DOMContentLoaded', function () {
      watchDocument(root.document, translate);
    });
  } else {
    watchDocument(root.document, translate);
  }
})(this);
