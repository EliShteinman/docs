// Interactive redis-cli widget. This is the canonical implementation served by
// the /cli backend (…/cli/static/js/cli.js) and loaded by the docs site through
// a thin shim. Behaviour is configured via window.REDIS_CLI_CONFIG, which a
// consumer assigns BEFORE this script runs; the CONFIG DEFAULTS below reproduce
// the backend page's behaviour, so the backend loads this file with no config.
//
// The docs shim overrides a few fields, e.g.:
//   window.REDIS_CLI_CONFIG = {
//     apiUrl: 'https://redis.io/cli', appendDbId: false, promptPrefix: 'redis> ',
//     enableUrlCommands: false, showBadge: false,
//   };
const CONFIG = Object.assign({
  apiUrl: window.location.pathname, // where command batches are POSTed
  appendDbId: true,                 // append the widget's dbid to apiUrl
  promptPrefix: 'redis:6379> ',     // text shown before each typed command
  enableUrlCommands: true,          // honour ?commands=<base64>&autorun=true
  showBadge: true,                  // draw the "Powered by" badge on terminals
}, window.REDIS_CLI_CONFIG || {});

/* The live terminals on the page, keyed by their form element: {pre, input,
   prompt, dbid}. A WeakMap so a removed terminal is collectable. */
const terminals = new WeakMap();

async function createCli(cli) {
  const toExecute = getCommandsToExecute(cli);
  const urlCommands = CONFIG.enableUrlCommands ? getUrlCommands() : null;
  cli.replaceChildren();

  const pre = createPre(cli),
    [input, prompt] = createPrompt(cli),
    dbid = cli.getAttribute('dbid');

  drawTerminal(cli);
  drawBadge(cli);
  handleHistory(pre, input);

  /* Remember this terminal's parts so an embedder can run commands *into* it
     later (see window.RedisCli.run). Without that, adding commands to a live
     terminal means replacing it, which throws away the transcript — and a
     console whose history vanishes every time you use it isn't one. */
  terminals.set(cli, { pre, input, prompt, dbid });

  try {
    await asciiArt(cli, dbid, pre, input);
  } finally {
    cli.addEventListener(
      'submit',
      event => {
        event.preventDefault();

        const command = input.value;
        input.value = '';
        if (!command.trim()) {
          writeLines(pre, input, command, '', false);
          return;
        }

        disablePrompt(cli, input, prompt,
          () => executeInputCommand(dbid, pre, input, command)
        );
      }
    );

    if (toExecute) {
      disablePrompt(cli, input, prompt, () =>
        executeCommands(dbid, pre, input, toExecute, shouldAnimate(cli), 'preset'));
    }

    if (urlCommands) {
      if (urlCommands.autorun) {
        disablePrompt(cli, input, prompt, () =>
          executeCommands(dbid, pre, input, urlCommands.commands, false, 'share'));
      } else {
        input.value = urlCommands.commands[0] || '';
      }
    }
  }
}

function drawBadge(cli) {
  if (!CONFIG.showBadge || shouldAnimate(cli) || !isTerminal(cli)) {
    return
  }
  const badge = document.createElement('div');
  badge.classList.add('powered');
  badge.appendChild(document.createTextNode('Powered by'));
  cli.appendChild(badge);
}

function drawTerminal(cli) {
    if (!isTerminal(cli)) return;
    const bar = document.createElement('div');
    bar.classList.add('bar');

    const buttons = ['#d00', '#0d0', '#00d'];
    buttons.forEach((b) => {
      let button = document.createElement('span');
      button.classList.add('button')
      // button.style.backgroundColor = b;
      bar.appendChild(button);
    });

    cli.classList.add('terminal');
    cli.prepend(bar);
}

function isTerminal(cli) {
    return cli.getAttribute('terminal') !== null
}

function shouldAnimate(cli) {
  try {
    return cli.getAttribute('typewriter') !== null &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return true;
  }
}

function getUrlCommands() {
  try {
    const params = new URLSearchParams(window.location.search);
    const commandsParam = params.get('commands');
    if (!commandsParam) return null;

    const decoded = decodeBase64(commandsParam);
    if (decoded === null) return null;

    const commands = JSON.parse(decoded);
    if (!Array.isArray(commands) || commands.length === 0) return null;

    const autorun = params.get('autorun') === 'true';
    return { commands: commands.map(String), autorun };
  } catch {
    return null;
  }
}

function decodeBase64(value) {
  try {
    let s = value.replace(/-/g, '+').replace(/_/g, '/');
    const pad = s.length % 4;
    if (pad) s += '='.repeat(4 - pad);
    const bin = atob(s);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder('utf-8', { fatal: false }).decode(bytes);
  } catch {
    return null;
  }
}

function getCommandsToExecute(cli) {
  const textContent = cli.textContent.trim();
  if (!textContent) return;

  return textContent.split('\n').map(x => x.trim());
}

function createPre(cli) {
  const pre = document.createElement('pre');
  pre.setAttribute('tabindex', '0');
  cli.appendChild(pre);
  return pre;
}

function createPrompt(cli) {
  const prompt = document.createElement('div');
  prompt.classList.add('prompt');

  const prefix = document.createElement('span');
  prefix.appendChild(document.createTextNode(CONFIG.promptPrefix));
  prompt.appendChild(prefix);

  const input = document.createElement('input');
  input.setAttribute('name', 'prompt');
  input.setAttribute('type', 'text');
  input.setAttribute('autocomplete', 'off');
  input.setAttribute('spellcheck', 'false');
  prompt.appendChild(input);

  cli.appendChild(prompt);

  cli.addEventListener('click', () => {
    if (document.getSelection().type === 'Range') return;
    input.focus();
  });

  cli.addEventListener('keydown', event =>  {
    if (event.target === input) return;
    if (event.ctrlKey || event.altKey || event.shiftKey || event.metaKey) return;
    input.focus();
    input.scrollIntoView({block: "nearest"});
  });
  return [input, prompt];
}

async function disablePrompt(cli, input, prompt, fn) {
  cli.classList.add('disabled');
  input.disabled = true;
  prompt.style.display = 'none';
  /* Returned, so a caller can await the batch it just queued — window.RedisCli
     .run needs that to know when a snippet has finished running. The callers
     inside this file ignore it, as they always have. */
  return Promise.all([fn()])
    .then(() => {
      prompt.style.display = '';
      cli.classList.remove('disabled');
      input.disabled = false;
      input.focus({preventScroll: true});
    });
}

function handleHistory(pre, input) {
  let position = 0,
    tempValue = '';
  input.addEventListener('keydown', event => {
    switch (event.key) {
      case 'ArrowUp':
        event.preventDefault();

        if (position === Math.floor(pre.childNodes.length / 2)) return;
        else if (position === 0) tempValue = input.value;

        ++position;
        break;

      case 'ArrowDown':
        event.preventDefault();

        if (position === 0) return;
        else if (--position === 0) {
          setInputValue(input, tempValue);
          return;
        }
        break;

      default:
        return;
    }

    const { nodeValue } = pre.childNodes[pre.childNodes.length - position * 2];
    setInputValue(input, nodeValue.substring(CONFIG.promptPrefix.length, nodeValue.length - 1));
  });
}

function setInputValue(input, value) {
  input.value = value;
  input.setSelectionRange(value.length, value.length);
}

async function writeLines(pre, input, command, reply, animate) {
  await writeLine(pre, input, command, animate, true);
  await writeLine(pre, input, reply, false, false);
}

async function executeCommands(dbid, pre, input, commands, animate, source = 'interactive') {
  try {
     const { replies } = await execute(commands, dbid, source);
     for (const [i, command] of commands.entries()) {
      const { error, value, status } = replies[i];
      try {
        await writeLines(pre, input, command, error ? `(error) ${value}` : formatReply(value, '', status), animate, false);
      } catch (err) {
        console.error(err);
        await writeLines(pre, input, command, `(fatal error) ${err.message}`, animate);
      }
    }
  } catch (err) {
    for (const command of commands) {
      await writeLines(pre, input, command, err.message, animate);
    }
  }
}

async function executeInputCommand(dbid, pre, input, command) {
  switch (command.toLowerCase()) {
    case 'clear':
      pre.replaceChildren();
      break;

    case 'help':
      writeLine(pre, input, command, false, false);
      writeLine(pre, input, 'No problem! Let me just open this url for you: https://redis.io/commands', false, false);
      window.open('https://redis.io/commands');
      break;

    default:
      executeCommands(dbid, pre, input, [command], false, 'interactive');
      break;
  }
}

// One shared session per page; requests serialized through a queue so parallel
// auto-runs reuse a single session id instead of each sending id=undefined at
// once and forking into separate databases. On the single-widget /cli page the
// queue simply serializes one stream, which is transparent.
let session = { id: undefined };
let executeQueue = Promise.resolve();

// Page attribution. Docs pages that embed CLI share-links add the originating
// page path and the specific snippet id to the URL, e.g.
//   /cli?commands=...&autorun=true&source=%2Fdocs%2Flatest%2Fcommands%2Fhdel%2F&snippet=cmds_hash-stephdel
// Captured once per page load and attached to every batch, so both the autorun
// and any commands typed afterwards on that page are attributed to it. NOTE:
// the docs param is named `source`; we map it to `page` here to avoid colliding
// with the batch-origin `source` (interactive/share/preset/internal). The
// backend validates the format and caps distinct values (cardinality guard).
const pageContext = (() => {
  try {
    const params = new URLSearchParams(window.location.search);
    return { page: params.get('source') || '', snippet: params.get('snippet') || '' };
  } catch {
    return { page: '', snippet: '' };
  }
})();

// How this page was opened, decided once at load: 'example' if it carries a
// shared command set (a docs interactive-example link, ?commands=…), else
// 'direct' (someone opened redis.io/cli themselves). Sent on every batch; the
// backend only uses it on the one that mints the session, giving an exact
// direct-vs-example open count (no fragile subtraction).
const openType = (() => {
  try {
    return new URLSearchParams(window.location.search).has('commands')
      ? 'example' : 'direct';
  } catch {
    return 'direct';
  }
})();

async function execute(commands, dbid = '', source = 'interactive') {
  const url = CONFIG.apiUrl + (CONFIG.appendDbId ? dbid : '');
  const run = executeQueue.then(async () => {
    const response = await fetch(url, {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json'
      },
      // `source` labels the batch's origin for usage metrics: 'interactive'
      // (typed at the prompt), 'share' (a ?commands= base64 share-link
      // autorun), 'preset' (commands embedded in the page) or 'internal' (the
      // startup INFO the widget runs itself). The backend validates it against
      // a fixed allowlist, so an arbitrary value can't inflate label cardinality.
      body: JSON.stringify({
        commands,
        id: session.id,
        source,
        page: pageContext.page,
        snippet: pageContext.snippet,
        open_type: openType
      })
    });
    const reply = await response.json();
    session.id = reply.id;
    notifyExecuted({ commands, replies: reply.replies || [], dbid, source });
    return reply;
  });
  executeQueue = run.then(() => {}, () => {});
  return run;
}

// Embedder hooks, fired after a batch is served (see window.RedisCli.onExecute).
// Batches the widget runs for itself are deliberately NOT reported: 'internal'
// is the startup INFO, and 'workbench' is a listener's own introspection, which
// would otherwise re-enter its listener and loop.
const executeListeners = new Set();

function notifyExecuted(batch) {
  if (batch.source === 'internal' || batch.source === 'workbench') {
    return;
  }
  for (const listener of executeListeners) {
    try {
      listener(batch);
    } catch (err) {
      console.error(err);
    }
  }
}

// Quote and escape a bulk string exactly like redis-cli's sdscatrepr: operate
// on the raw UTF-8 bytes, use the named escapes \\ " \n \r \t \a \b, leave
// printable ASCII (0x20-0x7e) literal, and emit \xHH (lowercase) for every
// other byte. This mirrors the native CLI byte-for-byte, e.g. a NUL renders as
// "\x00" (not JSON's "\u0000") and "é" as "\xc3\xa9".
function reprBytes(bytes) {
  let out = '"';
  for (const b of bytes) {
    switch (b) {
      case 0x5c: out += '\\\\'; break;
      case 0x22: out += '\\"'; break;
      case 0x0a: out += '\\n'; break;
      case 0x0d: out += '\\r'; break;
      case 0x09: out += '\\t'; break;
      case 0x07: out += '\\a'; break;
      case 0x08: out += '\\b'; break;
      default:
        out += (b >= 0x20 && b <= 0x7e)
          ? String.fromCharCode(b)
          : `\\x${b.toString(16).padStart(2, '0')}`;
    }
  }
  return out + '"';
}

// A text bulk string: its UTF-8 bytes are what redis-cli would see, so "é"
// renders as "\xc3\xa9". Binary values never reach here — the backend tags them
// {$bin} (see formatReply) because their raw bytes can't survive JSON intact.
function reprString(str) {
  return reprBytes(new TextEncoder().encode(str));
}

// Decode standard base64 (as emitted by the backend's {$bin} tag) to raw bytes.
function base64ToBytes(b64) {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}

function formatReply(reply, indent = '', status = false) {
  if (reply === null) {
    return '(nil)';
  }

  // Out-of-range 64-bit integers are tagged by the backend (safe_json_integers)
  // as {$int: "<decimal>"} so they survive JSON without precision loss and stay
  // distinct from numeric bulk strings. Render them as a plain integer reply.
  if (typeof reply === 'object' && !Array.isArray(reply)
      && typeof reply.$int === 'string') {
    return `(integer) ${reply.$int}`;
  }

  // Nested RESP simple strings are tagged by the backend (safe_json_integers)
  // as {$status: "<text>"} so they render unquoted like redis-cli — distinct
  // from bulk strings, which are quoted. TS.INFO field names and enum values
  // (e.g. "compressed"), TS.RANGE sample values, etc. arrive this way. Top-level
  // status replies use the `status` flag below instead and never reach here.
  if (typeof reply === 'object' && !Array.isArray(reply)
      && typeof reply.$status === 'string') {
    return reply.$status;
  }

  // Binary bulk strings (non-UTF-8 bytes: BF.SCANDUMP, DUMP, GET of a bitmap,
  // ...) are tagged by the backend as {$bin: "<base64>"} because their raw bytes
  // can't round-trip through JSON. Decode and print them byte-for-byte with \xHH
  // escapes, exactly like redis-cli.
  if (typeof reply === 'object' && !Array.isArray(reply)
      && typeof reply.$bin === 'string') {
    return reprBytes(base64ToBytes(reply.$bin));
  }

  const type = typeof reply;
  if (type === 'string') {
    // RESP simple string / status reply (e.g. PONG, OK): rendered without quotes
    if (status) {
      return reply;
    }
    // Bulk string: quote and escape it byte-for-byte the way redis-cli does
    // (e.g. a JSON.GET payload renders as "{\"a\":1}" and a NUL byte as "\x00").
    return reprString(reply);
  } else if (type === 'number') {
    return `(integer) ${reply}`;
  } else if (Array.isArray(reply)) {
    if (reply.length === 0) {
      return '(empty array)';
    } else {
      let s = '';
      for (const [i, x] of reply.entries()) {
        const num = i + 1,
          nestedIndent = indent + ' '.repeat(num.toString().length + 2);
        s += `${i === 0 ? '' : `\n${indent}`}${num}) ${formatReply(x, nestedIndent)}`;
      }
      return s;
    }
  } else {
    return `-PROTOCOLERR Unknown reply type ${typeof reply}`;
  }
}

async function writeLine(pre, input, line, animate, prompt) {
  const textNode = document.createTextNode('');
  pre.appendChild(textNode);

  const toWrite = line + '\n';
  if (prompt) textNode.nodeValue = CONFIG.promptPrefix;
  if (!animate) {
    textNode.nodeValue += toWrite;
  } else {
    await typewriter(textNode, toWrite);
  }
  input.scrollIntoView({block: "nearest"});
}

function typewriter(textNode, toWrite) {
  return new Promise(resolve => {
    let i = 0;
    const intervalId = setInterval(() => {
      if (i === toWrite.length) {
        clearInterval(intervalId);
        resolve();
        return;
      }

      textNode.nodeValue += toWrite[i++];
    }, 25+Math.random()*25);
  });
}

async function asciiArt(cli, dbid, pre, input) {
  if (cli.getAttribute('asciiart') === null) return;

  const { replies: [{ error, value: raw }] } = await execute(['INFO SERVER'], dbid, 'internal');

  if (error) {
    writeLine(pre, input, `(error) ${raw}`, false);
  } else {
    const time = new Date().toISOString(),
      version = raw.match(/redis_version:(.*)/)[1],
      sha = raw.match(/redis_git_sha1:(.*)/)[1],
      dirty = raw.match(/redis_git_dirty:(.*)/)[1],
      bits = raw.match(/arch_bits:(.*)/)[1],
      port = raw.match(/tcp_port:(.*)/)[1],
      pid = raw.match(/process_id:(.*)/)[1];
    writeLine(
      pre,
      input,
`${pid}:C ${time} # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
${pid}:C ${time} # Configuration loaded
                  _._
            _.-\`\`__ ''-._
      _.-\`\`    \`.  \`_.  ''-._            Redis ${version} (${sha}/${dirty}) ${bits} bit
    .-\`\` .-\`\`\`.  \`\`\`\/    _.,_ ''-._
  (    '      ,       .-\`  | \`,    )     Running in standalone mode
  |\`-._\`-...-\` __...-.\`\`-._|'\` _.-'|     Port: ${port}
  |    \`-._   \`._    /     _.-'    |     PID: ${pid}
  \`-._    \`-._  \`-./  _.-'    _.-'
  |\`-._\`-._    \`-.__.-'    _.-'_.-'|
  |    \`-._\`-._        _.-'_.-'    |           https://redis.io
  \`-._    \`-._\`-.__.-'_.-'    _.-'
  |\`-._\`-._    \`-.__.-'    _.-'_.-'|
  |    \`-._\`-._        _.-'_.-'    |
  \`-._    \`-._\`-.__.-'_.-'    _.-'
      \`-._    \`-.__.-'    _.-'
          \`-._        _.-'
              \`-.__.-'

${pid}:M ${time} # Server initialized
${pid}:M ${time} * Ready to accept connections`,
        false);
  }
}

function initRedisClis() {
  for (const cli of document.querySelectorAll('form.redis-cli')) {
    createCli(cli);
  }
}

// Public API for embedders — currently the docs "Try it" workbench, which needs
// to run its own keyspace introspection (TYPE/TTL/HGETALL/...) against THIS
// page's session and render replies the same way the terminal does. Exposing
// this deliberately small surface is what keeps consumers from reimplementing
// the session handshake or the reply formatter and drifting from this file, the
// single source of truth for both.
//
// `session` is exposed by reference: it is only ever mutated (`session.id = …`),
// never reassigned, so a consumer holding it always reads the live session id.
// `createCli` initialises one terminal, for terminals added after page load;
// calling `init` again would re-initialise (and so clear) the existing ones.
window.RedisCli = {
  execute,        // (commands[], dbid?, source?) -> Promise<{id, replies}>
  formatReply,    // (value, indent?, status?) -> redis-cli-faithful text
  createCli,      // (form.redis-cli element) -> Promise, initialises a terminal
  init: initRedisClis,
  session,

  /* Run commands in an already-initialised terminal, appending them and their
     replies to its transcript exactly as if they had been typed — the prompt is
     disabled for the duration, so this cannot interleave with the reader typing.
     Resolves when the batch has been written; false if the element is not a
     live terminal. */
  run: function (cli, commands, source) {
    const parts = terminals.get(cli);
    if (!parts || !commands || !commands.length) return Promise.resolve(false);
    return disablePrompt(cli, parts.input, parts.prompt, () =>
      executeCommands(parts.dbid, parts.pre, parts.input, commands, false,
        source || 'preset')).then(() => true);
  },

  /* Empty a terminal's transcript, exactly as the `clear` command typed at its
     prompt does. Only the printed history goes: the session, its keys and the
     prompt are untouched. False if the element is not a live terminal. */
  clear: function (cli) {
    const parts = terminals.get(cli);
    if (!parts) return false;
    parts.pre.replaceChildren();
    return true;
  },
  // Called after every user-visible batch with {commands, replies, dbid,
  // source}; returns an unsubscribe function.
  onExecute(listener) {
    executeListeners.add(listener);
    return () => executeListeners.delete(listener);
  },
};

// Initialise as soon as the DOM is ready. When the docs' cli.js shim injects
// this file dynamically it may run AFTER DOMContentLoaded has already fired, so
// fall back to initialising immediately in that case.
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initRedisClis);
} else {
  initRedisClis();
}
