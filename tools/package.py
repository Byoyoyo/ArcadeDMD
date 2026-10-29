"""Builds the release zip (dist/ArcadeDMD-<version>.zip) and its notes (dist/notes.md).

Checks first that the version is the same in dmd/app.py, the MAME plugin (plugin.json, init.lua)
and that CHANGELOG.md has a section for it. Used by the GitHub release workflow, and by hand.

Construit le zip de la version et ses notes, après avoir vérifié que la version est partout la même.

usage: python tools/package.py [--out dist] [--check] [--github-output FILE]
"""
import argparse
import json
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# shipped in the zip: everything except these (development files, user data, caches)
EXCLUDE_DIRS = {".git", ".github", "tools", "dist", "runtime", "learned", "appris", "appris.old", "obs", "artwork",
                "__pycache__"}
EXCLUDE_FILES = {"config.json", ".gitignore", ".gitattributes", "CONTRIBUTING.md"}
EXCLUDE_EXT = (".pyc", ".pyo", ".log", ".tmp")
REQUIRED = ["arcadedmd.py", "install.bat", "run.bat", "learn.bat", "config.default.json", "README.md", "README.fr.md",
            "CHANGELOG.md", "LICENSE", "dmd/app.py", "dmd/lang.bat", "dmd/find_python.bat", "dmd/hd.py",
            "mame-plugin/arcadedmd/init.lua", "mame-plugin/arcadedmd/plugin.json", "games/_generic.json",
            "fonts/OFL.txt"]


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def versions():
    app = re.search(r'^VERSION = "([^"]+)"', read("dmd/app.py"), re.M)
    plugin = json.loads(read("mame-plugin/arcadedmd/plugin.json"))["plugin"]["version"]
    lua = re.search(r'^\s*version = "([^"]+)"', read("mame-plugin/arcadedmd/init.lua"), re.M)
    return {"dmd/app.py": app and app.group(1), "plugin.json": plugin, "init.lua": lua and lua.group(1)}


def notes(version):
    """Section of CHANGELOG.md for this version, without its title."""
    text = read("CHANGELOG.md")
    m = re.search(r"^## " + re.escape(version) + r"\b[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else None


def files():
    out = []
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith("."))
        for n in sorted(names):
            rel = os.path.relpath(os.path.join(base, n), ROOT).replace(os.sep, "/")
            if n in EXCLUDE_FILES or n.endswith(EXCLUDE_EXT) or n.startswith("."):
                continue
            out.append(rel)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"))
    ap.add_argument("--check", action="store_true", help="only check, write nothing")
    ap.add_argument("--github-output", default="")
    args = ap.parse_args()

    v = versions()
    problems = []
    if len(set(v.values())) != 1 or None in v.values():
        problems.append("version differs: " + ", ".join(f"{k} {val}" for k, val in v.items()))
    version = v["dmd/app.py"]
    body = notes(version) if version else None
    if not body:
        problems.append(f"CHANGELOG.md has no section '## {version}'")
    listed = files()
    missing = [r for r in REQUIRED if r not in listed]
    if missing:
        problems.append("missing files: " + ", ".join(missing))
    for rel in listed:
        if rel.endswith(".json"):
            try:
                json.loads(read(rel))
            except ValueError as e:
                problems.append(f"{rel}: invalid JSON ({e})")
        if rel.endswith(".bat"):
            with open(os.path.join(ROOT, rel), "rb") as f:
                data = f.read()
            if b"\n" in data.replace(b"\r\n", b""):
                problems.append(f"{rel}: needs Windows line endings (CRLF)")
    if problems:
        for p in problems:
            print("ERROR", p)
        return 1
    print(f"ArcadeDMD {version}, {len(listed)} files")
    if args.check:
        return 0

    os.makedirs(args.out, exist_ok=True)
    zpath = os.path.join(args.out, f"ArcadeDMD-{version}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in listed:
            z.write(os.path.join(ROOT, rel), "ArcadeDMD/" + rel)
    with open(os.path.join(args.out, "notes.md"), "w", encoding="utf-8") as f:
        f.write(body + "\n\n---\n\nInstall or update: download `ArcadeDMD-" + version + ".zip` below, then see "
                "[README.md](https://github.com/" + os.environ.get("GITHUB_REPOSITORY", "") + "/blob/main/README.md). "
                "Installer ou mettre à jour : télécharge `ArcadeDMD-" + version + ".zip` ci-dessous, puis vois "
                "[README.fr.md](https://github.com/" + os.environ.get("GITHUB_REPOSITORY", "") + "/blob/main/README.fr.md).\n")
    print("written", zpath, os.path.getsize(zpath), "bytes")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as f:
            f.write(f"version={version}\nzip={zpath}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
