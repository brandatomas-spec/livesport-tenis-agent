# Livesport tenisový filtr – mobilní webová aplikace

Toto je mobilní webová verze prototypu.

## Pravidlo
- dnešní tenisové zápasy
- u každého zápasu aktuální povrch
- posledních 5 odehraných zápasů obou hráčů
- počet z těchto 5 zápasů na aktuálním povrchu
- zobrazit pouze zápasy, kde se počty liší

## Spuštění
```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
python app.py
```

Potom otevři v telefonu adresu serveru, např. `http://IP_POČÍTAČE:8080`.

## Nasazení
Aby aplikace fungovala z telefonu bez zapnutého PC, je potřeba tento projekt nasadit na server/VPS nebo jiný cloud, který umí spustit Python a Chromium/Playwright.

Poznámka: scraper je stále prototyp a může vyžadovat úpravu, pokud Livesport změní strukturu stránky.
