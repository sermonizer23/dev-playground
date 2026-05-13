import time
import requests
from datetime import datetime

WEBHOOK_URL = "https://gs.budy.bot/external/services/consultant/webhook/v2/run/hwhrn/e99193c28b9b44cc8dff86ec8037be57"
DELAY_SECONDS = 10 * 60  # 10 minutes
BATCH_SIZE = 3
WITHIN_BATCH_SPACING_SECONDS = 120  # 2 minutes between triggers in the same batch

# Community IDs to dispatch for
COMMUNITY_IDS = [
    "4707",
    "16478",
    "4757",
    "18953",
    "4729",
    "4750",
    "4733",
    "4756",  # The Savoy
    "16412", # Bear Hollow Estates
    "4766", # Stoneridge
    "4722", # Hessler Heights
    "4712", # CottonWood Estates
]

# Common config variables sent to the workflow
CONFIG_VARIABLES = {
    "netScoreThreshold": 0,
    "maxProspectsPerCounselor": 2,
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
    # Start time: May 13, 2026 at 5:30 AM Pacific (local Mac time)
    target = datetime(2026, 5, 13, 5, 30, 0)

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

    total = len(COMMUNITY_IDS)

    for batch_start in range(0, total, BATCH_SIZE):
        batch = COMMUNITY_IDS[batch_start:batch_start + BATCH_SIZE]
        batch_number = (batch_start // BATCH_SIZE) + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

        print(
            f"\nStarting batch {batch_number}/{total_batches}: {batch}"
        )

        for idx_in_batch, community_id in enumerate(batch, start=1):
            payload = {
                "communityId": community_id,
                "dryRun": False,
                "mode":"triggerChildOnly",
                "configVariables": CONFIG_VARIABLES,
            }

            try:
                trigger_webhook(payload, community_id)
            except requests.RequestException as e:
                print(f"ERROR triggering community {community_id}: {e}")

            if idx_in_batch < len(batch):
                print(
                    f"Waiting {WITHIN_BATCH_SPACING_SECONDS} seconds before next trigger in batch..."
                )
                time.sleep(WITHIN_BATCH_SPACING_SECONDS)

        if batch_start + BATCH_SIZE < total:
            print(
                f"Waiting {DELAY_SECONDS // 60} minutes before next batch..."
            )
            time.sleep(DELAY_SECONDS)

    print("\nAll dispatcher triggers completed.")


if __name__ == "__main__":
    main()
