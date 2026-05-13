import time
import requests
from datetime import datetime


WEBHOOK_URL = "https://gs.budy.bot/external/services/consultant/webhook/v2/run/hwhrn/25fdcb6f5d624bc28b5c904f86e5c008"
DELAY_SECONDS = 15 * 60  # 15 minutes

# Community IDs to dispatch for
COMMUNITY_IDS = [
    "16478",
    # "11364",
    # "18953",
    # "4736",
    # "4725",
    # "4770",
    # "4746",
    # "4728",
    # "4753",
    # "4772",
    # "4729",
    # "4715"
]

# Common config variables sent to the workflow
# CONFIG_VARIABLES = {
#     "maxProspects": 4,
#     "digitalTouchNetScoreLt": 0,
#     "includeScoreBreakdown": True,
# }


def trigger_webhook(payload: dict, community_id: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    print(f"\n[{datetime.now().isoformat(timespec='seconds')}] Triggering community {community_id}...")
    resp = requests.post(WEBHOOK_URL, headers=headers, json=payload, timeout=60)

    print(f"Status: {resp.status_code}")

    # Print a short response preview (helpful for debugging)
    text = (resp.text or "").strip()
    if text:
        print("Response (first 500 chars):")
        print(text[:500])

    # Raise on non-2xx responses
    resp.raise_for_status()


def main() -> None:
    # Start time: May 5, 2026 at 7:00 AM Pacific (local Mac time)
    target = datetime(2026, 5, 5, 7, 0, 0)

    now = datetime.now()
    if now < target:
        sleep_seconds = (target - now).total_seconds()
        mins = int(sleep_seconds // 60)
        print(
            f"[{now.isoformat(timespec='seconds')}] Sleeping until {target.isoformat(timespec='seconds')} "
            f"({mins} minutes)..."
        )
        time.sleep(sleep_seconds)

    print(f"[{datetime.now().isoformat(timespec='seconds')}] Starting dispatcher triggers...")

    for idx, community_id in enumerate(COMMUNITY_IDS, start=1):
        payload = {
            "communityIds": [community_id],
            "limit":9999,
            "dryRun": False,
            # "configVariables": CONFIG_VARIABLES,
        }

        try:
            trigger_webhook(payload, community_id)
        except requests.RequestException as e:
            print(f"ERROR triggering community {community_id}: {e}")

        if idx < len(COMMUNITY_IDS):
            print(f"Waiting {DELAY_SECONDS // 60} minutes before next trigger...")
            time.sleep(DELAY_SECONDS)

    print("\nAll dispatcher triggers completed.")


if __name__ == "__main__":
    main()
