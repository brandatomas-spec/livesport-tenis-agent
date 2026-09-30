# Livesport tenis agent – Render

Tato verze je připravená pro nasazení na Render jako Docker Web Service.

## Co dělá
- otevře dnešní tenis na Livesportu
- najde dnešní zápasy a povrch
- u každého hráče se pokusí zjistit posledních 5 zápasů
- spočítá zápasy na stejném povrchu
- zobrazí pouze zápasy, kde se počty liší

## Nasazení z telefonu
1. Vytvoř GitHub účet a nový repository.
2. Nahraj obsah tohoto projektu do repository.
3. Na Render vytvoř `New -> Web Service` a připoj GitHub repository.
4. Jako runtime zvol `Docker`.
5. Deploy.

Render použije Dockerfile a spustí Flask aplikaci na portu PORT.
