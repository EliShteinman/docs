// cli.js — docs-site entry point for the interactive redis-cli widget.
//
// Thin shim, intentionally tiny. The widget's logic is owned and served by the
// /cli backend at https://redis.io/cli/static/js/cli.js; upstream keeps NO copy
// of it so the docs renderer can never drift from the backend's (the class of
// bug that once left a stale copy without a $status case).
//
// Airgap fork: that redis.io URL is unreachable in a disconnected deployment, so
// the fork VENDORS the canonical script at /cli-playground/assets/cli.js (the
// same copy the playground uses) and this shim loads it from there. Both the
// apiUrl and the script.src therefore point at in-cluster paths, not redis.io.
// Because upstream no longer tracks the widget in git, the vendored copy must be
// re-checked against the canonical one on every image rebuild — see
// build/check_cli_js_drift.py and the feedback_cli_js_vendored_drift_check memory.
//
// This shim just:
//   1. sets window.REDIS_CLI_CONFIG with the docs overrides, then
//   2. loads the vendored canonical implementation.
//
// The canonical script reads window.REDIS_CLI_CONFIG at load, so it MUST be set
// before that script executes; assigning it synchronously here, before injecting
// the <script>, guarantees that ordering.
//
// NOTE: because the script is injected dynamically it may execute after
// DOMContentLoaded has already fired, so it must initialise off document
// .readyState (init immediately when the DOM is already parsed), not solely via a
// DOMContentLoaded listener.

// Airgap fork: upstream serves the widget and the command batches from one
// backend, so it carries a single REDIS_CLI_BACKEND used for both. In a
// disconnected deployment they are two different in-cluster paths — the batches
// go to the cli-proxy, the widget comes from the vendored copy the playground
// already ships — so the constant is split rather than pointed elsewhere.
const REDIS_CLI_API = '/cli';                              // cli-proxy, in-cluster
const REDIS_CLI_SCRIPT = '/cli-playground/assets/cli.js';  // vendored canonical widget

window.REDIS_CLI_CONFIG = {
  apiUrl: REDIS_CLI_API,          // POST command batches to the in-cluster cli-proxy
  // Which docs page a batch came from, for usage metrics. The widget used to
  // read this from its own URL (?source=), which only existed because "Try it"
  // opened redis.io/cli in a new tab. Snippets run in the workbench on the page
  // itself now, so the page has to say. The backend format-checks it and caps
  // distinct values.
  page: (function () {
    try { return window.location.pathname; } catch (err) { return ''; }
  })(),
  appendDbId: false,              // docs widgets don't carry a per-widget dbid
  promptPrefix: 'redis> ',        // docs use the bare prompt, not redis:6379>
  enableUrlCommands: false,       // commands come from the code block, not the URL
  showBadge: false,               // no "Powered by" badge in the docs
};

// Whether the canonical widget is still on its way. A "Try it" clicked before it
// lands must wait rather than fall back to another tab: "not here yet" and "this
// backend cannot do it" are different answers, and only the second one is a
// reason to leave the page.
window.REDIS_CLI_LOADING = true;
window.REDIS_CLI_FAILED = false;

(function () {
  const script = document.createElement('script');
  script.src = REDIS_CLI_SCRIPT;
  script.addEventListener('load', function () {
    window.REDIS_CLI_LOADING = false;
  });
  script.addEventListener('error', function () {
    window.REDIS_CLI_LOADING = false;
    window.REDIS_CLI_FAILED = true;
  });
  document.head.appendChild(script);
})();
