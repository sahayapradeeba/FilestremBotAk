from os import environ as env
from os import getenv, environ
from dotenv import load_dotenv
import os

load_dotenv()

class Telegram:
    API_ID = int(env.get("API_ID", "10499388"))
    API_HASH = str(env.get("API_HASH", "f7b1a0278675700f9bb9747c64403acb"))
    BOT_TOKEN = str(env.get("BOT_TOKEN", "7375854453:AAHbjPUQhVOZ7IAF1tjyiciEtJdFDBYgbB8"))
    OWNER_ID = int(env.get('OWNER_ID', '1473415982'))
    WORKERS = int(env.get("WORKERS", "6"))  # 6 workers = 6 commands at once
    DATABASE_URL = str(env.get('DATABASE_URL','mongodb+srv://TheatrePrint77:TheatrePrint77@filesharexbot.bjbua6q.mongodb.net/?retryWrites=true&w=majority'))
    UPDATES_CHANNEL = str(env.get('UPDATES_CHANNEL', "Telegram"))
    SESSION_NAME = str(env.get('SESSION_NAME', 'filesharexbot'))
    FORCE_SUB_ID = env.get('FORCE_SUB_ID', "-1002145921498")
    FORCE_SUB = env.get('FORCE_UPDATES_CHANNEL', True)
    FORCE_SUB = True if str(FORCE_SUB).lower() == "true" else False
    SLEEP_THRESHOLD = int(env.get("SLEEP_THRESHOLD", "60"))
    FILE_PIC = env.get('FILE_PIC', "https://graph.org/file/5bb9935be0229adf98b73.jpg")
    START_PIC = env.get('START_PIC', "https://graph.org/file/290af25276fa34fa8f0aa.jpg")
    VERIFY_PIC = env.get('VERIFY_PIC', "https://graph.org/file/736e21cc0efa4d8c2a0e4.jpg")
    MULTI_CLIENT = True
    FLOG_CHANNEL = int(env.get("FLOG_CHANNEL", "-1007375854453"))   # Logs channel for file logs
    ULOG_CHANNEL = int(env.get("ULOG_CHANNEL", "-1007375854453"))   # Logs channel for user logs
    MODE = env.get("MODE", "primary")
    SECONDARY = True if MODE.lower() == "secondary" else False
    AUTH_USERS = list(set(int(x) for x in str(env.get("AUTH_USERS", "1473415982")).split()))
    SHORTLINK_URL = os.environ.get('SHORTLINK_URL', 'publicearn.com')
    SHORTLINK_API = os.environ.get('SHORTLINK_API', '5f14184b5d330486d0ebcb32127fdca5b03c8b42')

class Server:
    PORT = int(env.get("PORT", 8080))
    BIND_ADDRESS = str(env.get("BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(env.get("PING_INTERVAL", "1200"))
    HAS_SSL = str(env.get("HAS_SSL", "0").lower()) in ("1", "true", "t", "yes", "y")
    NO_PORT = str(env.get("NO_PORT", "0").lower()) in ("1", "true", "t", "yes", "y")
    if 'DYNO' in environ:
        ON_HEROKU = True
        APP_NAME = str(getenv('APP_NAME', "mrak-2a7526a285ee")) #dont need to fill anything here
        FQDN = str(env.get("FQDN", "https://mrak-utcj.onrender.com"))
    else:
        ON_HEROKU = False
    FQDN = str(env.get("FQDN", "https://mrak-streambot.onrender.com"))
    HAS_SSL=bool(getenv('HAS_SSL',True))
    if HAS_SSL:
        URL = "https://{}/".format(FQDN)
    else:
        URL = "http://{}/".format(FQDN)
    



