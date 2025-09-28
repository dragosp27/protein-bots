import time
from sites.ryse.crawler import RyseCrawler
from sites.ghost.crawler import GhostCrawler
from notifications.discord_notifier import DiscordNotifier
from configparser import ConfigParser

def load_config():
    cfg = ConfigParser()
    cfg.read("config/config.ini")
    return cfg

def main_loop():
    cfg = load_config()
    webhook = cfg.get("notifications", "discord_webhook_url")
    notifier = DiscordNotifier(webhook)

    crawlers = {
        "ryse": RyseCrawler(),
        "ghost": GhostCrawler(),
    }
    last_states = {key: None for key in crawlers.keys()}

    print("[INFO] Starting crawler loop...")

    while True:
        for key, crawler in crawlers.items():
            print(f"[INFO] Crawling {key}...")
            try:
                if key == "ghost":
                    statuses = crawler.fetch_all()
                    print(f"[DEBUG] Found {len(statuses)} Ghost products.")
                    for status in statuses:
                        print(f"[DEBUG] Processing {status.name} ({status.url})")
                        prev = last_states.get(status.url)
                        if prev is None or status != prev:
                            msg = f"[GHOST] {status.name}\nURL: {status.url}\n"
                            for v in status.variants:
                                msg += f"  - {v.flavor}: {'IN STOCK' if v.in_stock else 'OUT'}\n"
                            print(f"[DEBUG] Sending notification:\n{msg}")
                            notifier.notify(msg)
                            last_states[status.url] = status
                else:
                    status = crawler.fetch_status()
                    print(f"[DEBUG] Ryse product: {status.product_name}")
                    prev = last_states.get(key)
                    if prev is None or status != prev:
                        msg = f"[{key.upper()}] {status.product_name}\n"
                        for v in status.variants:
                            msg += f"  - {v.flavor}: {'IN STOCK' if v.in_stock else 'OUT'}\n"
                        print(f"[DEBUG] Sending notification:\n{msg}")
                        notifier.notify(msg)
                        last_states[key] = status
            except Exception as e:
                print(f"[ERROR] Error crawling {key}: {e}")

        print("[INFO] Sleeping for 5 minutes...")
        time.sleep(60 * 5)

if __name__ == "__main__":
    main_loop()
