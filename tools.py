import os


def calculate_delayed_compensation(shipment_date, delivery_date, compensation_rate):
    """
    Calculate the delayed compensation based on shipment and delivery dates.

    Args:
        shipment_date (datetime): The date when the shipment was sent.
        delivery_date (datetime): The date when the shipment was delivered.
        compensation_rate (float): The rate of compensation per day of delay.

    Returns:
        float: The total compensation amount for the delay.    
    
    """
    delay_days = (delivery_date - shipment_date).days
    if delay_days > 0:
        return delay_days * compensation_rate
    else:
        return 0.0

def damaged_compensation(damage_severity, base_compensation):
    """
    Calculate the compensation for damaged shipments based on severity.

    Args:
        damage_severity (str): The severity of the damage ('minor', 'moderate', 'severe').
        base_compensation (float): The base compensation amount.
    
    Returns:
        float: The total compensation amount for the damage.        

    """
    severity_multiplier = {
        'minor': 0.5,
        'moderate': 1.0,
        'severe': 2.0
    }
    return base_compensation * severity_multiplier.get(damage_severity, 0)

def lost_compensation(item_value, insurance_coverage):
    """
    Calculate the compensation for lost shipments based on item value and insurance coverage.

    Args:
        item_value (float): The value of the lost item.
        insurance_coverage (float): The percentage of the item value covered by insurance.
    
    Returns:
        float: The total compensation amount for the lost item.
    """
    return item_value * (insurance_coverage / 100.0)

