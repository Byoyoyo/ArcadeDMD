/* ArcadeDMD's window (1.37). Reads /api/state and /api/log each second, the marquee and the LED panel as images
   while the État tab is shown. Each tab is an entry of TABS: render() builds it, update(state) refreshes it.
   La fenêtre d'ArcadeDMD : lit l'état et le journal chaque seconde, le marquee et la dalle tant que l'onglet État est
   affiché. Chaque onglet est une entrée de TABS. */
"use strict";

const TOKEN = window.ARCADEDMD_TOKEN;
const APP = { state: null, lang: (navigator.language || "fr").toLowerCase().startsWith("fr") ? "fr" : "en",
  log: [], logAfter: 0, fails: 0, stopped: false, tab: null, frameUrls: {}, extra: {} };
const t = (fr, en) => (APP.lang === "fr" ? fr : en);

/* ---------------------------------------------------------------- small helpers / petits outils */
function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") el.className = v;
    else if (k === "style") el.style.cssText = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (k === "text") el.textContent = v;
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids.flat()) {
    if (kid === null || kid === undefined || kid === false) continue;
    el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  }
  return el;
}
const $ = (id) => document.getElementById(id);
function set(id, text, cls) {
  const el = $(id);
  if (!el) return;
  if (el.textContent !== text) el.textContent = text;
  if (cls !== undefined && el.className !== cls) el.className = cls;
}
async function api(path, body) {
  const opt = body === undefined ? {} : { method: "POST", body: JSON.stringify(body),
    headers: { "Content-Type": "application/json", "X-ArcadeDMD-Token": TOKEN } };
  const r = await fetch(path, opt);
  if (!r.ok) throw new Error(path + " " + r.status);
  return r.json();
}
function toast(text, ms) {
  const old = document.querySelector(".toast");
  if (old) old.remove();
  const el = h("div", { class: "toast", role: "status" }, text);
  document.body.append(el);
  setTimeout(() => el.remove(), ms || 4000);
}
function duration(s) {
  s = Math.max(0, Math.floor(s || 0));
  const d = Math.floor(s / 86400), hh = Math.floor((s % 86400) / 3600), m = Math.floor((s % 3600) / 60);
  if (d) return t(`${d} j ${hh} h`, `${d} d ${hh} h`);
  if (hh) return `${hh} h ${String(m).padStart(2, "0")}`;
  if (m) return `${m} min`;
  return `${s} s`;
}
/* a button that asks once more before doing it / un bouton qui redemande avant d'agir */
function sureButton(label, sureLabel, cls, fn) {
  let armed = 0;
  const b = h("button", { class: "btn " + (cls || ""), type: "button" }, label);
  b.addEventListener("click", () => {
    if (Date.now() < armed) { armed = 0; b.textContent = label; b.classList.remove("sure"); fn(); return; }
    armed = Date.now() + 4000;
    b.textContent = sureLabel;
    b.classList.add("sure");
    setTimeout(() => { if (armed && Date.now() >= armed) { armed = 0; b.textContent = label; b.classList.remove("sure"); } }, 4100);
  });
  return b;
}
const ICONS = {
  etat: '<path d="M3 12h4l3 7 4-14 3 7h4"/>',
  ecrans: '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
  emulateurs: '<rect x="2" y="7" width="20" height="11" rx="5"/><path d="M7 11v3M5.5 12.5h3"/><circle cx="16" cy="11.5" r="1"/><circle cx="18" cy="13.5" r="1"/>',
  frontal: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  journal: '<path d="M5 4h14v16H5z"/><path d="M8 8h8M8 12h8M8 16h5"/>',
};
function icon(name) {
  const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  s.setAttribute("width", "18"); s.setAttribute("height", "18"); s.setAttribute("viewBox", "0 0 24 24");
  s.setAttribute("fill", "none"); s.setAttribute("stroke", "currentColor"); s.setAttribute("stroke-width", "2");
  s.setAttribute("aria-hidden", "true");
  s.innerHTML = ICONS[name] || "";
  return s;
}

/* ---------------------------------------------------------------- the tabs / les onglets */
const TABS = [];

function sourceName(g) {
  if (!g) return "";
  if (g.source === "retroarch") return "RetroArch" + (g.core ? t(", cœur ", ", core ") + g.core : "");
  if (g.source === "plugin") return "MAME";
  if (g.source === "demo") return t("Démo", "Demo");
  return g.source || "";
}

function logClass(text) {
  const s = text.toLowerCase();
  if (/erreur|error|traceback|exception/.test(s)) return "l e";
  if (/blocage|stall|ne répond|does not answer|introuvable|not found|indisponible|unavailable|illisible|unreadable|impossible|cannot|could not/.test(s)) return "l w";
  if (/ jeu : | game: |retroarch : .* -> |retroarch: .* -> /.test(s)) return "l g";
  return "l";
}

TABS.push({
  id: "etat", fr: "État", en: "Status", order: 1,
  render(main) {
    main.append(
      h("div", { id: "alerts", style: "display:flex;flex-direction:column;gap:10px" }),
      h("div", { class: "head" },
        h("div", { class: "t" },
          h("span", { class: "lab", id: "g-lab" }),
          h("h1", { id: "g-title" }),
          h("span", { class: "sub", id: "g-sub" })),
        h("span", { style: "flex:1" })),
      h("div", { class: "grid", style: "--min:320px" },
        h("div", { class: "card", style: "gap:12px" },
          h("span", { class: "lab" }, t("Le marquee, en direct", "The marquee, live")),
          h("div", { class: "live", id: "live-hd", style: "aspect-ratio:1920/460" },
            h("img", { id: "img-hd", alt: t("Le marquee tel qu'il est affiché", "The marquee as shown"), hidden: true }),
            h("span", { class: "none", id: "none-hd" }, t("Pas d'écran de marquee", "No marquee screen")),
            h("span", { class: "tag", id: "tag-hd", hidden: true }))),
        h("div", { class: "card", style: "gap:12px" },
          h("span", { class: "lab" }, t("La dalle LED, en direct", "The LED panel, live")),
          h("div", { class: "live", style: "aspect-ratio:4/1;background:#050505" },
            h("img", { id: "img-led", alt: t("La dalle LED telle qu'elle est affichée", "The LED panel as shown"), hidden: true }),
            h("span", { class: "none", id: "none-led" }, t("En attente de la première image", "Waiting for the first image"))))),
      h("div", { class: "grid", style: "--min:210px" },
        statusCard("ra", "RetroArch"), statusCard("mame", "MAME"),
        statusCard("lcd", t("Marquee LCD", "LCD marquee")), statusCard("led", t("Dalle LED", "LED panel"))),
      h("div", { class: "card" },
        h("div", { class: "row-h" },
          h("span", { class: "lab" }, t("Ce qui vient de se passer", "What just happened")),
          h("span", { class: "grow" }),
          h("a", { href: "#journal", style: "font-size:13px;font-weight:600" }, t("Tout le journal", "The whole log"))),
        h("div", { class: "events", id: "events" })),
      h("div", { class: "card" },
        h("div", { class: "row-h" }, h("h2", {}, "ArcadeDMD"), h("span", { class: "grow" }),
          h("span", { class: "small", id: "app-up" })),
        h("label", { class: "check", id: "auto-row", hidden: true },
          h("input", { type: "checkbox", id: "auto", onchange: (e) => setAutostart(e.target.checked) }),
          t("Lancer ArcadeDMD avec Windows", "Start ArcadeDMD with Windows")),
        h("div", { class: "btns" },
          h("button", { class: "btn", type: "button", onclick: () => doAction("restart") }, t("Relancer", "Restart")),
          h("button", { class: "btn", type: "button", onclick: () => api("/api/action", { do: "open_folder" }) },
            t("Ouvrir le dossier", "Open the folder")),
          sureButton(t("Quitter ArcadeDMD", "Quit ArcadeDMD"), t("Sûr ? Le marquee s'arrête", "Sure? The marquee stops"),
            "danger", () => doAction("quit")))));
  },
  update(s) {
    const g = s.game;
    if (g) {
      set("g-lab", g.source === "demo" ? t("Démo en cours", "Demo running") : t("Jeu en cours", "Game running"));
      set("g-title", g.title || g.rom || "?");
      const bits = [sourceName(g)];
      if (g.key) bits.push(`games/${g.key}.json`);
      else if (g.source !== "demo") bits.push(t("pas de fichier dans games, scène de base", "no file in games, basic scene"));
      if (g.values) bits.push(t(`${g.values} valeurs lues`, `${g.values} values read`));
      if (s.credits !== null && s.credits !== undefined)
        bits.push(t(`${s.credits} crédit${s.credits > 1 ? "s" : ""}`, `${s.credits} credit${s.credits === 1 ? "" : "s"}`));
      set("g-sub", bits.filter(Boolean).join(" · "));
    } else if (s.mode === "starting") {
      set("g-lab", ""); set("g-title", t("ArcadeDMD démarre", "ArcadeDMD is starting")); set("g-sub", "");
    } else {
      set("g-lab", t("En attente", "Waiting"));
      set("g-title", t("Aucun jeu lancé", "No game running"));
      set("g-sub", t("Lance un jeu dans RetroArch ou MAME, le marquee le suit.",
                     "Start a game in RetroArch or MAME, the marquee follows it."));
    }
    // RetroArch
    const ra = s.retroarch;
    if (!ra) setStatus("ra", t("Désactivé", "Disabled"), "dim", t("Dans config.json", "In config.json"));
    else if (s.silent) setStatus("ra", t("Ne répond pas", "Not answering"), "warn",
      t(`Il tourne mais le port ${ra.port} reste muet`, `It runs but port ${ra.port} stays silent`));
    else if (ra.age !== null && ra.age < 15) setStatus("ra", ra.playing ? t("Partie suivie", "Game followed") : t("Connecté", "Connected"),
      "ok", t(`Commandes réseau, port ${ra.port}`, `Network commands, port ${ra.port}`) + (ra.version ? ` · ${ra.version}` : ""));
    else setStatus("ra", t("En attente", "Waiting"), "dim", t("RetroArch n'est pas lancé", "RetroArch is not running"));
    // MAME
    if (s.mame && s.mame.playing) setStatus("mame", t("Partie suivie", "Game followed"), "ok", t("Par le plugin ArcadeDMD", "By the ArcadeDMD plugin"));
    else setStatus("mame", t("En attente", "Waiting"), "dim", t("Le plugin parle dès qu'un jeu démarre", "The plugin talks as soon as a game starts"));
    // screens / écrans
    const lcd = s.outputs.find((o) => o.kind === "marquee" || o.kind === "window");
    if (lcd) setStatus("lcd", lcd.shown ? t("Affiché", "Shown") : t("Caché", "Hidden"), lcd.shown ? "ok" : "dim",
      `${lcd.w} × ${lcd.h}` + t(` à ${lcd.x}, ${lcd.y}`, ` at ${lcd.x}, ${lcd.y}`) + (lcd.shown ? "" : t(", le frontal a l'écran", ", the frontend has the screen")));
    else setStatus("lcd", t("Aucun", "None"), "dim", t("Pas de fenêtre de marquee", "No marquee window"));
    const pc = s.outputs.find((o) => o.kind === "pixelcade"), zd = s.outputs.find((o) => o.kind === "zedmd");
    if (pc) setStatus("led", pc.ok ? "Pixelcade" : t("Pixelcade absente", "Pixelcade missing"), pc.ok ? "ok" : "warn",
      pc.ok ? t(`Port ${pc.port || "trouvé"}`, `Port ${pc.port || "found"}`) : t("Branchée ? Le port est cherché seul", "Plugged in? The port is looked for on its own"));
    else if (zd) setStatus("led", zd.ok ? "ZeDMD" : t("ZeDMD absente", "ZeDMD missing"), zd.ok ? "ok" : "warn", "");
    else setStatus("led", t("Aucune", "None"), "dim", t("Pas de dalle active", "No panel enabled"));
    $("none-hd").textContent = lcd ? t("En attente de la première image", "Waiting for the first image") : t("Pas d'écran de marquee", "No marquee screen");
    if (lcd) $("live-hd").style.aspectRatio = `${lcd.w}/${lcd.h}`;
    const tag = $("tag-hd");
    tag.hidden = !(lcd && !lcd.shown);
    tag.textContent = t("Caché, dernière image", "Hidden, last image");
    // alerts / alertes
    const box = $("alerts");
    box.replaceChildren();
    if (s.stall && s.stall.length)
      box.append(h("div", { class: "banner bad" }, h("div", {}, h("b", {}, t("Un fil d'ArcadeDMD est arrêté", "A thread of ArcadeDMD stopped")),
        t(`${s.stall.join(", ")}. Le détail est écrit dans le dossier runtime.`, `${s.stall.join(", ")}. The details are written in the runtime folder.`))));
    if (s.silent)
      box.append(h("div", { class: "banner" }, h("div", {}, h("b", {}, t("RetroArch ne répond pas", "RetroArch does not answer")),
        t("Il tourne mais ses commandes réseau restent muettes. Le marquee ne peut pas suivre le jeu. Vérifie le réglage dans l'onglet Émulateurs.",
          "It runs but its network commands stay silent. The marquee cannot follow the game. Check the setting in the Emulators tab."))));
    // the ArcadeDMD card / la carte ArcadeDMD
    $("auto-row").hidden = !s.windows;
    const a = $("auto");
    if (a && document.activeElement !== a) a.checked = !!s.autostart;
    set("app-up", t(`Tourne depuis ${duration(s.up)}`, `Running for ${duration(s.up)}`));
    renderEvents();
  },
  frames: true,
});

function statusCard(id, label) {
  return h("div", { class: "card" }, h("span", { class: "lab" }, label),
    h("span", { class: "big", id: `st-${id}` }), h("span", { class: "small", id: `st-${id}-s` }));
}
function setStatus(id, main, cls, sub) {
  set(`st-${id}`, main, "big " + cls);
  set(`st-${id}-s`, sub || "", "small");
}
function renderEvents() {
  const box = $("events");
  if (!box) return;
  const last = APP.log.slice(-7).reverse();
  const key = last.map((l) => l.n).join(",");
  if (box.dataset.key === key) return;
  box.dataset.key = key;
  box.replaceChildren(...last.flatMap((l) => {
    const m = /^(\d\d:\d\d):\d\d (.*)$/.exec(l.text);
    return [h("span", { class: "h" }, m ? m[1] : ""), h("span", {}, m ? m[2] : l.text)];
  }));
}
async function setAutostart(on) {
  try {
    const r = await api("/api/action", { do: "autostart", on });
    toast(r.on ? t("ArcadeDMD se lancera avec Windows.", "ArcadeDMD will start with Windows.")
               : t("ArcadeDMD ne se lancera plus avec Windows.", "ArcadeDMD will no longer start with Windows."));
  } catch (e) { toast(t("Le réglage n'a pas pu être changé.", "The setting could not be changed.")); }
}
async function doAction(what) {
  try {
    await api("/api/action", { do: what });
  } catch (e) { toast(t("ArcadeDMD n'a pas répondu.", "ArcadeDMD did not answer.")); return; }
  if (what === "quit") { APP.stopped = true; showStopped(); }
  else toast(t("ArcadeDMD redémarre, le marquee revient dans un instant.", "ArcadeDMD restarts, the marquee is back in a moment."));
}
function showStopped() {
  $("main").replaceChildren(h("div", { class: "stopped" }, h("h1", {}, t("ArcadeDMD est arrêté", "ArcadeDMD is stopped")),
    h("span", { class: "sub" }, t("Tu peux fermer cette fenêtre. Relance ArcadeDMD avec run.bat ou au prochain démarrage de Windows.",
      "You can close this window. Start ArcadeDMD again with run.bat or at the next Windows start."))));
  setPill("bad", t("Arrêté", "Stopped"));
}

TABS.push({
  id: "journal", fr: "Journal", en: "Log", order: 9,
  render(main) {
    const box = h("div", { class: "logbox", id: "logbox", role: "log", "aria-live": "off" });
    const filter = h("input", { type: "search", id: "logfilter", placeholder: t("Chercher dans le journal", "Search the log"),
      oninput: () => fillLog(true) });
    main.append(
      h("div", { class: "head" }, h("div", { class: "t" }, h("h1", {}, t("Journal", "Log")),
        h("span", { class: "sub", id: "logwhere" }, t("Les dernières lignes de runtime\\arcadedmd.log", "The last lines of runtime\\arcadedmd.log")))),
      h("div", { class: "toolbar" }, filter,
        h("button", { class: "btn", type: "button", onclick: copyLog }, t("Copier", "Copy")),
        h("button", { class: "btn", type: "button", onclick: () => api("/api/action", { do: "open_log" }) },
          t("Ouvrir le fichier", "Open the file"))),
      box);
    fillLog(true);
  },
  update() { fillLog(false); },
});

function fillLog(all) {
  const box = $("logbox");
  if (!box) return;
  const q = ($("logfilter") || {}).value ? $("logfilter").value.toLowerCase() : "";
  const follow = box.scrollHeight - box.scrollTop - box.clientHeight < 40;
  const shown = Number(box.dataset.last || 0);
  if (all) { box.replaceChildren(); box.dataset.last = "0"; }
  const add = APP.log.filter((l) => (all || l.n > shown) && (!q || l.text.toLowerCase().includes(q)));
  if (!add.length && !all) return;
  box.append(...add.map((l) => h("span", { class: logClass(l.text) }, l.text)));
  if (APP.log.length) box.dataset.last = String(APP.log[APP.log.length - 1].n);
  while (box.childElementCount > 2000) box.firstChild.remove();
  if (follow || all) box.scrollTop = box.scrollHeight;
}
async function copyLog() {
  const text = [...document.querySelectorAll("#logbox .l")].map((e) => e.textContent).join("\n");
  try { await navigator.clipboard.writeText(text); toast(t("Journal copié.", "Log copied.")); }
  catch (e) {
    const r = document.createRange(); r.selectNodeContents($("logbox"));
    const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
  }
}

/* ---------------------------------------------------------------- the frame / le cadre */
function buildTabs() {
  const nav = $("tabs");
  nav.replaceChildren(...TABS.map((tab) => h("a", { href: "#" + tab.id, id: "tab-" + tab.id }, icon(tab.id), t(tab.fr, tab.en))),
    h("span", { class: "grow" }),
    h("div", { class: "side-foot", id: "side-foot" }, h("span", { id: "sf-up" }), h("br"), h("span", { id: "sf-stall" })));
}
function route() {
  if (APP.stopped) return;
  const id = (location.hash || "#etat").slice(1);
  const tab = TABS.find((x) => x.id === id) || TABS[0];
  APP.tab = tab;
  for (const x of TABS) {
    const a = $("tab-" + x.id);
    if (a) { a.classList.toggle("on", x === tab); a.setAttribute("aria-current", x === tab ? "page" : "false"); }
  }
  const main = $("main");
  main.replaceChildren();
  tab.render(main);
  if (APP.state && tab.update) tab.update(APP.state);
  main.scrollTop = 0;
}
function setPill(cls, text) {
  const p = $("pill");
  p.className = "pill " + cls;
  p.querySelector("span").textContent = text;
}

async function poll() {
  if (APP.stopped) return;
  try {
    const s = await api("/api/state");
    const fresh = !APP.state;
    APP.fails = 0;
    APP.state = s;
    if (s.lang && s.lang !== APP.lang) { APP.lang = s.lang; document.documentElement.lang = s.lang; buildTabs(); route(); }
    else if (fresh) route();
    $("ver").textContent = s.version;
    if (s.goto) {                       // the icon's menu asked for a tab / le menu de l'icône demande un onglet
      if (APP.gotoSeen === undefined) APP.gotoSeen = s.goto[0];
      else if (s.goto[0] > APP.gotoSeen) { APP.gotoSeen = s.goto[0]; if (s.goto[1]) location.hash = s.goto[1]; }
    }
    const lg = await api("/api/log?after=" + APP.logAfter);
    if (lg.lines.length) {
      APP.log.push(...lg.lines);
      APP.logAfter = lg.lines[lg.lines.length - 1].n;
      if (APP.log.length > 2000) APP.log.splice(0, APP.log.length - 2000);
    }
    if (s.stall && s.stall.length) setPill("bad", t("Blocage", "Stalled"));
    else if (s.silent) setPill("warn", t("RetroArch muet", "RetroArch silent"));
    else if (s.game) setPill("ok", s.game.source === "demo" ? t("Démo", "Demo") : t("Partie en cours", "Game running"));
    else setPill("ok", t("En marche", "Running"));
    set("sf-up", t(`Tourne depuis ${duration(s.up)}`, `Running for ${duration(s.up)}`));
    set("sf-stall", s.stall && s.stall.length ? t("Blocage en cours", "Stalled now") : t("Aucun blocage", "No stall"),
      s.stall && s.stall.length ? "bad" : "ok");
    if (APP.tab && APP.tab.update) APP.tab.update(s);
  } catch (e) {
    APP.fails += 1;
    if (APP.fails >= 3) setPill("bad", t("ArcadeDMD ne répond plus", "ArcadeDMD does not answer"));
  }
}

async function frame(name, imgId, noneId) {
  const img = $(imgId);
  if (!img) return;
  try {
    const r = await fetch("/api/frame/" + name + "?t=" + Date.now());
    if (!r.ok) return;
    const url = URL.createObjectURL(await r.blob());
    img.onload = () => { if (APP.frameUrls[name]) URL.revokeObjectURL(APP.frameUrls[name]); APP.frameUrls[name] = url; };
    img.src = url;
    img.hidden = false;
    const none = $(noneId);
    if (none) none.hidden = true;
  } catch (e) { /* the next one / la suivante */ }
}
async function frames() {
  if (!APP.stopped && APP.tab && APP.tab.frames && document.visibilityState === "visible") {
    await Promise.all([frame("hd.jpg", "img-hd", "none-hd"), frame("led.png", "img-led", "none-led")]);
  }
  setTimeout(frames, 500);
}

function start() {
  TABS.sort((a, b) => (a.order || 0) - (b.order || 0));
  buildTabs();
  window.addEventListener("hashchange", route);
  route();
  poll();
  setInterval(poll, 1000);
  frames();
}
