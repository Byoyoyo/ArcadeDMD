/* The settings tabs of ArcadeDMD's window (1.37): Écrans and Émulateurs. They read their own route once when shown
   and write config.json when saved, ArcadeDMD then starts again with the new settings by itself.
   Les onglets de réglage. Ils lisent leur route à l'affichage et écrivent config.json à l'enregistrement. */
"use strict";

const OK_ICON = '<path d="M5 12l5 5 9-10"/>';
const WARN_ICON = '<circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16.5v.5"/>';
const BAD_ICON = '<path d="M6 6l12 12M18 6L6 18"/>';
function mark(kind) {
  const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  s.setAttribute("width", "18"); s.setAttribute("height", "18"); s.setAttribute("viewBox", "0 0 24 24");
  s.setAttribute("fill", "none"); s.setAttribute("stroke-width", "2.5"); s.setAttribute("aria-hidden", "true");
  s.setAttribute("stroke", kind === "ok" ? "#5FE08F" : kind === "bad" ? "#FF6B6B" : kind === "warn" ? "#FFB547" : "#6E7588");
  s.style.flex = "none";
  s.style.marginTop = "1px";
  s.innerHTML = kind === "ok" ? OK_ICON : kind === "bad" ? BAD_ICON : WARN_ICON;
  return s;
}
function check(kind, text) {
  return h("div", { class: "row-c" }, mark(kind), h("span", {}, text));
}
function chip(cls, text) { return h("span", { class: "chip " + cls }, text); }
function field(label, input) { return h("label", { class: "field" }, label, input); }
function select(id, options, value) {
  const s = h("select", { id });
  for (const [v, text] of options) s.append(h("option", { value: v, selected: String(v) === String(value) }, text));
  return s;
}
function loading(main, title, sub) {
  main.append(h("div", { class: "head" }, h("div", { class: "t" }, h("h1", {}, title), h("span", { class: "sub" }, sub))),
    h("div", { id: "tabbody", class: "dim" }, t("Lecture des réglages", "Reading the settings")));
}
async function busy(btn, fn) {
  const old = btn.textContent;
  btn.disabled = true;
  try { return await fn(); } finally { btn.disabled = false; btn.textContent = old; }
}
function saved(r, what) {
  if (r && r.ok) toast(what || t("Enregistré. ArcadeDMD repart avec ces réglages dans un instant.",
                                 "Saved. ArcadeDMD starts again with these settings in a moment."));
  else toast((r && r.error) || t("Pas enregistré.", "Not saved."), 6000);
}

/* ---------------------------------------------------------------- Écrans / Screens */
TABS.push({
  id: "ecrans", fr: "Écrans", en: "Screens", order: 2,
  async render(main) {
    loading(main, t("Écrans", "Screens"), t("Choisis l'écran du marquee dans la liste de ceux que Windows voit.",
                                             "Pick the marquee screen in the list of those Windows sees."));
    let d;
    try { d = await api("/api/screens"); } catch (e) { $("tabbody").textContent = t("Réglages illisibles.", "Settings unreadable."); return; }
    if (APP.tab.id !== "ecrans") return;
    APP.extra.screens = d;
    drawScreens(d);
  },
});

function drawScreens(d) {
  const body = $("tabbody");
  body.className = "stack";
  const pv = d.preview, led = d.led;
  const head = document.querySelector("main .head");
  if (d.windows && head && !head.querySelector(".ident"))
    head.append(h("span", { style: "flex:1" }), h("button", { class: "btn ident", type: "button",
      onclick: (e) => busy(e.target, () => api("/api/screens/identify", {})) }, t("Identifier les écrans", "Identify the screens")));

  const num = (id, v) => h("input", { id, inputmode: "numeric", value: v === null || v === undefined ? "" : String(v) });
  const xs = num("pv-x", pv.x), ys = num("pv-y", pv.y), ws = num("pv-w", pv.width), hs = num("pv-h", pv.height);
  const list = h("div", { class: "screens" });
  const pick = (s) => {
    xs.value = s.x; ys.value = s.y; ws.value = s.width; hs.value = s.height;
    $("pv-on").checked = true;
    paint();
  };
  const paint = () => {
    const on = $("pv-on").checked;
    for (const b of list.querySelectorAll("button")) {
      const s = d.screens[Number(b.dataset.i)];
      const chosen = on && s && Number(xs.value) >= s.x && Number(xs.value) < s.x + s.width
        && Number(ys.value) >= s.y && Number(ys.value) < s.y + s.height;
      b.setAttribute("aria-pressed", chosen ? "true" : "false");
      b.querySelector(".what").textContent = chosen ? t("Marquee choisi", "Marquee picked")
        : s.primary ? t("Principal, le jeu", "Main, the game") : s.guess ? t("Semble fait pour le marquee", "Looks made for the marquee") : "";
    }
    for (const el of body.querySelectorAll(".pv-dep")) el.disabled = !on;
  };
  d.screens.forEach((s, i) => {
    const ratio = `${s.width} / ${s.height}`;
    list.append(h("button", { type: "button", class: "screen", "data-i": String(i), onclick: () => pick(s) },
      h("span", { class: "shape", style: `aspect-ratio:${ratio}` }, String(i + 1)),
      h("span", { class: "big" }, t(`Écran ${i + 1}`, `Screen ${i + 1}`) + ` · ${s.width} × ${s.height}`),
      h("span", { class: "small what" })));
  });
  if (!d.screens.length)
    list.append(h("span", { class: "dim" }, d.windows ? t("Windows ne donne aucun écran.", "Windows gives no screen.")
      : t("La liste des écrans vient de Windows. Ici, règle la position et la taille à la main.",
          "The list of screens comes from Windows. Here, set the position and size by hand.")));
  for (const el of [xs, ys, ws, hs]) { el.classList.add("pv-dep"); el.addEventListener("input", paint); }

  const ledKind = select("led-kind", [["pixelcade", "Pixelcade"], ["zedmd", "ZeDMD"], ["none", t("Aucune", "None")]], led.kind);
  const ports = [["", t("Trouvé seul", "Found on its own")]].concat(d.ports.map((p) =>
    [p.device, p.device + (p.likely ? t(", Pixelcade probable", ", probably the Pixelcade") : "")]));
  if (led.device && !d.ports.some((p) => p.device === led.device)) ports.push([led.device, led.device + t(", pas branché", ", not plugged in")]);
  const portSel = select("led-port", ports, led.device);
  const order = select("led-order", [["auto", t("Trouvé seul", "Found on its own")], ["rgb", "RGB"], ["rbg", t("RBG, vert et bleu inversés", "RBG, green and blue swapped")]], led.color_order);
  const bright = h("input", { type: "range", id: "led-bright", min: "0", max: "15", step: "1", value: led.brightness === null ? "8" : String(led.brightness) });
  const brightKeep = h("input", { type: "checkbox", id: "led-bright-keep", checked: led.brightness === null });
  const pcRow = h("div", { class: "grid", style: "--min:200px" }, field(t("Port", "Port"), portSel), field(t("Ordre des couleurs", "Colour order"), order));
  const zdRow = h("div", { class: "grid", style: "--min:200px" }, field(t("Luminosité, de 0 à 15", "Brightness, 0 to 15"), bright),
    h("label", { class: "check" }, brightKeep, t("Garder celle réglée dans la dalle", "Keep the one set in the panel")));
  const showLed = () => { pcRow.hidden = ledKind.value !== "pixelcade"; zdRow.hidden = ledKind.value !== "zedmd"; bright.disabled = brightKeep.checked; };
  ledKind.addEventListener("change", showLed);
  brightKeep.addEventListener("change", showLed);

  body.replaceChildren(
    h("div", { class: "card" },
      h("span", { class: "lab" }, t("Le marquee", "The marquee")),
      h("label", { class: "check" }, h("input", { type: "checkbox", id: "pv-on", checked: !!pv.enabled, onchange: paint }),
        t("Un écran LCD sert de marquee", "An LCD screen is used as the marquee")),
      list,
      h("div", { class: "grid", style: "--min:130px" }, field(t("Position x", "Position x"), xs), field(t("Position y", "Position y"), ys),
        field(t("Largeur", "Width"), ws), field(t("Hauteur", "Height"), hs)),
      h("div", { class: "grid", style: "--min:260px" },
        field(t("Affichage", "Display"), select("pv-style", [["hd", t("HD lisse, avec le logo du jeu", "Smooth HD, with the game logo")],
          ["led", t("LED virtuelles, comme une vraie dalle", "Virtual LEDs, like a real panel")]], pv.style === "hd" ? "hd" : "led")),
        h("label", { class: "check", style: "align-self:end" }, h("input", { type: "checkbox", id: "pv-top", class: "pv-dep", checked: !!pv.topmost }),
          t("Toujours au-dessus du frontal pendant les parties", "Always above the frontend during games")))),
    h("div", { class: "card" },
      h("span", { class: "lab" }, t("La dalle LED", "The LED panel")),
      h("div", { class: "grid", style: "--min:200px" }, field(t("Dalle", "Panel"), ledKind)),
      pcRow, zdRow),
    h("div", { class: "btns", style: "justify-content:space-between" },
      h("div", { class: "btns" },
        h("button", { class: "btn", type: "button", onclick: (e) => busy(e.target, async () => {
          const r = await api("/api/test", { game: "kof98", seconds: 12 });
          toast(r.ok ? t("Une démo passe 12 secondes sur le marquee et la dalle, sauf pendant une partie.",
                         "A demo plays for 12 seconds on the marquee and the panel, except during a game.") : t("Démo impossible.", "Demo not possible."));
        }) }, t("Tester le marquee et la dalle", "Test the marquee and the panel"))),
      h("div", { class: "btns" },
        h("button", { class: "btn", type: "button", onclick: () => route() }, t("Annuler", "Cancel")),
        h("button", { class: "btn main", type: "button", onclick: (e) => busy(e.target, saveScreens) }, t("Enregistrer", "Save")))));
  paint();
  showLed();
}

async function saveScreens() {
  const v = (id) => $(id).value.trim();
  const preview = { enabled: $("pv-on").checked, style: v("pv-style"), topmost: $("pv-top").checked };
  if (preview.enabled) Object.assign(preview, { x: v("pv-x"), y: v("pv-y"), width: v("pv-w"), height: v("pv-h") });
  const kind = v("led-kind");
  const led = { kind, device: v("led-port"), color_order: v("led-order") };
  if (kind === "zedmd") led.brightness = $("led-bright-keep").checked ? null : Number(v("led-bright"));
  saved(await api("/api/screens", { preview, led }));
}

/* ---------------------------------------------------------------- Émulateurs / Emulators */
TABS.push({
  id: "emulateurs", fr: "Émulateurs", en: "Emulators", order: 3,
  async render(main) {
    loading(main, t("Émulateurs", "Emulators"), t("ArcadeDMD vérifie chaque réglage et corrige ce qui manque d'un clic.",
                                                  "ArcadeDMD checks each setting and fixes what is missing in one click."));
    await loadEmulators();
  },
});

async function loadEmulators() {
  let d;
  try { d = await api("/api/emulators"); } catch (e) { $("tabbody").textContent = t("Réglages illisibles.", "Settings unreadable."); return; }
  if (!APP.tab || APP.tab.id !== "emulateurs") return;
  APP.extra.emulators = d;
  const body = $("tabbody");
  body.className = "grid";
  body.style.cssText = "--min:340px";
  body.replaceChildren(raCard(d.retroarch), mameCard(d.mame), coinsCard(d.coins, d.windows), recordCard(d.record, d.retroarch));
}

function folderField(id, what, value, placeholder) {
  const input = h("input", { id, value: value || "", placeholder, spellcheck: "false" });
  const keep = h("button", { class: "btn", type: "button", onclick: (e) => busy(e.target, async () => {
    const r = await api("/api/emulators/folder", { what, dir: input.value });
    if (r.ok) { toast(t("Dossier retenu.", "Folder kept.")); loadEmulators(); } else toast(r.error || t("Dossier refusé.", "Folder refused."), 6000);
  }) }, t("Retenir", "Keep"));
  return h("div", { class: "field" }, t("Dossier", "Folder"), h("div", { class: "inline" }, input, keep));
}

function raCard(ra) {
  const card = h("div", { class: "card" });
  const netOn = ra.net === "true", portOk = String(ra.net_port) === String(ra.port);
  let status;
  if (!ra.enabled) status = chip("dim", t("Coupé dans config.json", "Off in config.json"));
  else if (!ra.cfg) status = chip("warn", t("Introuvable", "Not found"));
  else if (netOn && portOk) status = chip("ok", t("Prêt", "Ready"));
  else status = chip("warn", t("À régler", "To set"));
  card.append(h("div", { class: "row-h" }, h("h2", {}, "RetroArch"), h("span", { class: "grow" }), status),
    folderField("ra-dir", "retroarch", ra.dir, "C:\\RetroArch-Win64"));
  if (ra.cfg) {
    card.append(
      check("ok", ra.how === "running" ? t("retroarch.cfg trouvé, celui du RetroArch lancé", "retroarch.cfg found, the one of the running RetroArch")
        : t("retroarch.cfg trouvé", "retroarch.cfg found")),
      check(netOn ? "ok" : "bad", netOn ? t("Commandes réseau actives", "Network commands on")
        : t("Commandes réseau coupées, le marquee ne peut pas lire les jeux", "Network commands off, the marquee cannot read the games")),
      check(portOk ? "ok" : "bad", portOk ? t(`Port ${ra.port}, le même des deux côtés`, `Port ${ra.port}, the same on both sides`)
        : t(`RetroArch écoute sur le port ${ra.net_port} et ArcadeDMD sur le ${ra.port}`, `RetroArch listens on port ${ra.net_port} and ArcadeDMD on ${ra.port}`)));
    if (ra.save_on_exit === "false")
      card.append(check("warn", t("RetroArch n'enregistre pas ses réglages en quittant, la correction reste donc après sa fermeture",
                                  "RetroArch does not save its settings when it quits, so the fix stays after it closes")));
  } else {
    card.append(check("warn", t("Indique le dossier qui contient retroarch.exe et retroarch.cfg", "Give the folder that holds retroarch.exe and retroarch.cfg")));
  }
  const btns = h("div", { class: "btns" });
  if (ra.cfg && !(netOn && portOk)) {
    const fix = h("button", { class: "btn main", type: "button", disabled: ra.running, onclick: (e) => busy(e.target, async () => {
      const r = await api("/api/emulators/retroarch/fix", {});
      if (r.ok) { toast(t("Corrigé. Une copie de l'ancien retroarch.cfg est gardée à côté.", "Fixed. A copy of the old retroarch.cfg is kept next to it.")); loadEmulators(); }
      else toast(r.error || t("Pas corrigé.", "Not fixed."), 6000);
    }) }, t("Corriger", "Fix"));
    btns.append(fix);
    if (ra.running) card.append(check("warn", t("Ferme RetroArch pour corriger, il réécrit son fichier en quittant", "Close RetroArch to fix it, it writes its file again when it quits")));
  }
  btns.append(h("button", { class: "btn", type: "button", onclick: (e) => busy(e.target, loadEmulators) }, t("Vérifier à nouveau", "Check again")));
  if (ra.cfg) btns.append(h("button", { class: "btn", type: "button", onclick: () => api("/api/emulators/open", { what: "retroarch_cfg" }) },
    t("Ouvrir retroarch.cfg", "Open retroarch.cfg")));
  card.append(btns);
  return card;
}

function mameCard(m) {
  const card = h("div", { class: "card" });
  const found = !!m.dir && (!!m.exe || m.plugin !== null);
  const same = m.plugin && m.plugin === m.current;
  let status;
  if (!found) status = chip("warn", t("Introuvable", "Not found"));
  else if (!m.plugin) status = chip("warn", t("Plugin absent", "Plugin missing"));
  else if (!same) status = chip("warn", t("Plugin à mettre à jour", "Plugin to update"));
  else if (m.off || m.root_ok === false) status = chip("warn", t("À régler", "To set"));
  else status = chip("ok", t("Plugin à jour", "Plugin up to date"));
  card.append(h("div", { class: "row-h" }, h("h2", {}, "MAME"), h("span", { class: "grow" }), status),
    folderField("mame-dir", "mame", m.dir, "C:\\LaunchBox\\Emulators\\MAME"));
  if (found) {
    if (m.version !== null && m.version !== undefined)
      card.append(check(m.version >= m.min ? "ok" : "bad", m.version >= m.min ? `MAME 0.${m.version}`
        : t(`MAME 0.${m.version}, trop ancien, il faut la 0.${m.min} ou plus récente`, `MAME 0.${m.version}, too old, 0.${m.min} or newer is needed`)));
    if (!m.plugin) card.append(check("bad", t("Le plugin ArcadeDMD n'est pas dans le dossier plugins", "The ArcadeDMD plugin is not in the plugins folder")));
    else card.append(check(same ? "ok" : "warn", same ? t(`Plugin en ${m.plugin}, comme ArcadeDMD`, `Plugin at ${m.plugin}, like ArcadeDMD`)
      : t(`Plugin installé en ${m.plugin}, ArcadeDMD est en ${m.current}`, `Plugin installed at ${m.plugin}, ArcadeDMD is at ${m.current}`)));
    if (m.plugin) card.append(check(m.off ? "bad" : "ok", m.off ? t("Plugin coupé par la ligne arcadedmd 0 de plugin.ini", "Plugin turned off by the line arcadedmd 0 in plugin.ini")
      : t("Plugin activé", "Plugin enabled")));
    if (m.plugin && m.root_ok === false) card.append(check("bad", t("Le plugin cherche ArcadeDMD dans un autre dossier, réinstalle-le", "The plugin looks for ArcadeDMD in another folder, install it again")));
  } else {
    card.append(check("warn", t("Indique le dossier qui contient mame.exe", "Give the folder that holds mame.exe")));
  }
  const btns = h("div", { class: "btns" });
  if (found && (!same || m.root_ok === false)) {
    btns.append(h("button", { class: "btn main", type: "button", onclick: (e) => busy(e.target, async () => {
      const r = await api("/api/emulators/mame/install", { dir: $("mame-dir").value });
      toast(r.ok ? t("Plugin installé.", "Plugin installed.") : (r.text || t("Plugin pas installé.", "Plugin not installed.")), 6000);
      loadEmulators();
    }) }, m.plugin ? t("Mettre à jour le plugin", "Update the plugin") : t("Installer le plugin", "Install the plugin")));
  }
  if (found) btns.append(h("button", { class: "btn", type: "button", onclick: () => api("/api/emulators/open", { what: "mame" }) },
    t("Ouvrir le dossier", "Open the folder")));
  card.append(btns);
  return card;
}

function coinsCard(c, windows) {
  const known = ["left", "right", "start1", "start2"].filter((k) => c[k]).length;
  const card = h("div", { class: "card" },
    h("div", { class: "row-h" }, h("h2", {}, t("Boutons pièce et START", "Coin and START buttons")), h("span", { class: "grow" }),
      known ? chip("ok", t("Appris", "Learned")) : chip("dim", t("Pas appris", "Not learned"))),
    h("div", { class: "soft" }, t("Pour les jeux qui ne disent pas leurs crédits, ArcadeDMD compte les pièces lui-même.",
                                  "For games that do not tell their credits, ArcadeDMD counts the coins itself.")),
    h("div", { class: "pairs" },
      h("span", { class: "dim" }, t("Pièce gauche", "Left coin")), h("span", {}, c.left || "—"),
      h("span", { class: "dim" }, t("Pièce droite", "Right coin")), h("span", {}, c.right || "—"),
      h("span", { class: "dim" }, "START 1"), h("span", {}, c.start1 || "—"),
      h("span", { class: "dim" }, "START 2"), h("span", {}, c.start2 || "—")));
  if (windows)
    card.append(h("div", { class: "btns" }, h("button", { class: "btn", type: "button", onclick: async () => {
      const r = await api("/api/coins/learn", {});
      toast(r.ok ? t("Une console s'ouvre et te demande chaque bouton. ArcadeDMD repart ensuite avec eux.",
                     "A console opens and asks for each button. ArcadeDMD then starts again with them.") : t("Impossible de lancer coin_buttons.bat.", "Could not start coin_buttons.bat."), 7000);
    } }, known ? t("Réapprendre mes boutons", "Learn my buttons again") : t("Apprendre mes boutons", "Learn my buttons"))));
  return card;
}

function recordCard(r, ra) {
  const dir = h("input", { id: "rec-dir", value: r.shots_dir || "", placeholder: ra.shot_dir || "", spellcheck: "false" });
  const card = h("div", { class: "card" },
    h("div", { class: "row-h" }, h("h2", {}, t("Enregistrer les parties", "Record the games"))),
    h("div", { class: "soft" }, t("Ce qu'il faut pour apprendre un jeu, chaque valeur lue avec son heure, et pour RetroArch la mémoire et des captures d'écran.",
                                  "What it takes to learn a game, each value read with its time, and for RetroArch the memory and screenshots.")),
    field(t("Parties enregistrées", "Games recorded"), select("rec-cap", [["all", t("Tous les jeux", "All games")],
      ["fights", t("Les jeux de combat", "Fighting games")], ["off", t("Aucune", "None")]], r.capture)),
    h("label", { class: "check" }, h("input", { type: "checkbox", id: "rec-ram", checked: r.ram }),
      t("Toute la mémoire de RetroArch, pour trouver une adresse", "The whole RetroArch memory, to find an address")),
    h("label", { class: "check" }, h("input", { type: "checkbox", id: "rec-shots", checked: r.shots }),
      t("Des captures d'écran de RetroArch", "RetroArch screenshots")),
    h("div", { class: "field" }, t("Dossier des captures d'écran de RetroArch", "RetroArch's screenshot folder"),
      h("div", { class: "inline" }, dir, ra.shot_dir ? h("button", { class: "btn", type: "button", onclick: () => { dir.value = ra.shot_dir; } },
        t("Prendre celui de RetroArch", "Take RetroArch's")) : null)),
    h("div", { class: "btns" },
      h("button", { class: "btn main", type: "button", onclick: (e) => busy(e.target, async () => saved(await api("/api/emulators/record", {
        capture: $("rec-cap").value, ram: $("rec-ram").checked, shots: $("rec-shots").checked, shots_dir: dir.value.trim() }))) },
        t("Enregistrer", "Save")),
      h("button", { class: "btn", type: "button", onclick: () => api("/api/emulators/open", { what: "captures" }) },
        t("Ouvrir le dossier des captures", "Open the captures folder")),
      h("button", { class: "btn", type: "button", disabled: !r.last, onclick: (e) => busy(e.target, async () => {
        const p = await api("/api/captures/pack", {});
        toast(p.ok ? t(`${p.file} est prêt à envoyer, ${Math.round(p.size / 1024)} Ko, dans le dossier runtime.`,
                       `${p.file} is ready to send, ${Math.round(p.size / 1024)} KB, in the runtime folder.`) : (p.error || ""), 8000);
      }) }, t("Préparer l'envoi de la dernière partie", "Get the last game ready to send"))),
    r.last ? h("span", { class: "small" }, t(`Dernière partie enregistrée ${r.last}`, `Last game recorded ${r.last}`)) : null);
  return card;
}
