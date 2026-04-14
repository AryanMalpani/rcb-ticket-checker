import requests
import time
import json
import os
from datetime import datetime

URL = "https://rcbscaleapi.ticketgenie.in/ticket/eventlist/O"
SLACK_WEBHOOK_URL = (
    "<INSERT-YOUR-CHAT-WEBHOOK>"
)
STATE_FILE = os.path.join(os.path.dirname(__file__), "last_response.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://shop.royalchallengers.com",
    "Referer": "https://shop.royalchallengers.com/",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def load_last_response():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return None


def save_response(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


def notify_slack(data):
    payload = {"text": f"🏏 RCB Ticket Info Changed!\n```{json.dumps(data, indent=2)}```"}
    resp = requests.post(SLACK_WEBHOOK_URL, json=payload)
    log(f"Slack notified, status: {resp.status_code}")


def check():
    try:
        response = requests.get(URL, headers=HEADERS, verify=False, timeout=10)
        log(f"Status Code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        log(f"Response: {data}")
        return data
    except requests.exceptions.HTTPError as e:
        log(f"HTTP Error: {e} | Response: {e.response.text if e.response else 'N/A'}")
    except requests.exceptions.RequestException as e:
        log(f"Request failed: {e}")
    return None


if __name__ == "__main__":
    log("Starting infinite checker, every 5 seconds. Press Ctrl+C to stop.")
    while True:
        try:
            data = check()
            if data is not None:
                last = load_last_response()
                if data != last:
                    log("Response changed! Sending 3 Slack notifications...")
                    for i in range(3):
                        notify_slack(data)
                        log(f"Notification {i+1}/3 sent.")
                        if i < 2:
                            time.sleep(2)
                    save_response(data)
                    log("New response saved.")
                else:
                    log("No change detected.")
        except Exception as e:
            log(f"Unexpected error: {e}")
            requests.post(
                SLACK_WEBHOOK_URL,
                json={
                    "text": f"⚠️ RCB checker crashed and stopped!\nError: `{e}`"
                },
            )
            break
        time.sleep(5) # Change this to lower freq like 1 sec on the day rcb announces ticket sales for lower latency.
