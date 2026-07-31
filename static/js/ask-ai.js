/*
 * Airgap fork: "Ask AI to explain this page" behavior.
 *
 * The button is rendered by layouts/partials/meta-links.html as a plain
 * <a href="/chat?..."> so the public build keeps the upstream redis.io behavior.
 * Here we override that for airgap deployments, driven by the single AI switch
 * RUNTIME_CONFIG.aiServices.litellm (the same one the agent-builder chat uses):
 *
 *   RUNTIME_CONFIG present + litellm.enabled  -> intercept the click, ask the
 *                                                internal LiteLLM endpoint, show
 *                                                the answer in a modal.
 *   RUNTIME_CONFIG present + litellm disabled  -> remove the button. No AI, and
 *                                                no outbound call to redis.io.
 *   RUNTIME_CONFIG absent (public build)       -> leave the <a href> untouched.
 */
(function () {
  "use strict";

  // meta-links renders once per page today, but guard against a future layout
  // that includes it twice (which would double-bind click handlers).
  if (window.__askAiInit) return;
  window.__askAiInit = true;

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function injectStyleOnce() {
    if (document.getElementById("ask-ai-style")) return;
    var css =
      ".ask-ai-modal{position:fixed;inset:0;z-index:9999;display:none;" +
      "align-items:center;justify-content:center;background:rgba(0,0,0,.5);}" +
      ".ask-ai-panel{background:#fff;color:#163341;max-width:640px;width:90%;" +
      "max-height:80vh;overflow:auto;border-radius:12px;padding:24px 28px;" +
      "box-shadow:0 10px 40px rgba(0,0,0,.3);}" +
      ".ask-ai-close{float:right;border:0;background:none;font-size:20px;" +
      "cursor:pointer;line-height:1;color:inherit;opacity:.6;}" +
      "@media (prefers-color-scheme:dark){.ask-ai-panel{background:#0f2129;color:#e6edf0;}}" +
      "[data-theme=dark] .ask-ai-panel,.dark .ask-ai-panel{background:#0f2129;color:#e6edf0;}";
    var el = document.createElement("style");
    el.id = "ask-ai-style";
    el.textContent = css;
    document.head.appendChild(el);
  }

  var modal, lastFocus;

  function showModal(html) {
    injectStyleOnce();
    if (!modal) {
      modal = document.createElement("div");
      modal.className = "ask-ai-modal";
      modal.setAttribute("role", "dialog");
      modal.setAttribute("aria-modal", "true");
      modal.setAttribute("aria-label", "AI explanation");
      modal.addEventListener("click", function (e) {
        if (e.target === modal) hideModal();
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && modal && modal.style.display === "flex") hideModal();
      });
      document.body.appendChild(modal);
    }
    modal.innerHTML =
      '<div class="ask-ai-panel">' +
      '<button type="button" class="ask-ai-close" aria-label="Close">×</button>' +
      html +
      "</div>";
    modal.style.display = "flex";
    var close = modal.querySelector(".ask-ai-close");
    if (close) {
      close.addEventListener("click", hideModal);
      close.focus();
    }
  }

  function hideModal() {
    if (modal) modal.style.display = "none";
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  function askLiteLLM(cfg, title, url) {
    if (!cfg.url) {
      showModal("<p>AI endpoint not configured.</p>");
      return;
    }
    showModal("<p>Asking AI…</p>");
    var prompt =
      'Explain this Redis documentation page: "' + title + '" (' + url +
      "). Summarize what it covers and the key points a reader should take away.";
    var headers = { "Content-Type": "application/json" };
    if (cfg.apiKey) headers["Authorization"] = "Bearer " + cfg.apiKey;

    fetch(cfg.url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        model: cfg.model || "gpt-3.5-turbo",
        messages: [{ role: "user", content: prompt }],
        max_tokens: 1000,
        temperature: 0.7
      })
    })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        var answer = (((data.choices || [])[0] || {}).message || {}).content || "(empty response)";
        showModal("<div>" + escapeHtml(answer).replace(/\n/g, "<br>") + "</div>");
      })
      .catch(function (err) {
        showModal("<p>AI request failed: " + escapeHtml(err.message || err) + "</p>");
      });
  }

  ready(function () {
    var links = document.querySelectorAll("a.ask-ai-link");
    if (!links.length) return;

    // No RUNTIME_CONFIG => public build: leave the upstream /chat link as-is.
    if (!window.RUNTIME_CONFIG) return;

    var cfg =
      (window.RUNTIME_CONFIG.aiServices && window.RUNTIME_CONFIG.aiServices.litellm) || {};

    if (!cfg.enabled) {
      // AI disabled system-wide: remove the button, no outbound call.
      Array.prototype.forEach.call(links, function (a) { a.remove(); });
      return;
    }

    // AI enabled: route the question to the internal LiteLLM endpoint.
    Array.prototype.forEach.call(links, function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        lastFocus = a;
        askLiteLLM(
          cfg,
          a.getAttribute("data-ask-title") || document.title,
          a.getAttribute("data-ask-url") || location.pathname
        );
      });
    });
  });
})();
