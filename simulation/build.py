"""Embed data/*.csv into index.html so the page needs no runtime fetch.
Run this after editing any CSV in data/:  python build.py
"""
import re, pathlib
root = pathlib.Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")
names = ["gate_details", "gate_activity", "performance_schedule", "weather", "equipment_downtime"]
for n in names:
    csv = (root / "data" / f"{n}.csv").read_text(encoding="utf-8").replace("</script", r"<\/script")
    block = f'<script type="text/csv" id="csv-{n}">\n{csv.strip()}\n</script>'
    pat = re.compile(rf'<script type="text/csv" id="csv-{n}">.*?</script>', re.S)
    html = pat.sub(lambda m: block, html, count=1) if pat.search(html) else html.replace("<script>\n'use strict';", block + "\n<script>\n'use strict';", 1)
(root / "index.html").write_text(html, encoding="utf-8")
print("embedded", ", ".join(names))
