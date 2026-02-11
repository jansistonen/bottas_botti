import os
import time
import random
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
API = f"https://api.telegram.org/bot{TOKEN}"

# Trigger-sanat
TRIGGERS = {"bottas", "valtteri", "viikset", "sauna", "kahvi", "perkele", "spämmi"}
TRIGGERS_OTHERS = {"jatkot"}

# stickerien file_id:t
BOTTAS_STICKERS = [
    "CAACAgQAAxkBAAMRaV94KGXhTsLpR5VpmH3AuVSlAlcAApkhAAJ2Z_lSv4pmvbRfGT04BA",
    "CAACAgQAAxkBAAMSaV94KwXnbLARh15tucMoh9m04dUAAg4aAAJAzgFTMSaSVjthd2U4BA",
    "CAACAgQAAxkBAAMPaV9y-GG-q00xUaUTx5g5zD-3HF8AAqkaAALQTQFTbraAyNft_o04BA",
    "CAACAgQAAxkBAAMKaV6Inxtp2J88GOjQEP3nW6ksUD0AAjUcAAKtEuBQCwlFWjtX6kk4BA",
    # "PASTE_STICKER_FILE_ID_2",
]

#slotti stickerien id:t
SLOT_STICKERS = [
    "CAACAgQAAxkBAAMEaYxm7mc4yvqVVnBihfWFtTQLHUgAAjAaAAJQF2lQzbnDo2lrD-k6BA", #takis
    "CAACAgQAAxkBAAMFaYxnLAHrPoPfN11zh2Yu2NqiC1UAAhYfAAKhz2FQW2wqdyIfcSs6BA", #mikko
    "CAACAgQAAxkBAAMGaYxnPnuUSHQgdWsP4PD73AQGfaQAAjcgAAKW92hQG2jkg35ETac6BA", #las palmasi
    "CAACAgQAAxkBAAMHaYxnxUTxbHYJlml2hB9GMLZ9hXUAAiwjAAIk5GBQtjhtK3aB0U86BA", #poppi
    "CAACAgQAAxkBAAMIaYxn4M3zNqZMDLZ2Rl85v2GnlfUAAkgaAALLz2FQ6a3ZyqwH_rs6BA", #jetti
    #lisää id
]

# Pieni “anti-späm” rate limit (sekunteina)
MIN_SECONDS_BETWEEN_STICKERS = 2.0
last_sent_at = 0.0

def api(method: str, payload: dict):
    r = requests.post(f"{API}/{method}", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

def should_trigger(text: str) -> bool:
    t = (text or "").lower()
    # trigger jos mikä tahansa trigger-sana esiintyy tekstissä
    return any(word in t for word in TRIGGERS)

def should_also_trigger(text: str) -> bool:
    t = (text or "").lower()
    # trigger jos mikä tahansa trigger-sana esiintyy tekstissä
    return any(word in t for word in TRIGGERS_OTHERS)

def main():
    global last_sent_at
    offset = None

    print("BOTtas käynnissä. Luetaan päivityksiä…")
    while True:
        try:
            updates = api("getUpdates", {"timeout": 25, "offset": offset})
            for upd in updates.get("result", []):
                offset = upd["update_id"] + 1

                msg = upd.get("message") or upd.get("edited_message")
                if not msg:
                    continue

                chat_id = msg["chat"]["id"]

                # jos joku lähetti stickerin chattiin, tulostetaan sen file_id -> helpottaa keräämistä
                if "sticker" in msg:
                    st = msg["sticker"]
                    print("Nähty sticker! file_id =", st.get("file_id"))
                    

                text = msg.get("text") or msg.get("caption")
                if not text:
                    continue

                if should_trigger(text):
                    now = time.time()
                    if now - last_sent_at < MIN_SECONDS_BETWEEN_STICKERS:
                        continue  # rate limit

                    sticker_id = random.choice(BOTTAS_STICKERS)
                    api("sendSticker", {
                        "chat_id": chat_id,
                        "sticker": sticker_id,
                    })
                    last_sent_at = now
                    print("Trigger -> lähetetty sticker chat:", chat_id)

                elif should_also_trigger(text):
                    now = time.time()
                    if now - last_sent_at < MIN_SECONDS_BETWEEN_STICKERS:
                        continue  # rate limit

                    sticker_id = random.choice(SLOT_STICKERS)
                    api("sendSticker", {
                        "chat_id": chat_id,
                        "sticker": sticker_id,
                    })
                    last_sent_at = now
                    print("Trigger -> lähetetty sticker chat:", chat_id)

        except requests.HTTPError as e:
            print("HTTP error:", e)
            time.sleep(2)
        except Exception as e:
            print("Error:", e)
            time.sleep(2)

if __name__ == "__main__":
    main()
