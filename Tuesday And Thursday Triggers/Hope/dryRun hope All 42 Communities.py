import time
import requests
from datetime import datetime

WEBHOOK_URL = "https://gs.budy.bot/external/services/consultant/webhook/v2/run/hwhrn/0be8bb51a9914c9ca3d5bd23ad15eaf5"
DELAY_SECONDS = 1 * 60  # 1 minute

# Community IDs to dispatch for
COMMUNITY_IDS = [
    # "4729",
    # "4736",
    # "4725","4770","4728","4753","4772","11364","16478","18953","4746","4715",
    # "4707",
    # "4758",
    # "11363",
    # "4713",
    # "4711",
    # "4750",
    # "4737",
    # "4717",
    # "4731",
    # "4724",
    # "4742",
    # "4701",
    # "4730",
    # "4745",
    # "4763",
    # "4755",
    # "4733",
    # "4697",
    # "4748",
    # "4734",
    # "4739",
    # "4751",
    # "4716",
    # "4714",
    # "4754",
    # "4744",
    # "4718",
    # "4703",
    # "4762",
    # "4757",
]

# Common config variables sent to the workflow
CONFIG_VARIABLES = {
    "netScoreThreshold": 0,
    "maxProspectsPerCounselor": 5,
    "lookaheadDays": 30,
    "cooldownDays": 60,
    "dispatchSleepMinutes": 0.1,
    "crmBaseUrl" : "https://crm.welcomehomesoftware.com/",
    "mailKind": "MAILGUN",
    "ccEmails": ["budy@budy.bot"],
}


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
    # Start time: Feb 24, 2026 at 5:00 AM Pacific (local Mac time)
    target = datetime(2026, 2, 24, 5, 0, 0)

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
            "communityId": community_id,
            "dryRun": True,
            "pickBasedOnTaggingTrue": True,
            "mode":"triggerChildOnly",
            "configVariables": CONFIG_VARIABLES,
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
