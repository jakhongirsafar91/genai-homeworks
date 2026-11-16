"""Northstar recipe: rebuild the 3 report charts from a monthly sales CSV.

Standard library only. Usage:  python sales_recipe.py northstar_sales_2026-01.csv charts.html

Cleaning (same rules as the 2025 analysis): exact duplicate rows are dropped,
text dates like 10/05/2025 are read as DD/MM/YYYY. Zero ad_spend on Email and
Organic is normal, so ROAS is calculated for Search and Social only.
NOT rebuilt: the reviews chart - the monthly file has sales only, no reviews.
"""
import argparse, csv, html
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ACCENT, GREY = "#d9480f", "#b8bfc9"

def parse_date(text):
    text = text.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Unreadable date: {text!r}")

def load(source):
    with Path(source).open(encoding="utf-8-sig", newline="") as f:
        raw = list(csv.DictReader(f))
    seen, rows = set(), []
    for r in raw:
        key = tuple(r.values())
        if key in seen:
            continue
        seen.add(key)
        r["d"] = parse_date(r["order_date"])
        for c in ("orders", "returns"):
            r[c] = int(r[c])
        for c in ("revenue", "ad_spend"):
            r[c] = float(r[c])
        rows.append(r)
    print(f"Rows before cleaning: {len(raw)}, after: {len(rows)}")
    return rows

def bar_chart(items, fmt, highlight):
    """items = [(label, value)]; the highlighted label gets the accent colour."""
    top = max([v for _, v in items] or [1]) or 1
    out = [f"<svg viewBox='0 0 700 {len(items) * 34 + 10}' width='700' font-family='sans-serif' font-size='14'>"]
    for i, (label, v) in enumerate(items):
        y, w = 6 + i * 34, v / top * 420
        bold = " font-weight='bold'" if label == highlight else ""
        out.append(f"<text x='0' y='{y + 17}'>{html.escape(label)}</text>")
        out.append(f"<rect x='170' y='{y}' width='{w:.1f}' height='24' fill='{ACCENT if label == highlight else GREY}'/>")
        out.append(f"<text x='{176 + w:.1f}' y='{y + 17}'{bold}>{fmt(v)}</text>")
    return "".join(out) + "</svg>"

def run(source, output):
    rows = load(source)
    first, last = min(r["d"] for r in rows), max(r["d"] for r in rows)
    print(f"Period: {first} to {last}")

    # Chart 1: revenue by month (by week if the file holds a single month)
    one_month = len({(r["d"].year, r["d"].month) for r in rows}) == 1
    rev = defaultdict(float)
    for r in rows:
        k = (r["d"] - timedelta(days=r["d"].weekday())).isoformat() if one_month else r["d"].strftime("%Y-%m")
        rev[k] += r["revenue"]
    c1 = sorted(rev.items())
    unit = "week starting" if one_month else "month"
    best = max(c1, key=lambda x: x[1])
    t1 = f"Revenue peaked in the {unit} {best[0]}: ${best[1]:,.0f} of ${sum(rev.values()):,.0f} total"

    # Chart 2: revenue per $1 of ads, Search and Social only, by month
    ads = defaultdict(lambda: [0.0, 0.0])
    for r in rows:
        if r["channel"] in ("Search", "Social"):
            k = (r["channel"], r["d"].strftime("%Y-%m"))
            ads[k][0] += r["revenue"]; ads[k][1] += r["ad_spend"]
    c2 = [(f"{c} {m}", rv / sp) for (c, m), (rv, sp) in sorted(ads.items()) if sp]
    low = min(c2, key=lambda x: x[1])
    t2 = f"Lowest revenue per $1 of ads: {low[0]} at ${low[1]:.2f}"

    # Chart 3: return rate = returns / orders, by warehouse, whole file, sorted
    wh = defaultdict(lambda: [0, 0])
    for r in rows:
        wh[r["warehouse"]][0] += r["returns"]; wh[r["warehouse"]][1] += r["orders"]
    c3 = sorted(((k, 100 * a / b) for k, (a, b) in wh.items() if b), key=lambda x: -x[1])
    t3 = f"Highest return rate: {c3[0][0]} at {c3[0][1]:.1f}% of orders ({first:%d %b}-{last:%d %b %Y})"

    parts = ["<!doctype html><html lang='en'><meta charset='utf-8'><title>Northstar sales charts</title>",
             "<body style='font-family:sans-serif;max-width:760px;margin:24px auto'>",
             f"<p>Source: {html.escape(Path(source).name)} | {len(rows)} cleaned rows | {first} to {last}</p>"]
    for title, svg in ((t1, bar_chart(c1, lambda v: f"${v:,.0f}", best[0])),
                       (t2, bar_chart(c2, lambda v: f"${v:.2f}", low[0])),
                       (t3, bar_chart(c3, lambda v: f"{v:.1f}%", c3[0][0]))):
        parts.append(f"<h2>{html.escape(title)}</h2>{svg}")
    parts.append("<p><i>Reviews chart not rebuilt: the monthly file has sales only, no reviews.</i></p></body></html>")
    Path(output).write_text("\n".join(parts), encoding="utf-8")
    print(t1); print(t2); print(t3); print("Created", output)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input"); p.add_argument("output")
    a = p.parse_args(); run(a.input, a.output)
