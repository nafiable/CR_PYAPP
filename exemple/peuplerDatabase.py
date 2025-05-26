"""
This file contains code to generate a sample pandas DataFrame
representing portfolio data for testing purposes.
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)

def generate_sample_portfolio_data():
    """
    Generates a sample pandas DataFrame with portfolio data.

    The DataFrame includes the following columns:
    - 'Fund': The name of the investment fund.
    - 'Country': The country of the investment.
    - 'Asset Type': The type of asset (e.g., Stock, Bond, Real Estate).
    - 'Market Value': The market value of the investment.
    - 'Sector': The sector of the investment (e.g., Technology, Finance, Healthcare).
    - 'Manager': The name of the fund manager.

    Returns:
        pandas.DataFrame: A DataFrame containing sample portfolio data.
    """
    data = {
        'Fund': ['Fund A', 'Fund A', 'Fund B', 'Fund A', 'Fund C', 'Fund B', 'Fund C', 'Fund A', 'Fund B', 'Fund C'],
        'Country': ['USA', 'Canada', 'USA', 'UK', 'Germany', 'France', 'USA', 'USA', 'Canada', 'Germany'],
        'Asset Type': ['Stock', 'Bond', 'Stock', 'Real Estate', 'Stock', 'Bond', 'Stock', 'Bond', 'Real Estate', 'Stock'],
        'Market Value': [100000, 50000, 150000, 200000, 75000, 60000, 120000, 80000, 180000, 90000],
        'Sector': ['Technology', 'Government', 'Finance', 'Residential', 'Healthcare', 'Corporate', 'Technology', 'Government', 'Commercial', 'Finance'],
        'Manager': ['Manager X', 'Manager Y', 'Manager X', 'Manager Z', 'Manager Y', 'Manager Z', 'Manager X', 'Manager Y', 'Manager Z', 'Manager X']
    }
    df = pd.DataFrame(data)
    logger.info("Generated sample portfolio DataFrame.")
    return df

if __name__ == '__main__':
    # Example usage:
    sample_df = generate_sample_portfolio_data()
    logger.info("Sample DataFrame:\n%s", sample_df)