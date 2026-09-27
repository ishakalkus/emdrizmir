#!/usr/bin/env python3
"""live/ altındaki canlı sayfaların tam boy ekran görüntüsünü alır.

Yüklü Google Chrome'u kullanır (ayrı tarayıcı indirmez):
    .venv-archive/bin/pip install playwright
    .venv-archive/bin/python migration/screenshots.py
Çıktı: migration/screenshots/<yol>.jpg (masaüstü, 1280 px genişlik).
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "screenshots"
BASE = "https://www.emdrizmir.com"


def main():
    paths = sorted(
        json.loads(f.read_text(encoding="utf-8"))["url"].removeprefix(BASE)
        for f in (ROOT / "live").rglob("*.json")
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, locale="tr-TR")
        page = ctx.new_page()
        for path in paths:
            name = path.lstrip("/") or "index"
            if name.endswith("/"):
                name += "index"
            dest = OUT / (name + ".jpg")
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                page.goto(BASE + path, wait_until="networkidle", timeout=45000)
            except Exception as e:  # yavaş üçüncü taraf betikleri
                print(f"  ! {path}: {e.__class__.__name__}", file=sys.stderr)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(dest), full_page=True, type="jpeg", quality=60)
            print(f"{dest.relative_to(ROOT)}", file=sys.stderr)
        browser.close()


if __name__ == "__main__":
    main()
