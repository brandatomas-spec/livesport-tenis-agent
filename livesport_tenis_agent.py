from __future__ import annotations
import re
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE = "https://www.livesport.cz"
TODAY_URL = f"{BASE}/tenis/"
LAST_MATCHES = 5

def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()

def normalize_surface(text):
    t = clean(text).lower()
    if "antuka" in t: return "antuka"
    if "tráva" in t or "travnat" in t: return "tráva"
    if "tvrdý" in t or "hard" in t: return "tvrdý povrch"
    return None

def split_players(text):
    text = clean(text)
    for sep in [" – ", " - "]:
        if sep in text:
            p = [clean(x) for x in text.split(sep)]
            if len(p) == 2 and all(p): return p[0], p[1]
    return None

def match_links(page):
    out, seen = [], set()
    links = page.locator('a[href*="/zapas/"]')
    for i in range(links.count()):
        a = links.nth(i)
        try:
            href, txt = a.get_attribute("href"), clean(a.inner_text())
        except Exception:
            continue
        if not href or not txt or (" - " not in txt and " – " not in txt):
            continue
        key = (txt, href)
        if key not in seen:
            seen.add(key); out.append((txt, urljoin(BASE, href)))
    return out

def extract_matches(page):
    found = []
    for txt, href in match_links(page):
        players = split_players(txt)
        if not players: continue
        surface = None
        try:
            a = page.locator(f'a[href="{href}"]').first
            surface = normalize_surface(a.locator("xpath=..").inner_text())
        except Exception: pass
        if not surface:
            try:
                body = clean(page.locator("body").inner_text())
                pos = body.find(txt)
                if pos >= 0:
                    surface = normalize_surface(body[max(0,pos-900):pos+900])
            except Exception: pass
        if surface:
            found.append((players[0], players[1], href, surface))
    return list(dict(((x[0],x[1],x[2]), x) for x in found).values())

def profile_url(page, name):
    target = clean(name).lower()
    links = page.locator('a[href*="/hrac/"]')
    fallback = None
    for i in range(links.count()):
        a = links.nth(i)
        try: txt, href = clean(a.inner_text()), a.get_attribute("href")
        except Exception: continue
        if not href: continue
        if txt.lower() == target: return urljoin(BASE, href)
        if target in txt.lower() or txt.lower() in target:
            fallback = urljoin(BASE, href)
    return fallback

def last_five(player_page):
    # Prototype heuristic: extracts surface labels and dated completed-result rows.
    lines = [clean(x) for x in player_page.locator("body").inner_text().splitlines()]
    rows, current_surface = [], None
    for line in lines:
        if not line: continue
        s = normalize_surface(line)
        if s:
            current_surface = s
            continue
        if re.search(r"\b\d{1,2}\.\d{1,2}\.", line):
            low = line.lower()
            if any(x in low for x in ["skreč", "bez boje", "walkover"]):
                continue
            if current_surface:
                rows.append(current_surface)
                if len(rows) == LAST_MATCHES: break
    return rows

def run_scan():
    diagnostics = {}
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(locale="cs-CZ", viewport={"width": 1440, "height": 1000})
        page = context.new_page()
        page.goto(TODAY_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3500)
        for label in ["Souhlasím", "Přijmout", "Přijmout vše", "Accept all"]:
            try:
                page.get_by_text(label, exact=True).first.click(timeout=800)
                break
            except Exception: pass
        for _ in range(8):
            page.mouse.wheel(0, 1800); page.wait_for_timeout(350)
        matches = extract_matches(page)
        diagnostics["today_matches_found"] = len(matches)

        pp = context.new_page()
        cache = {}
        for p1, p2, url, surface in matches:
            counts = {}
            for player in (p1, p2):
                if player not in cache:
                    u = profile_url(page, player)
                    if not u:
                        cache[player] = []
                    else:
                        try:
                            pp.goto(u, wait_until="domcontentloaded", timeout=60000)
                            pp.wait_for_timeout(800)
                            cache[player] = last_five(pp)
                        except Exception:
                            cache[player] = []
                counts[player] = sum(1 for x in cache[player] if x == surface)
            if counts[p1] != counts[p2]:
                results.append({
                    "player1": p1, "player2": p2, "surface": surface,
                    "p1_surface_matches": counts[p1],
                    "p2_surface_matches": counts[p2],
                    "match_url": url,
                })
        browser.close()
    return results, diagnostics
