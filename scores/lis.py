def calculate_liquidity_investable_subscore(properties):
    """
    Calculate the Liquidity Investable SubScore (LIS) based on the ratio of the total
    estimated value of properties purchased by investors recently to the total sales
    value of all properties sold in the same period.

    :param properties: A list of Property objects with sale values, sold indicators,
                       and investor ownership status.
    :return: The LIS score as a float.
    """
    if not properties:
        return 0

    # Total sale value of all properties sold recently
    total_sale_value_sold_recently = sum(prop.sale_value for prop in properties if prop.sold_recently and prop.sale_value)

    # Total sale value of properties sold recently that were investor-owned
    total_investor_purchase_value = sum(prop.sale_value for prop in properties if prop.sold_recently and prop.investor_owned and prop.sale_value)

    # Avoid division by zero
    if total_sale_value_sold_recently == 0:
        return 0

    # Calculate the investable liquidity ratio
    investable_liquidity_ratio = total_investor_purchase_value / total_sale_value_sold_recently

    # For the LIS score, let's assume a simple linear scaling. The maximum ratio is
    # considered 1 (or 100%), which maps directly to a score of 10.
    lis_score = investable_liquidity_ratio * 10

    return lis_score


def test():
    # Example list of Property objects with relevant attributes
    properties = [
        Property(property_id=1, sale_value=200000, sold_recently=True, investor_owned=True),
        Property(property_id=2, sale_value=150000, sold_recently=True, investor_owned=False),
        Property(property_id=3, sale_value=250000, sold_recently=True, investor_owned=True),
        # More properties...
    ]

    # Calculate the LIS
    lis_score = calculate_liquidity_investable_subscore(properties)
    print(f"Liquidity Investable SubScore (LIS): {lis_score:.2f}")

if __name__ == "__main__":
    main()
