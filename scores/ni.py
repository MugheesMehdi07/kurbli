from datetime import datetime, timedelta

from data.models import Property


def calculate_new_investors_subscore(properties):
    """
    Calculate the New Investors SubScore (NI) based on the influx of new investors
    into the market over specific recent time frames.

    :param properties: A list of Property objects with sale dates and new investor indicators.
    :return: The NI score as a float.
    """
    # Define time frames for calculation
    now = datetime.now()
    time_frames = [
        (now - timedelta(days=30), now),
        (now - timedelta(days=60), now - timedelta(days=31)),
        (now - timedelta(days=90), now - timedelta(days=61)),
        (now - timedelta(days=180), now - timedelta(days=91)),
        (now - timedelta(days=360), now - timedelta(days=181)),
    ]

    # Initialize counters for new investors in each time frame
    new_investors_counts = [0 for _ in time_frames]

    for prop in properties:
        if prop.new_investor:
            sale_date = datetime.strptime(prop.sale_date, "%Y-%m-%d")
            for i, (start, end) in enumerate(time_frames):
                if start < sale_date <= end:
                    new_investors_counts[i] += 1
                    break

    # Calculate total new investors for normalization
    total_new_investors = sum(new_investors_counts)
    if total_new_investors == 0:
        return 0

    # Calculate weighted score for each time frame
    # Assuming equal weight for simplicity; adjust as needed
    weights = [1, 1, 1, 1, 1]
    ni_score = sum(count * weight for count, weight in zip(new_investors_counts, weights)) / total_new_investors

    # Normalize the score to a scale of 0 to 10
    ni_score = (ni_score / len(time_frames)) * 10

    return ni_score



def main():
    # Example list of Property objects with sale dates and new investor indicators
    properties = [
        Property(property_id=1, sale_date="2024-03-01", new_investor=True),
        Property(property_id=2, sale_date="2024-02-15", new_investor=True),
        Property(property_id=3, sale_date="2024-01-10", new_investor=False),
        # More properties...
    ]

    # Calculate the NI
    ni_score = calculate_new_investors_subscore(properties)
    print(f"New Investors SubScore (NI): {ni_score:.2f}")

if __name__ == "__main__":
    main()
