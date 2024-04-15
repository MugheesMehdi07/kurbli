from data.models import Property


def calculate_institutionality_subscore(properties):
    """
    Calculate the Institutionality SubScore (IS) based on the distribution of properties
    owned by different types of investors (Investment Funds, Corporate Investors, Mom/Pop Investors).

    :param properties: A list of Property objects with investor type attributes.
    :return: The IS score as a float.
    """
    if not properties:
        return 0

    # Initialize counters for each investor type
    investment_funds, corporate_investors, mom_pop_investors = 0, 0, 0

    for prop in properties:
        if prop.investor_type == "Investment Fund":
            investment_funds += 1
        elif prop.investor_type == "Corporate Investor":
            corporate_investors += 1
        elif prop.investor_type == "Mom/Pop Investor":
            mom_pop_investors += 1

    # Calculate total investor-owned properties for denominator to avoid division by zero
    total_investor_properties = investment_funds + corporate_investors + mom_pop_investors
    if total_investor_properties == 0:
        return 0

    # Calculate percentages for each investor type
    pct_investment_funds = investment_funds / total_investor_properties
    pct_corporate_investors = corporate_investors / total_investor_properties
    pct_mom_pop_investors = mom_pop_investors / total_investor_properties

    # Define how each percentage contributes to the IS score.
    # For simplicity, let's assume equal importance and a straightforward aggregation.
    # Adjust the methodology as necessary to reflect your analysis needs.
    is_score = (pct_investment_funds * 3.3) + (pct_corporate_investors * 3.3) + (pct_mom_pop_investors * 3.4)

    return is_score


def test():
    # Example list of Property objects with investor type details
    properties = [
        Property(property_id=1, is_investor_owned=True, investor_type='Investment Fund', quality_of_investment=5.5),
        Property(property_id=2, is_investor_owned=True, investor_type='Corporate Investor', quality_of_investment=6.0),
        # More properties with investor type details
    ]

    # Calculate the IS
    is_score = calculate_institutionality_subscore(properties)
    print(f"Institutionality SubScore (IS): {is_score:.2f}")


# QOI Score, Investor Type Required

