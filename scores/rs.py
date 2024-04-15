from data.models import Property


def calculate_regionality_subscore(properties):
    """
    Calculate the Regionality SubScore (RS) based on the distribution of investment
    activity across different geographical levels (zip code, city, state, outside state).

    :param properties: A list of Property objects with investor location attributes.
    :return: The RS score as a float.
    """
    if not properties:
        return 0

    # Initialize counters for each regionality category
    same_zip, same_city, same_state, outside_state = 0, 0, 0, 0

    for prop in properties:
        if prop.property_zip == prop.investor_zip:
            same_zip += 1
        elif prop.property_city == prop.investor_city:
            same_city += 1
        elif prop.property_state == prop.investor_state:
            same_state += 1
        else:
            outside_state += 1

    # Calculate total properties for denominator to avoid division by zero
    total_properties = len(properties)
    if total_properties == 0:
        return 0

    # Calculate percentages for each category
    pct_same_zip = same_zip / total_properties
    pct_same_city = same_city / total_properties
    pct_same_state = same_state / total_properties
    pct_outside_state = outside_state / total_properties

    # Define how each percentage contributes to the RS score.
    # For simplicity, let's equally weight each category for a max score of 10.
    # Adjust the weighting as needed to match your scoring criteria.
    rs_score = (pct_same_zip + pct_same_city + pct_same_state + pct_outside_state) * 2.5

    return rs_score


def test():
    # Example list of Property objects with investor location details
    properties = [
        Property(property_id=1, is_investor_owned=True, property_zip='10001', property_city='New York', property_state='NY', investor_zip='10001', investor_city='New York', investor_state='NY', quality_of_investment=5.5),
        Property(property_id=2, is_investor_owned=True, property_zip='90001', property_city='Los Angeles', property_state='CA', investor_zip='10001', investor_city='New York', investor_state='NY', quality_of_investment=6.0),
        # More properties with location and investor details
    ]

    # Calculate the RS
    rs_score = calculate_regionality_subscore(properties)
    print(f"Regionality SubScore (RS): {rs_score:.2f}")

# QOI Score, Investor Zip, City, State Required