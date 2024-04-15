class Property:
    def __init__(self, property_id, property_type, sale_value, rent_estimate, sale_date,
                 is_investor_owned, investor_type, new_investor, investor_zip, investor_city,
                 investor_state, property_zip, property_city, property_state, quality_of_investment,
                 sold_recently):
        """
        Initializes a new instance of the Property class.

        :param property_id: Unique identifier for the property.
        :param property_type: Type of the property (SFR, CON, TW, OTR).
        :param sale_value: Sale price or current market value of the property.
        :param rent_estimate: Estimated annual rent for the property.
        :param sale_date: Date the property was sold (YYYY-MM-DD).
        :param is_investor_owned: Indicates if the property is owned by an investor.
        :param investor_type: Type of the investor (Investment Fund, Corporate Investor, Mom/Pop Investor).
        :param new_investor: Indicates if the property was purchased by a new investor.
        :param investor_zip: Zip code of the investor.
        :param investor_city: City of the investor.
        :param investor_state: State of the investor.
        :param property_zip: Zip code of the property.
        :param property_city: City where the property is located.
        :param property_state: State where the property is located.
        :param quality_of_investment: Quality of Investment score for the property.
        :param sold_recently: Indicates if the property was sold in the relevant timeframe for liquidity calculation.
        """
        self.property_id = property_id
        self.property_type = property_type
        self.sale_value = sale_value
        self.rent_estimate = rent_estimate
        self.sale_date = sale_date
        self.is_investor_owned = is_investor_owned
        self.investor_type = investor_type
        self.new_investor = new_investor
        self.investor_zip = investor_zip
        self.investor_city = investor_city
        self.investor_state = investor_state
        self.property_zip = property_zip
        self.property_city = property_city
        self.property_state = property_state
        self.quality_of_investment = quality_of_investment
        self.sold_recently = sold_recently
