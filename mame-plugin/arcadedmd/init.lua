-- license:MIT
-- ArcadeDMD : plugin MAME
-- Lit des valeurs dans la RAM du jeu (score, vies, credits...) selon les fichiers
-- <root>/games/*.json et les ecrit dans <root>/runtime/events.jsonl pour le moteur
-- d'affichage (arcadedmd.py). Sert aussi a capturer la RAM pour l'outil d'apprentissage.

local exports = {
	name = "arcadedmd",
	version = "1.3.2",
	description = "ArcadeDMD",
	license = "MIT",
	author = { name = "ArcadeDMD" } }

local arcadedmd = exports

local plugin_dir = nil
local subs = {}            -- notifier subscriptions (must stay referenced)

function arcadedmd.set_folder(path)
	plugin_dir = path
end

----------------------------------------------------------------------------
-- helpers
----------------------------------------------------------------------------

local function log(msg)
	emu.print_info("[arcadedmd] " .. msg)
end

local function log_error(msg)
	emu.print_error("[arcadedmd] " .. msg)
end

local function read_file(path)
	local f = io.open(path, "rb")
	if not f then return nil end
	local data = f:read("a")
	f:close()
	return data
end

local function dir_exists(path)
	return lfs and lfs.attributes(path, "mode") == "directory"
end

local function ensure_dir(path)
	if dir_exists(path) then return true end
	if lfs then
		lfs.mkdir(path)
	end
	return dir_exists(path)
end

local function file_exists(path)
	local f = io.open(path, "rb")
	if f then f:close() return true end
	return false
end

local function sanitize(name)
	return (tostring(name or "unknown"):gsub("[^%w%-_]", "_"))
end

-- minimal JSON encoder (numbers, strings, booleans, arrays, objects)
local function json_val(v)
	local t = type(v)
	if t == "number" then
		if math.type(v) == "integer" then return string.format("%d", v) end
		if v == math.floor(v) and math.abs(v) < 2^53 then return string.format("%d", math.tointeger(v)) end
		return string.format("%.6g", v)
	elseif t == "string" then
		return '"' .. v:gsub('[%c"\\]', function(c) return string.format("\\u%04x", c:byte()) end) .. '"'
	elseif t == "boolean" then
		return tostring(v)
	elseif t == "table" then
		if #v > 0 then
			local parts = {}
			for i, x in ipairs(v) do parts[i] = json_val(x) end
			return "[" .. table.concat(parts, ",") .. "]"
		end
		local parts = {}
		for k, x in pairs(v) do
			parts[#parts + 1] = json_val(tostring(k)) .. ":" .. json_val(x)
		end
		return "{" .. table.concat(parts, ",") .. "}"
	end
	return "null"
end

local function parse_addr(v)
	if type(v) == "number" then return math.tointeger(v) end
	if type(v) == "string" then
		local s = v:gsub("^%s+", ""):gsub("%s+$", ""):gsub("^0[xX]", ""):gsub("^%$", "")
		return tonumber(s, 16)
	end
	return nil
end

----------------------------------------------------------------------------
-- settings & game configs
----------------------------------------------------------------------------

local settings = {
	root = "C:/ArcadeDMD",
	capture_key = "KEYCODE_RCONTROL KEYCODE_D",
	poll_frames = 2,
	heartbeat_seconds = 2,
}

local function load_settings()
	local json = require("json")
	local candidates = {}
	if plugin_dir then candidates[#candidates + 1] = plugin_dir .. "/settings.json" end
	for _, path in ipairs(candidates) do
		local data = read_file(path)
		if data then
			local ok, parsed = pcall(json.parse, data)
			if ok and type(parsed) == "table" then
				for k, v in pairs(parsed) do settings[k] = v end
				log("settings loaded from " .. path)
			else
				log_error("settings.json invalide : " .. path)
			end
			break
		end
	end
	settings.root = tostring(settings.root):gsub("\\", "/"):gsub("/+$", "")
	settings.poll_frames = math.max(1, math.tointeger(settings.poll_frames) or 2)
end

local function load_games()
	local json = require("json")
	local games = {}
	local dir = settings.root .. "/games"
	if not dir_exists(dir) then
		log_error("dossier introuvable : " .. dir)
		return games
	end
	local names = {}
	for name in lfs.dir(dir) do
		if name:match("%.json$") and not name:match("^_") then names[#names + 1] = name end
	end
	table.sort(names)
	for _, name in ipairs(names) do
		local data = read_file(dir .. "/" .. name)
		if data then
			local ok, parsed = pcall(json.parse, data)
			if ok and type(parsed) == "table" then
				parsed._key = name:gsub("%.json$", "")
				games[#games + 1] = parsed
			else
				log_error("JSON invalide : " .. name)
			end
		end
	end
	return games
end

----------------------------------------------------------------------------
-- machine identification
----------------------------------------------------------------------------

-- propriete (MAME recents) ou methode (versions plus anciennes)
local function prop(obj, name)
	local ok, v = pcall(function() return obj[name] end)
	if not ok then return nil end
	if type(v) == "function" then
		local ok2, r = pcall(v, obj)
		if ok2 then return r end
		return nil
	end
	return v
end

local function machine_info()
	local m = manager.machine
	local sys = m.system
	local info = {
		system = sys.name,
		parent = (sys.parent and sys.parent ~= "0" and sys.parent ~= "") and sys.parent or nil,
		description = sys.description,
		manufacturer = sys.manufacturer,
		year = sys.year,
		media = {},
	}
	for tag, img in pairs(m.images) do
		if prop(img, "exists") then
			local fname = tostring(prop(img, "filename") or "")
			local base = fname:match("([^/\\]+)$") or fname
			base = base:gsub("%.[^%.]+$", "")
			info.media[#info.media + 1] = {
				tag = tag,
				file = base,
				longname = prop(img, "software_longname"),
				list = prop(img, "software_list_name"),
				parent = prop(img, "software_parent"),
			}
		end
	end
	return info
end

local function lower(s)
	return s and string.lower(tostring(s)) or ""
end

local function list_has(list, value)
	if type(list) ~= "table" or not value then return false end
	for _, s in ipairs(list) do
		if s == value then return true end
	end
	return false
end

local function software_hay(info)
	local hay = {}
	for _, media in ipairs(info.media) do
		hay[#hay + 1] = lower(media.file) .. "|" .. lower(media.longname) .. "|" .. lower(media.parent)
	end
	return table.concat(hay, "||")
end

local function match_rule(mt, info)
	if type(mt) ~= "table" then return false end
	if mt.system then
		if not (list_has(mt.system, info.system) or list_has(mt.system, info.parent)) then
			return false
		end
	end
	local hay = software_hay(info)
	if mt.software then
		local found = false
		for _, pat in ipairs(mt.software) do
			if hay:find(lower(pat), 1, true) then found = true break end
		end
		if not found then return false end
	end
	if mt.software_not then
		for _, pat in ipairs(mt.software_not) do
			if hay:find(lower(pat), 1, true) then return false end
		end
	end
	return mt.system ~= nil or mt.software ~= nil
end

-- "match" is either one rule or a list of rules (any rule may match)
local function matches(game, info)
	local mt = game.match
	if type(mt) ~= "table" then return false end
	if #mt > 0 then
		for _, rule in ipairs(mt) do
			if match_rule(rule, info) then return true end
		end
		return false
	end
	return match_rule(mt, info)
end

----------------------------------------------------------------------------
-- memory readers
----------------------------------------------------------------------------

local function find_space(tag, spacename)
	local dev = manager.machine.devices[tag]
	if not dev then return nil end
	local ok, space = pcall(function() return dev.spaces[spacename or "program"] end)
	if ok then return space end
	return nil
end

local function default_cpu_tag()
	if manager.machine.devices[":maincpu"] then return ":maincpu" end
	for tag, dev in pairs(manager.machine.devices) do
		local ok, sp = pcall(function() return dev.spaces["program"] end)
		if ok and sp and dev.state then return tag end
	end
	return ":maincpu"
end

local function make_reader(space, def)
	local addr = parse_addr(def.addr)
	if not space or not addr then return nil end
	local t = def.type or "u8"
	local nbytes = math.tointeger(def.bytes) or ((t:find("32") and 4) or (t:find("16") and 2) or 1)
	local mult = def.mult or 1
	local add = def.add or 0
	local vmin = tonumber(def.min)
	local vmax = tonumber(def.max)
	local mask = parse_addr(def.mask)
	local shift = math.tointeger(def.shift)
	local doff = parse_addr(def.digit_offset) or 0
	local raw
	if t == "u8" then
		raw = function() return space:read_u8(addr) end
	elseif t == "u16" then
		raw = function() return space:read_u16(addr) end
	elseif t == "u32" then
		raw = function() return space:read_u32(addr) end
	elseif t == "s8" then
		raw = function() local v = space:read_u8(addr) if v >= 0x80 then v = v - 0x100 end return v end
	elseif t == "s16" then
		raw = function() local v = space:read_u16(addr) if v >= 0x8000 then v = v - 0x10000 end return v end
	elseif t == "be" or t == "le" then
		raw = function()
			local v = 0
			for i = 0, nbytes - 1 do
				local b = space:read_u8(addr + ((t == "be") and i or (nbytes - 1 - i)))
				v = v * 256 + b
			end
			return v
		end
	elseif t == "bcd" or t == "bcd_le" then
		raw = function()
			local v = 0
			for i = 0, nbytes - 1 do
				local b = space:read_u8(addr + ((t == "bcd") and i or (nbytes - 1 - i)))
				local hi, lo = b >> 4, b & 15
				if hi > 9 then hi = 0 end
				if lo > 9 then lo = 0 end
				v = v * 100 + hi * 10 + lo
			end
			return v
		end
	elseif t == "digits" or t == "digits_le" then
		raw = function()
			local v = 0
			for i = 0, nbytes - 1 do
				local d = space:read_u8(addr + ((t == "digits") and i or (nbytes - 1 - i))) - doff
				if d < 0 or d > 9 then d = 0 end
				v = v * 10 + d
			end
			return v
		end
	else
		log_error("type inconnu : " .. tostring(t))
		return nil
	end
	return function()
		local v = raw()
		if mask then v = v & mask end
		if shift then v = v >> shift end
		v = v * mult + add
		if vmin and v < vmin then v = vmin end
		if vmax and v > vmax then v = vmax end
		if math.type(v) == "float" and v == math.floor(v) then v = math.tointeger(v) or v end
		return v
	end
end

----------------------------------------------------------------------------
-- events file
----------------------------------------------------------------------------

local ev_file = nil

local close_events

local function open_events()
	if close_events then close_events() end
	local rt = settings.root .. "/runtime"
	ensure_dir(settings.root)
	ensure_dir(rt)
	local path = rt .. "/events.jsonl"
	local f = io.open(path, "w")      -- truncate previous session
	if f then f:close() end
	ev_file = io.open(path, "a")
	if ev_file then
		ev_file:setvbuf("no")
		log("events -> " .. path)
	else
		log_error("impossible d'ecrire " .. path)
	end
end

local function emit(tbl)
	if not ev_file then return end
	local ok = pcall(function() ev_file:write(json_val(tbl) .. "\n") end)
	if not ok then
		ev_file = nil
		log_error("ecriture des evenements interrompue")
	end
end

close_events = function()
	if ev_file then
		pcall(function() ev_file:close() end)
		ev_file = nil
	end
end

----------------------------------------------------------------------------
-- session
----------------------------------------------------------------------------

local session = nil

local function start_session()
	local info = machine_info()
	local games = load_games()
	local game = nil
	for _, g in ipairs(games) do
		if matches(g, info) then game = g break end
	end
	local mem = (game and game.memory) or {}
	local cpu_tag = mem.cpu or default_cpu_tag()
	local space = find_space(cpu_tag, mem.space)
	if not space then
		log_error("CPU introuvable : " .. tostring(cpu_tag) .. " (verifier \"cpu\" dans le fichier du jeu)")
	end
	local readers, names = {}, {}
	if type(mem.values) == "table" then
		for name, def in pairs(mem.values) do
			if type(def) == "table" and def.addr ~= nil and def.addr ~= "" then
				local sp = space
				if def.cpu then sp = find_space(def.cpu, def.space or mem.space) end
				local r = make_reader(sp, def)
				if r then
					local ok = pcall(r)
					if ok then
						readers[name] = r
						names[#names + 1] = name
					else
						log_error("lecture impossible pour " .. name)
					end
				end
			end
		end
	end
	table.sort(names)
	session = {
		info = info,
		game = game,
		key = game and game._key or nil,
		cpu_tag = cpu_tag,
		space = space,
		readers = readers,
		names = names,
		last = {},
		frame = 0,
		last_hb = os.time(),
		capture_seq = nil,
		capture_was = false,
		captures = 0,
		paused = false,
	}
	local ok, seq = pcall(function() return manager.machine.input:seq_from_tokens(settings.capture_key) end)
	if ok then session.capture_seq = seq end

	open_events()
	emit({
		t = "start",
		game = session.key or "",
		system = info.system,
		parent = info.parent or "",
		description = info.description,
		manufacturer = info.manufacturer,
		year = info.year,
		media = info.media,
		values = names,
		plugin = exports.version,
		mame = emu.app_version(),
	})
	log(string.format("jeu %s (%s) -> config %s, %d valeur(s)", info.system, info.description, tostring(session.key), #names))
end

local function read_all()
	local vals = {}
	for _, name in ipairs(session.names) do
		local ok, v = pcall(session.readers[name])
		if ok then vals[name] = v end
	end
	return vals
end

----------------------------------------------------------------------------
-- RAM capture for the learning tool
----------------------------------------------------------------------------

local function write_bmp(path, pixels, w, h)
	-- pixels: 32-bit little-endian ARGB (bytes B,G,R,A); BMP wants bottom-up BGR rows
	local f = io.open(path, "wb")
	if not f then return false end
	local rowbytes = w * 3
	local pad = (4 - rowbytes % 4) % 4
	local datasize = (rowbytes + pad) * h
	local function u32(v) return string.pack("<I4", v) end
	local function u16(v) return string.pack("<I2", v) end
	f:write("BM", u32(54 + datasize), u32(0), u32(54))
	f:write(u32(40), u32(w), u32(h), u16(1), u16(24), u32(0), u32(datasize), u32(2835), u32(2835), u32(0), u32(0))
	local padding = string.rep("\0", pad)
	for y = h - 1, 0, -1 do
		local row = pixels:sub(y * w * 4 + 1, (y + 1) * w * 4)
		row = row:gsub("(...).", "%1")
		f:write(row, padding)
	end
	f:close()
	return true
end

local function capture_ranges()
	local ranges = {}
	local mem = (session.game and session.game.memory) or {}
	if type(mem.learn_ranges) == "table" and #mem.learn_ranges > 0 then
		for _, r in ipairs(mem.learn_ranges) do
			local s, e = parse_addr(r[1]), parse_addr(r[2])
			if s and e and e >= s then ranges[#ranges + 1] = { s = s, e = e } end
		end
		return ranges
	end
	local seen = {}
	local ok, entries = pcall(function() return session.space.map.entries end)
	if not ok or not entries then return ranges end
	for _, e in ipairs(entries) do
		local rtype = e.read and e.read.handlertype
		if rtype == "ram" then
			local size = e.address_end - e.address_start + 1
			local share = e.share
			if size > 0 and size <= 0x200000 and not (share and seen[share]) then
				if share then seen[share] = true end
				-- use the highest mirror (e.g. Mega Drive RAM E00000 -> FF0000, the address games use)
				local m = e.address_mirror or 0
				ranges[#ranges + 1] = { s = e.address_start | m, e = e.address_end | m, share = share }
			end
		end
	end
	return ranges
end

local function capture()
	if not session or not session.space then
		manager.machine:popmessage("ArcadeDMD : capture impossible (CPU introuvable)")
		return
	end
	local key = sanitize(session.key or session.info.system)
	local base = settings.root .. "/runtime/learn"
	ensure_dir(settings.root .. "/runtime")
	ensure_dir(base)
	local dir = base .. "/" .. key
	ensure_dir(dir)
	local n = 1
	while file_exists(string.format("%s/snap_%03d.json", dir, n)) do n = n + 1 end
	local stem = string.format("%s/snap_%03d", dir, n)
	local ranges = capture_ranges()
	local f = io.open(stem .. ".bin", "wb")
	if not f then
		manager.machine:popmessage("ArcadeDMD : ecriture impossible dans " .. dir)
		return
	end
	local offset = 0
	local out_ranges = {}
	local space = session.space
	local amask = space.address_mask or 0xFFFFFFFF
	for _, r in ipairs(ranges) do
		-- read_range refuses addresses above the space mask (e.g. FF8000 on X-Board, mask 3FFFFF),
		-- so read the masked equivalent but keep the address the game uses in the metadata
		local rs, re = r.s & amask, r.e & amask
		local ok, data
		if re >= rs and (re - rs) == (r.e - r.s) then
			ok, data = pcall(function() return space:read_range(rs, re, 8) end)
		end
		if not (ok and type(data) == "string") then
			ok, data = pcall(function()
				local parts = {}
				for a = r.s, r.e do parts[#parts + 1] = string.char(space:read_u8(a)) end
				return table.concat(parts)
			end)
		end
		if ok and type(data) == "string" then
			f:write(data)
			out_ranges[#out_ranges + 1] = { start = r.s, ["end"] = r.e, offset = offset, length = #data, share = r.share or "" }
			offset = offset + #data
		else
			log_error(string.format("zone %X-%X illisible", r.s, r.e))
		end
	end
	f:close()
	local meta = {
		n = n,
		game = session.key or "",
		system = session.info.system,
		description = session.info.description,
		cpu = session.cpu_tag,
		space = "program",
		frame = session.frame,
		time = os.time(),
		ranges = out_ranges,
		values = session.last,
	}
	local jf = io.open(stem .. ".json", "w")
	if jf then jf:write(json_val(meta)) jf:close() end
	-- screenshot of the emulated screen (no UI overlay)
	for _, scr in pairs(manager.machine.screens) do
		local ok, pixels, w, h = pcall(function() return scr:pixels() end)
		if ok and type(pixels) == "string" and w and h and w > 0 then
			write_bmp(stem .. ".bmp", pixels, w, h)
		end
		break
	end
	session.captures = session.captures + 1
	manager.machine:popmessage(string.format("ArcadeDMD : capture %d enregistree", n))
	emit({ t = "capture", n = n, game = key })
	log(string.format("capture %d -> %s (%d octets)", n, stem, offset))
end

----------------------------------------------------------------------------
-- per-frame work
----------------------------------------------------------------------------

local function on_frame()
	if not session then return end
	session.frame = session.frame + 1

	if session.capture_seq then
		local ok, pressed = pcall(function() return manager.machine.input:seq_pressed(session.capture_seq) end)
		pressed = ok and pressed
		if pressed and not session.capture_was then capture() end
		session.capture_was = pressed
	end
	-- test hook: automatic captures at given frame numbers
	if type(settings.debug_capture_frames) == "table" then
		for _, f in ipairs(settings.debug_capture_frames) do
			if session.frame == f then capture() end
		end
	end

	if session.frame % settings.poll_frames ~= 0 then return end
	if #session.names == 0 then return end

	local vals = read_all()
	local changed, any = {}, false
	for name, v in pairs(vals) do
		if session.last[name] ~= v then
			changed[name] = v
			session.last[name] = v
			any = true
		end
	end
	if any then emit({ t = "v", v = changed }) end
	local now = os.time()
	if now - session.last_hb >= (settings.heartbeat_seconds or 2) then
		session.last_hb = now
		emit({ t = "hb", v = session.last })
	end
end

----------------------------------------------------------------------------
-- MAME menu (Tab > Options des plugins > ArcadeDMD)
----------------------------------------------------------------------------

local menu_capture_index = nil

local function menu_populate()
	local items = {}
	items[#items + 1] = { "ArcadeDMD " .. exports.version, "", "off" }
	items[#items + 1] = { "---", "", "" }
	if session then
		items[#items + 1] = { "Jeu", session.info.system, "off" }
		items[#items + 1] = { "Configuration", session.key or "aucune (scene generique)", "off" }
		items[#items + 1] = { "CPU", session.cpu_tag .. (session.space and "" or " (introuvable)"), "off" }
		for _, name in ipairs(session.names) do
			local v = session.last[name]
			items[#items + 1] = { name, v ~= nil and tostring(v) or "-", "off" }
		end
		items[#items + 1] = { "---", "", "" }
		items[#items + 1] = { "Capturer la RAM (apprentissage)", tostring(session.captures) .. " capture(s)", "" }
		menu_capture_index = #items
	end
	return items
end

local function menu_callback(index, event)
	if event == "select" and index == menu_capture_index then
		capture()
		return true
	end
	return false
end

----------------------------------------------------------------------------
-- plugin entry point
----------------------------------------------------------------------------

-- MAME 0.254 et plus : emu.add_machine_*_notifier
-- MAME 0.227 a 0.253 : anciennes fonctions emu.register_*
local LEGACY = { reset = "register_start", frame = "register_frame_done", stop = "register_stop",
                 pause = "register_pause", resume = "register_resume" }

local function subscribe(kind, fn)
	local add = emu["add_machine_" .. kind .. "_notifier"]
	if add and not settings.legacy_callbacks then
		subs[kind] = add(fn)
		return true
	end
	local old = emu[LEGACY[kind]]
	if old then
		old(fn)
		subs[kind] = true
		return true
	end
	log_error("version de MAME trop ancienne (ni add_machine_" .. kind .. "_notifier ni " .. LEGACY[kind] .. ")")
	return false
end

function arcadedmd.startplugin()
	load_settings()

	subscribe("reset", function()
		local ok, err = pcall(start_session)
		if not ok then log_error("demarrage : " .. tostring(err)) end
	end)

	subscribe("frame", function()
		local ok, err = pcall(on_frame)
		if not ok then
			log_error("frame : " .. tostring(err))
			session = nil
		end
	end)

	subscribe("stop", function()
		emit({ t = "stop" })
		close_events()
		session = nil
	end)

	subscribe("pause", function()
		if session then emit({ t = "pause" }) end
	end)

	subscribe("resume", function()
		if session then emit({ t = "resume" }) end
	end)

	if emu.register_menu then
		emu.register_menu(menu_callback, menu_populate, "ArcadeDMD")
	end
end

return exports
