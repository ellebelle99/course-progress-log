"""Render and recalculate a course progress log.

  python build_log.py build spec.json out.md   spec.json -> new log
  python build_log.py recalc log.md            re-sum totals in an existing log

spec.json: {"title", "url", "platform" (optional, default "LinkedIn Learning"),
            "chapters": [{"name", "episodes": [{"name", "time", "done"}]}]}
Times are strings as shown on the platform: "1h 5m 10s", "3m 13s", "39s", "1m".
"""
import json
import re
import sys

LEGEND = ("Done: [x] watched (green tick), [ ] not finished. "
          "Durations as shown on LinkedIn; totals are summed.")


def seconds(t):
    h = re.search(r"(\d+)h", t)
    m = re.search(r"(\d+)m", t)
    s = re.search(r"(\d+)s", t)
    return ((int(h.group(1)) * 3600 if h else 0)
            + (int(m.group(1)) * 60 if m else 0)
            + (int(s.group(1)) if s else 0))


def fmt(x):
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    return (f"{h}h " if h else "") + (f"{m}m " if h or m else "") + f"{s}s"


def render(spec):
    out = [f"# {spec['title']}", "",
           f"{spec.get('platform', 'LinkedIn Learning')}: {spec['url']}", "",
           LEGEND, ""]
    total = done_total = 0
    body = []
    for ch in spec["chapters"]:
        eps = ch["episodes"]
        s = sum(seconds(e["time"]) for e in eps)
        d = sum(seconds(e["time"]) for e in eps if e["done"])
        total += s
        done_total += d
        body += [f"## {ch['name']}", f"Total: {fmt(s)} | Done: {fmt(d)}", "",
                 "| Done | Episode | Time |", "|---|---|---|"]
        body += [f"| {'[x]' if e['done'] else '[ ]'} | {e['name']} | {e['time']} |"
                 for e in eps]
        body.append("")
    out += [f"**Course total: {fmt(total)}** | **Done: {fmt(done_total)}** "
            f"| Remaining: {fmt(total - done_total)}", ""]
    return "\n".join(out + body)


def parse(text):
    lines = text.split("\n")
    if not lines[0].startswith("# ") or ": " not in lines[2]:
        raise SystemExit("not a course log: header lines missing")
    platform, url = lines[2].split(": ", 1)
    spec = {"title": lines[0][2:], "platform": platform, "url": url,
            "chapters": []}
    for line in lines[3:]:
        if line.startswith("## "):
            spec["chapters"].append({"name": line[3:], "episodes": []})
        elif line.startswith("| [") and spec["chapters"]:
            mark, name, time = [c.strip() for c in line.strip("|").split("|")]
            if mark not in ("[x]", "[ ]"):
                raise SystemExit(f"bad Done mark in row: {line}")
            spec["chapters"][-1]["episodes"].append(
                {"name": name, "time": time, "done": mark == "[x]"})
    return spec


def main(argv):
    if len(argv) == 4 and argv[1] == "build":
        spec = json.load(open(argv[2], encoding="utf-8"))
        open(argv[3], "w", encoding="utf-8").write(render(spec))
    elif len(argv) == 3 and argv[1] == "recalc":
        spec = parse(open(argv[2], encoding="utf-8").read())
        open(argv[2], "w", encoding="utf-8").write(render(spec))
    else:
        raise SystemExit(__doc__)
    n = sum(len(c["episodes"]) for c in spec["chapters"])
    print(f"{len(spec['chapters'])} chapters, {n} episodes")
    print(render(spec).split("\n")[6])


if __name__ == "__main__":
    main(sys.argv)
