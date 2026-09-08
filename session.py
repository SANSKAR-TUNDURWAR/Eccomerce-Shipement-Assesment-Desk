# session.py
from collections import defaultdict
from typing import Any, Dict, List, Optional
from chains import classify_chain, escalate_chain, draft_email_chain
from pipeline import process_shipment_report
# Threshold for automatic manager escalation on damage claims
ESCALATION_PRICE_THRESHOLD = 100.0

class TriageSession:
    def __init__(self):
        self.processed_records: List[Dict[str, Any]] = []
        self.category_payouts: Dict[str, float] = defaultdict(float)
        self.total_compensation_paid: float = 0.0
        self.escalation_count: int = 0

    def process_report(self, shipment_data: dict) -> Dict[str, Any]:
        _, data = process_shipment_report(shipment_data)
        self.processed_records.append(data)
        self.total_compensation_paid += data["compensation_paid"]
        self.category_payouts[data["category"]] += data["compensation_paid"]
        if data["is_escalated"]:
            self.escalation_count += 1
        return data
    def get_daily_triage_summary(self) -> Dict[str, Any]:
        """Calculates aggregate metrics across the session."""
        total_reports = len(self.processed_records)
        if total_reports == 0:
            return {
                "total_reports_processed": 0,
                "total_compensation_paid": 0.0,
                "escalation_rate": "0.0%",
                "costliest_category": "None ($0.00)",
                "payout_breakdown_by_category": {},
            }

        escalation_rate = (self.escalation_count / total_reports) * 100

        # Determine costliest category by total aggregated payout
        costliest_cat, max_payout = "None", 0.0
        for cat, total_payout in self.category_payouts.items():
            if total_payout > max_payout:
                max_payout = total_payout
                costliest_cat = cat

        return {
            "total_reports_processed": total_reports,
            "total_compensation_paid": round(self.total_compensation_paid, 2),
            "escalation_rate": f"{escalation_rate:.1f}%",
            "costliest_category": f"{costliest_cat} (${max_payout:.2f})",
            "payout_breakdown_by_category": dict(self.category_payouts),
        }

    def print_daily_summary(self):
        summary = self.get_daily_triage_summary()
        print("\n" + "=" * 50)
        print("         DAILY TRIAGE AGGREGATED SUMMARY         ")
        print("=" * 50)
        print(f"Total Reports Processed : {summary['total_reports_processed']}")
        print(f"Total Compensation Paid : ${summary['total_compensation_paid']:.2f}")
        print(f"Escalation Rate         : {summary['escalation_rate']}")
        print(f"Costliest Category      : {summary['costliest_category']}")
        print("\nPayout by Category:")
        for cat, val in summary["payout_breakdown_by_category"].items():
            print(f"  - {cat:<10}: ${val:.2f}")
        print("=" * 50 + "\n")