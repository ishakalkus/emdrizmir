#!/usr/bin/env python3
"""Eski adreslerin hepsini yeni sitede dener.

Her eski adres ya doğrudan 200 dönmeli ya da TEK bir yönlendirmeyle
(301/308) envanterdeki hedefe gidip orada 200 almalı.

Kullanım:
    # yerelde, Cloudflare Pages benzetimiyle:
    npm run build && npx wrangler pages dev dist --port 8788
    python3 migration/check_urls.py http://127.0.0.1:8788

    # yayından sonra:
    python3 migration/check_urls.py https://www.emdrizmir.com

Yalnızca standart kütüphane kullanır.
"""

import csv
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "emdrizmir-url-check/1.0"})
    try:
        with OPENER.open(req, timeout=20) as r:
            return r.status, r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "")


def main(base):
    base = base.rstrip("/")
    rows = list(csv.DictReader(open(ROOT / "inventory.csv", encoding="utf-8")))
    bad = []
    counts = {"200": 0, "1 yönlendirme": 0}
    for r in rows:
        path, karar, hedef = r["eski_adres"], r["karar"], r["hedef"]
        if karar == "kural-kaldir":
            continue  # eski sitede hiç olmamış adres
        status, loc = fetch(base + path)
        if status == 200:
            if karar == "yeni-sayfa" and path == hedef:
                counts["200"] += 1
                continue
            bad.append(f"{path}: 200 döndü, beklenen → {hedef}")
            continue
        if status not in (301, 308):
            bad.append(f"{path}: {status}")
            continue
        target = urljoin(base + path, loc)
        u = urlsplit(target)
        got = u.path + (f"#{u.fragment}" if u.fragment else "")
        if got != hedef:
            bad.append(f"{path}: {status} → {got}, beklenen {hedef}")
            continue
        s2, _ = fetch(f"{u.scheme}://{u.netloc}{u.path}")
        if s2 != 200:
            bad.append(f"{path}: {status} → {got} → {s2} (tek adımda 200 değil)")
            continue
        counts["1 yönlendirme"] += 1

    total = sum(counts.values())
    print(f"{base}: {total} adres doğru ({counts['200']} doğrudan 200, {counts['1 yönlendirme']} tek yönlendirmeyle)")
    if bad:
        print(f"{len(bad)} sorun:")
        for b in bad:
            print("  " + b)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8788")
