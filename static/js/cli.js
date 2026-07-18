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

window.REDIS_CLI_CONFIG = {
  apiUrl: '/cli',                 // POST command batches to the in-cluster cli-proxy
  appendDbId: false,              // docs widgets don't carry a per-widget dbid
  promptPrefix: 'redis> ',        // docs use the bare prompt, not redis:6379>
  enableUrlCommands: false,       // commands come from the code block, not the URL
  showBadge: false,               // no "Powered by" badge in the docs
};

(function () {
  const script = document.createElement('script');
  script.src = '/cli-playground/assets/cli.js'; // vendored canonical copy (airgap fork)
  document.head.appendChild(script);
})();
