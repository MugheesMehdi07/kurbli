from data.models import Property


def calculate_concentration_properties_subscore(properties):
    """
    Calculate the Concentration Properties SubScore (CPS) with adjustments for
    Quality of Investment (QoI) and scoring based on a specified table.

    :param properties: A list of Property objects.
    :return: The CPS score as a float.
    """
    if not properties:
        return 0

    # Step 1: Calculate CPZU based on properties with QoI >= 5.0
    total_properties = len(properties)
    investor_owned_properties = [p for p in properties if p.is_investor_owned and p.quality_of_investment >= 5.0]
    cpz = len(investor_owned_properties) / total_properties if total_properties else 0
    cpzu = cpz / 10  # Normalize CPZ to CPZU

    # Step 2: Assign points based on CPZU and the provided table
    if cpzu <= 1:
        cps_score = cpzu  # Direct mapping since 1 CPZU unit = 1 score point
    elif cpzu > 9.5:
        cps_score = 10
    else:
        # Find the score based on the CPZU range
        cps_score = next(score for score, range_min in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9, 9.5], start=1) if cpzu > range_min)

    return cps_score



def test():
    # Example list of Property objects with QoI scores
    properties = [
        Property(property_id=1, is_investor_owned=True, property_type='Single Family', sale_value=200000, rent_estimate=1500, cap_rate=0.09, sale_date='2022-01-15', quality_of_investment=5.5),
        Property(property_id=2, is_investor_owned=True, property_type='Condo', sale_value=150000, rent_estimate=1200, cap_rate=0.096, sale_date='2022-02-20', quality_of_investment=4.8),
        # More properties with their QoI scores
    ]

    # Calculate the CPS
    cps_score = calculate_concentration_properties_subscore(properties)
    print(f"Concentration Properties SubScore (CPS): {cps_score:.2f}")

# QOI, Investor Owned Required


