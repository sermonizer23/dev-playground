import time
import json
import requests
from datetime import datetime

WEBHOOK_URL = "https://gs.budy.bot/external/services/consultant/webhook/v2/run/beztak/1cb284fa3f7a411dbc89cea9eb583810"
DELAY_SECONDS = 10 * 60  # 10 minutes

BODIES = [
    # Body 1

    {
    "inputSheetName": "38725ENV",
    "filters": {
        "fields": {
            "stage": {
                "operator": "in",
                "values": [
                    "Post-Tour"
                ]
            },
            "communityId": {
                "operator": "in",
                "values": [
                    "38725"
                ]
            },
            "qualifyForReengageTuesdays": {
                "operator": "equals",
                "value": True
            },
            "prospectStatus": {
                "operator": "equals",
                "value": "open"
            },
            "nextEligTues": {
                "operator": "is_null"
            },
            "salesCounselorId":{
                "operator":"equals",
                "value":"Heather Savelle"
            },
            "nextEligTues": {
                "operator": "equals",
                "value":"1"
            }
        }
    }
},
    # Body 2
    {
    "inputSheetName": "38725ENV",
    "filters": {
        "fields": {
            "stage": {
                "operator": "in",
                "values": [
                    "Post-Tour"
                ]
            },
            "communityId": {
                "operator": "in",
                "values": [
                    "38725"
                ]
            },
            "qualifyForReengageTuesdays": {
                "operator": "equals",
                "value": True
            },
            "prospectStatus": {
                "operator": "equals",
                "value": "open"
            },
            "nextEligTues": {
                "operator": "is_null"
            },
            "salesCounselorId":{
                "operator":"equals",
                "value":"Kaseigh Layne"
            }
        }
    }
},
    # Body 3
    {
    "inputSheetName": "38726ENV",
    "filters": {
        "fields": {
            "stage": {
                "operator": "in",
                "values": [
                    "Post-Tour"
                ]
            },
            "communityId": {
                "operator": "in",
                "values": [
                    "38726"
                ]
            },
            "qualifyForReengageTuesdays": {
                "operator": "equals",
                "value": True
            },
            "prospectStatus": {
                "operator": "equals",
                "value": "open"
            },
            "nextEligTues": {
                "operator": "is_null"
            }
        }
    }
},
    # Body 4
{
    "inputSheetName": "38727ENV",
    "filters": {
        "fields": {
            "stage": {
                "operator": "in",
                "values": [
                    "Post-Tour"
                ]
            },
            "communityId": {
                "operator": "in",
                "values": [
                    "38727"
                ]
            },
            "qualifyForReengageTuesdays": {
                "operator": "equals",
                "value": True
            },
            "prospectStatus": {
                "operator": "equals",
                "value": "open"
            },
            "nextEligTues": {
                "operator": "equals",
                "value":"2"
            }
        }
    }
},
    # Body 5
    {
    "inputSheetName": "38728ENV",
    "filters": {
        "fields": {
            "stage": {
                "operator": "in",
                "values": [
                    "Post-Tour"
                ]
            },
            "communityId": {
                "operator": "in",
                "values": [
                    "38728"
                ]
            },
            "qualifyForReengageTuesdays": {
                "operator": "equals",
                "value": True
            },
            "prospectStatus": {
                "operator": "equals",
                "value": "open"
            },
            "nextEligTues": {
                "operator": "equals",
                "value":"1"
            }
        }
    }
},
    # Body 6
    {
    "inputSheetName": "38729ENV",
    "filters": {
        "fields": {
            "stage": {
                "operator": "in",
                "values": [
                    "Post-Tour"
                ]
            },
            "communityId": {
                "operator": "in",
                "values": [
                    "38729"
                ]
            },
            "qualifyForReengageTuesdays": {
                "operator": "equals",
                "value": True
            },
            "prospectStatus": {
                "operator": "equals",
                "value": "open"
            },
            "nextEligTues": {
                "operator": "equals",
                "value":"2"
            },
            "salesCounselorId": {
                "operator": "equals",
                "value": "Kathryn Andros"
            }
        }
    }
},
    # Body 7
    {
    "inputSheetName": "38730ENV",
    "filters": {
        "fields": {
            "stage": {
                "operator": "in",
                "values": [
                    "Post-Tour"
                ]
            },
            "communityId": {
                "operator": "in",
                "values": [
                    "38730"
                ]
            },
            "qualifyForReengageTuesdays": {
                "operator": "equals",
                "value": True
            },
            "prospectStatus": {
                "operator": "equals",
                "value": "open"
            },
            "nextEligTues": {
                "operator": "equals",
                "value":"2"
            }
        }
    }
},
    # Body 8
    {
    "inputSheetName": "38731ENV",
    "filters": {
        "fields": {
            "stage": {
                "operator": "in",
                "values": [
                    "Post-Tour"
                ]
            },
            "communityId": {
                "operator": "in",
                "values": [
                    "38731"
                ]
            },
            "qualifyForReengageTuesdays": {
                "operator": "equals",
                "value": True
            },
            "prospectStatus": {
                "operator": "equals",
                "value": "open"
            },
            "nextEligTues": {
                "operator": "equals",
                "value":"2"
            }
        }
    }
},
]

def trigger_webhook(payload: dict, index: int) -> None:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    print(f"\n[{datetime.now().isoformat(timespec='seconds')}] Triggering body {index}...")
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
    # Start time: Apr 21, 2026 at 5:00 AM Pacific (local Mac time)
    target = datetime(2026, 4, 21, 5, 0, 0)

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