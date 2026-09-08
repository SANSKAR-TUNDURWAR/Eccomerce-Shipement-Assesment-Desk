# triage_check.py
import sys
from datetime import date
from session import TriageSession

# 4 Test Scenarios with datetime.date format
TEST_CASES = [
    {
        "id": "CASE-1: Mild Delay",
        "data": {
            "tracking_id": "TRK-DELAY-01",
            "customer_name": "Alice Smith",
            "customer_email": "alice@example.com",
            "report_text": "My shipment was supposed to arrive yesterday, but tracking says it is delayed by 1 day.",
            "Shipment_Price": 50.0,
            "Shipment_Date": date(2024, 6, 1),
            "Delivery_Date": date(2024, 6, 6),
        },
        "expected_category": "delayed",
        "expected_escalation": False,
    },
    {
        "id": "CASE-2: High-Value Loss",
        "data": {
            "tracking_id": "TRK-LOST-02",
            "customer_name": "Bob Vance",
            "customer_email": "bob@example.com",
            "report_text": "The courier marked this delivered last week, but the package never showed up. It is missing.",
            "Shipment_Price": 850.0,
            "Shipment_Date": date(2024, 5, 20),
            "Delivery_Date": date(2024, 5, 25),
        },
        "expected_category": "lost",
        "expected_escalation": False,
    },
    {
        "id": "CASE-3: Minor Damage Claim",
        "data": {
            "tracking_id": "TRK-DMG-03",
            "customer_name": "Carol Danvers",
            "customer_email": "carol@example.com",
            "report_text": "The package arrived damaged and the mug inside is broken.",
            "Shipment_Price": 35.0,
            "Shipment_Date": date(2024, 6, 2),
            "Delivery_Date": date(2024, 6, 5),
        },
        "expected_category": "damaged",
        "expected_escalation": False,
    },
    {
        "id": "CASE-4: Garbled / Unclassifiable",
        "data": {
            "tracking_id": "TRK-UNKN-04",
            "customer_name": "David Miller",
            "customer_email": "david@example.com",
            "report_text": "### ERR_NULL_BUFFER: 0x992384a sdkjfh 999 ??? help qwe#$! ---",
            "Shipment_Price": 0.0,
            "Shipment_Date": date(2024, 6, 3),
            "Delivery_Date": date(2024, 6, 5),
        },
        "expected_category": "unknown",
        "expected_escalation": True,
    },
]


def run_triage_checks():
    session = TriageSession()
    all_passed = True

    print("Running triage_check.py against session pipeline...\n")

    for test in TEST_CASES:
        print(f"--> Testing [{test['id']}]")
        result = session.process_report(test["data"])

        category_match = result["category"] == test["expected_category"]
        escalation_match = result["is_escalated"] == test["expected_escalation"]

        if category_match and escalation_match:
            print(
                f"    [PASS] Category='{result['category']}' | "
                f"Escalated={result['is_escalated']} | "
                f"Payout=${result['compensation_paid']:.2f}"
            )
        else:
            all_passed = False
            print(
                f"    [FAIL] Expected Category='{test['expected_category']}', got '{result['category']}'"
            )
            print(
                f"           Expected Escalation={test['expected_escalation']}, got {result['is_escalated']}"
            )

    session.print_daily_summary()

    if all_passed:
        print("[SUCCESS] All 4 scenarios routed and triaged correctly.")
    else:
        print("[ERROR] One or more test scenarios failed.")
        sys.exit(1)


if __name__ == "__main__":
    run_triage_checks()