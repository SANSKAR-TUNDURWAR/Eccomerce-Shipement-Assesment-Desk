from chains import classify_chain, escalate_chain, draft_email_chain
from tools import calculate_delayed_compensation,damaged_compensation,lost_compensation

def process_shipment_report(shipment_data: dict) -> dict:
    """
    Processes a shipment issue through classification, routing, and resolution.
    
    Expected input schema:
    {
        "tracking_id": "TRK-987654",
        "customer_name": "Jane Doe",
        "customer_email": "jane@example.com",
        "report_text": "The box arrived crushed and the items inside were broken."
        "Shipment_Price": 100.0,
        "Shipment_Date": "2024-06-01",
        "Delivery_Date": "2024-06-05",
    }
    """
    # Step 1: Classify the issue
    # classify_chain evaluates the user report and returns a category
    classification_result = classify_chain.invoke({
        "report_text": shipment_data["report_text"]
    })
    
    # Normalize category string (handles string outputs or dict responses)
    category = None
    if isinstance(classification_result, dict):
        category = classification_result.get("category", "unknown").lower().strip()
    else:
        category = str(classification_result).lower().strip()

    print(f"[*] Shipment {shipment_data['tracking_id']} classified as: '{category}'")

    # Step 2: Context dictionary passed downstream
    context = {
        **shipment_data,
        "category": category,
    }

    # Step 3: Route based on issue severity
    # Severe issues (damaged / lost / unknown) require managerial escalation
    # Standard issues (delayed) receive a customer resolution email
    results = {
        "tracking_id": shipment_data["tracking_id"],
        "category": category,
        "customer_email": None,
        "internal_escalation_note": None,
        "action_taken": None
    }
    compensation_amount = 0.0
    is_escalated = False
    escalation_note = None
    if category in ["damaged", "lost", "delayed"]:
        if category == "delayed":
            # Calculate delayed compensation
            shipment_date = shipment_data.get("Shipment_Date")
            delivery_date = shipment_data.get("Delivery_Date")
            compensation_rate = 10.0  # Example rate per day of delay
            compensation_amount = calculate_delayed_compensation(shipment_date, delivery_date, compensation_rate)
        elif category == "damaged":
            # Calculate damaged compensation
            damage_severity = "moderate"  # Example severity; in practice, this would be derived from the report
            base_compensation = shipment_data.get("Shipment_Price", 0.0)
            compensation_amount = damaged_compensation(damage_severity, base_compensation)

        elif category == "lost":
            # Calculate lost compensation
            item_value = shipment_data.get("Shipment_Price", 0.0)
            insurance_coverage = 80.0  # Example insurance coverage percentage
            compensation_amount = lost_compensation(item_value, insurance_coverage)
        
        context["compensation_amount"] = compensation_amount
        customer_email = draft_email_chain.invoke(context)
                
        results["customer_email"] = customer_email
        results["action_taken"] = "Drafted standard delay update email"

    elif category == "unknown":
        is_escalated = True
        context["compensation_amount"] = compensation_amount
        context["is_escalated"] = is_escalated
        escalation_note = escalate_chain.invoke(context)
        customer_email = draft_email_chain.invoke(context)
        results["internal_escalation_note"] = escalation_note
        results["customer_email"] = customer_email
        results["action_taken"] = "Escalated to management & drafted customer notification"

    record = {
        "tracking_id": shipment_data.get("tracking_id"),
        "customer_name": shipment_data.get("customer_name"),
        "customer_email": shipment_data.get("customer_email"),
        "Shipment_Price": shipment_data.get("Shipment_Price"),
        "Shipment_Date": shipment_data.get("Shipment_Date"),
        "Delivery_Date": shipment_data.get("Delivery_Date"),
        "category": str(category),
        "compensation_paid": compensation_amount,
        "is_escalated": is_escalated,
        "escalation_note": escalation_note,
        "customer_email": results["customer_email"],
    }
    return results,record