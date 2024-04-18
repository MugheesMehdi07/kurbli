def calculate_investibility_score(property):
    score = 0

    # Step 1: Cap Rate Scoring
    if property.cap_rate >= 10:
        score += 30
    elif 8 <= property.cap_rate < 10:
        score += 8
    elif 5 <= property.cap_rate < 8:
        score += 5
    elif property.cap_rate < 5:
        score += 0

    # Step 2: Number of NxO SFRs Scoring
    if property.number_of_nxo_sfrs > 20:
        score += 20
    elif 10 <= property.number_of_nxo_sfrs <= 20:
        score += 8
    elif 5 <= property.number_of_nxo_sfrs < 10:
        score += 5
    elif 1 < property.number_of_nxo_sfrs < 5:
        score += 2
    elif property.number_of_nxo_sfrs <= 1:
        score += 1

    # Step 3: Number of rSFRs Scoring
    if property.number_of_rsfr > 20:
        score += 20
    elif 10 <= property.number_of_rsfr <= 20:
        score += 8
    elif 5 <= property.number_of_rsfr < 10:
        score += 5
    elif 1 < property.number_of_rsfr < 5:
        score += 2
    elif property.number_of_rsfr <= 1:
        score += 1

    # Step 4: Flood Factor Scoring
    if 1 <= property.flood_factor_score <= 2:
        score += 10
    elif 3 <= property.flood_factor_score <= 6:
        score += 7
    elif 7 <= property.flood_factor_score <= 8:
        score += 3
    else:
        score += 1

    # Step 5: Crime Factor Scoring
    crime_factor = property.neighborhood_crime_rating
    if 1 <= crime_factor <= 2:
        score += 10
    elif 3 <= crime_factor <= 6:
        score += 7
    elif 7 <= crime_factor <= 8:
        score += 3
    else:
        score += 1

    # Step 6: School Rating Scoring
    if property.school_score > 7:
        score += 10
    elif property.school_score > 5:
        score += 7
    elif property.school_score > 3:
        score += 3
    else:
        score += 1

    # Step 8: Determining the Ranking
    if score >= 99:
        ranking = "Diamond"
    elif 90 <= score <= 98:
        ranking = "Platinum"
    elif 85 <= score <= 89:
        ranking = "Gold"
    elif 75 <= score <= 84:
        ranking = "Silver"
    else:
        ranking = "Bronze"

    return f"{score},{ranking}"


# # Example property data for testing the function
# property_data = {
#     'cap_rate': 9,
#     'number_of_nxo_sfrs': 15,
#     'number_of_rsfr': 4,
#     'flood_factor_score': 2,
#     'neighborhood_crime_rating': 1,
#     'school_score': 10
# }
#
# # Calculate score and print result
# result = calculate_investibility_score(property_data)
# print(result)
