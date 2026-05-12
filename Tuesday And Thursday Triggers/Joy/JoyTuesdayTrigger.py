import time
import json
import requests
from datetime import datetime

WEBHOOK_URL = "https://gs.budy.bot/external/services/consultant/webhook/v2/run/beztak/1cb284fa3f7a411dbc89cea9eb583810"
DELAY_SECONDS = 20 * 60  # 20 minutes

COMMUNITY_IDS = [
    38725,
    38726,
    38727,
    38728,
    38729,
    38730,
    38731,
]

BODIES = [
    {
        "inputSheetName": "environmentv3",
        "mockRun": False,
        "overrideCommunityIds": [community_id],
    }
    for community_id in COMMUNITY_IDS
]

def trigger_webhook(payload: dict, index: int) -> None:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    community_ids = payload.get("overrideCommunityIds", [])
    community_label = community_ids[0] if community_ids else "unknown"
    print(f"\n[{datetime.now().isoformat(timespec='seconds')}] Triggering community {community_label} (body {index})...")
    resp = requests.post(WEBHOOK_URL, headers=headers, json=payload, timeout=60)

    print(f"Status: {resp.status_code}")
    # Print a short response preview (helpful for debugging)
    text = (resp.text or "").strip()
    if text:
        print("Response (first 500 chars):")
        print(text[:500])

    # Raise on non-2xx responses
    resp.raise_for_status()

def main():
    # Start time: May 5, 2026 at 4:00 AM Pacific (local Mac time)
    target = datetime(2026, 5, 5, 4, 0, 0)

    now = datetime.now()
    if now < target:
        sleep_seconds = (target - now).total_seconds()
        mins = int(sleep_seconds // 60)
        print(f"[{now.isoformat(timespec='seconds')}] Sleeping until {target.isoformat(timespec='seconds')} "
              f"({mins} minutes)...")
        time.sleep(sleep_seconds)

    print(f"[{datetime.now().isoformat(timespec='seconds')}] Starting webhook triggers...")

    for i, payload in enumerate(BODIES, start=1):
        try:
            trigger_webhook(payload, i)
        except requests.RequestException as e:
            print(f"ERROR triggering body {i}: {e}")

        if i < len(BODIES):
            print(f"Waiting {DELAY_SECONDS // 60} minutes before next trigger...")
            time.sleep(DELAY_SECONDS)

    print("\nAll triggers completed.")

if __name__ == "__main__":
    main()