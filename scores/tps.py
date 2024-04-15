from data.models import Property


def calculate_type_of_property_subscore(properties):
    """
    Calculate the Type Of Property SubScore (TPS) based on the distribution of different
    property types (SFR, CON, TW, OTR) in a given list of properties.

    :param properties: A list of Property objects with property type attributes.
    :return: The TPS score as a float.
    """
    if not properties:
        return 0

    # Initialize counters for each property type
    property_type_counts = {"SFR": 0, "CON": 0, "TW": 0, "OTR": 0}

    for prop in properties:
        if prop.property_type in property_type_counts:
            property_type_counts[prop.property_type] += 1
        else:
            property_type_counts["OTR"] += 1  # Assume any unspecified types as Other Residential

    total_properties = len(properties)
    if total_properties == 0:
        return 0

    # Calculate the percentage distribution for each property type
    property_type_percentages = {ptype: count / total_properties for ptype, count in property_type_counts.items()}

    # For the TPS score, calculate the diversity or variance among the percentages
    # One simple approach is to use the standard deviation among the percentage values
    # Higher deviation indicates higher diversity, contributing to a higher score
    avg_percentage = sum(property_type_percentages.values()) / len(property_type_percentages)
    variance = sum((percentage - avg_percentage) ** 2 for percentage in property_type_percentages.values()) / len(
        property_type_percentages)
    std_deviation = variance ** 0.5

    # Normalize and scale the standard deviation to a 0-10 score
    # This example uses a hypothetical range for standard deviation; adjust based on actual data
    max_std_dev = 0.25  # Hypothetical maximum standard deviation for full diversity
    tps_score = (std_deviation / max_std_dev) * 10
    tps_score = min(max(tps_score, 0), 10)  # Ensure score is within 0-10

    return tps_score


def test():
    # Example list of Property objects with various types
    properties = [
        Property(property_id=1, property_type="SFR"),
        Property(property_id=2, property_type="CON"),
        Property(property_id=3, property_type="TW"),
        Property(property_id=4, property_type="OTR"),
        # Add more properties as needed
    ]

    # Calculate the Type Of Property SubScore
    tps_score = calculate_type_of_property_subscore(properties)
    print(f"Type Of Property SubScore (TPS): {tps_score:.2f}")

# Property Type Required
