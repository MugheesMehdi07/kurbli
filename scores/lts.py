from data.models import Property


def calculate_liquidity_total_subscore(properties):
    """
    Calculate the Liquidity Total SubScore (LTS) based on the ratio of the total estimated
    value of properties sold recently to the total estimated value of all properties.

    :param properties: A list of Property objects with sale values and sold indicators.
    :return: The LTS score as a float.
    """
    if not properties:
        return 0

    total_sale_value_all = sum(prop.sale_value for prop in properties if prop.sale_value)
    total_sale_value_sold_recently = sum(prop.sale_value for prop in properties if prop.sold_recently and prop.sale_value)

    # Avoid division by zero
    if total_sale_value_all == 0:
        return 0

    # Calculate the liquidity ratio
    liquidity_ratio = total_sale_value_sold_recently / total_sale_value_all

    # For the LTS score, we need to scale the liquidity ratio. This scaling factor
    # depends on the market context. Let's assume a simple linear scaling for illustration.
    # The maximum ratio is considered 1 (or 100%), which maps directly to a score of 10.
    lts_score = liquidity_ratio * 10

    return lts_score


def main():
    # Example list of Property objects with sale values and sold indicators
    properties = [
        Property(property_id=1, sale_value=200000, sold_recently=True),
        Property(property_id=2, sale_value=150000, sold_recently=False),
        Property(property_id=3, sale_value=250000, sold_recently=True),
        # More properties...
    ]

    # Calculate the LTS
    lts_score = calculate_liquidity_total_subscore(properties)
    print(f"Liquidity Total SubScore (LTS): {lts_score:.2f}")

if __name__ == "__main__":
    main()


# Sale Value, Sold Recently Required
