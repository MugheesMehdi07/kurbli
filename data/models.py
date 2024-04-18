# models.py

class Property:
    def __init__(self, address, cap_rate, number_of_nxo_sfrs, number_of_rsfr, neighborhood_crime_rating, school_score,flood_factor_score):
        self.address = address
        self.cap_rate = cap_rate
        self.number_of_nxo_sfrs = number_of_nxo_sfrs
        self.number_of_rsfr = number_of_rsfr
        self.neighborhood_crime_rating = neighborhood_crime_rating
        self.school_score = school_score
        self.flood_factor_score = flood_factor_score
        self.investibility_score = 0

    def to_dict(self):
        """Converts the property data to a dictionary format suitable for API responses."""
        return {
            "address": self.address,
            "cap_rate": self.cap_rate,
            "number_of_nxo_sfrs": self.number_of_nxo_sfrs,
            "number_of_rsfr": self.number_of_rsfr,
            "neighborhood_crime_rating": self.neighborhood_crime_rating,
            "school_score": self.school_score,
            "flood_factor_score": self.flood_factor_score,
            "investibility_score": self.investibility_score
        }


    @staticmethod
    def validate_cap_rate(rate):
        """Validates that the cap rate is a non-negative float."""
        if not isinstance(rate, float) or rate < 0:
            raise ValueError("Cap Rate must be a non-negative float.")

    # Additional validation methods can be added here.
