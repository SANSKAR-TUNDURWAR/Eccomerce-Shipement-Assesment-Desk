import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from session import TriageSession

TRIAGE_LOG: List[Dict[str, Any]] = []

def handle_submission(report_text: str, shipment_value: float, shipment_date: str, delivery_date: str, customer_name: str, customer_email: str, tracking_id: str):
    if not report_text.strip():
        raise gr.Error("Please provide an incident description.")

    # Construct shipment data dictionary
    shipment_data = {
        "tracking_id": tracking_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "report_text": report_text,
        "Shipment_Price": shipment_value,
        "Shipment_Date": shipment_date,
        "Delivery_Date": delivery_date,
    }

    # Process the shipment report through the triage session
    session = TriageSession()
    result = session.process_report(shipment_data)

    # Add the result to the triage log
    TRIAGE_LOG.append(result)

    outcome_md = f"""
    ### 📋 Category: {result['category']}
    - **Compensation:** `{result['compensation_paid']:.2f}`
    - **Is Escalated:** **{result['is_escalated']}**
    - **Escalation Note:** {result['escalation_note']}`
    """
    df = pd.DataFrame([result])
    return outcome_md, df

def handle_daily_summary():
    if not TRIAGE_LOG:
        return "### 📊 Daily Summary\n\n*No tickets processed today yet.*"

    df = pd.DataFrame(TRIAGE_LOG)
    total_tickets = len(df)
    #total_val = df["shipment_value"].sum()
    escalated_count = len(df[df["is_escalated"] == True])
    
    summary_md = f"""
    # 📊 Daily Triage Summary Report
    *Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

    ---
    ### 📈 High-Level Metrics
    - **Total Claims/Reports Processed:** `{total_tickets}`
    - **Escalated for Manual Review:** `{escalated_count}`
    ---
    """
    return summary_md
