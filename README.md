# BOTtas
![Bot avatar](bot1.png)



BOTtas on Telegram-huumoribotti, joka spämmiä Bottas-aiheisia stickereitä
trigger-sanoista

## Ominaisuudet
- Reagoi määriteltyihin trigger-sanoihin
- Lähettää Bottas-stickereitä (file_id)
- Helppo laajentaa komennoilla
- Ajettavissa Raspberry Pi:llä

  ![Bot response](bot2.png)


---

## Vaatimukset
- Python 3.9+
- Telegram Bot Token (BotFather)
- Telegram-ryhmä, johon botti lisätään
- (Suositus) Raspberry Pi tai Linux-palvelin

## Kuinka ajaa?
- Repo kloonattu raspille
- samaan directoryyn tehty .evn tiedosto sisältää vain
```
export TELEGRAM_BOT_TOKEN="..."   # jos ei ole .env:ssä
```
- HUOM. saman komennon voi myös ajaa suoraan directoryssä jos ei halua kirjoittaa .env tiedostoa!
- ennen käynnistystä sourcetaan .env
```
source .env #ohita tämä jos et ole tehnyt .enviä vaan olet exportannut tokenin käsin
```
- lopulta käynnistetään botti komennolla

```
python3 bottas.py
```
- itse pyöritän bottia tmux sessiossa raspilla, bottia voi edellä mainituilla ohjeilla ajaa myös suoraan terminaalista esim. läppärillä
- tarvitset oman BOT_TOKENIN, tämän saa Telegramin Bot Fatherilta


## tmux
- katsotaan missä botti pyörii
```
tmux ls
```
- avataan sessio
```
tmux attach -t <session_nimi>
```
- pysäytä botti ctrl + c
- sessio detachataan ctrl + b, d
