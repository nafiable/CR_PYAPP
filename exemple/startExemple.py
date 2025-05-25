"""
This file is used to test the analysis functions locally without using the API.
"""

# Import the function to generate sample data
from exemple.peuplerDatabase import generate_sample_dataframe
# Import the analysis function
from analysis.data_analyzer import calculate_market_value_by_asset_type, calculate_market_value_by_fund_country_asset_type, calculate_weight_by_fund, calculate_weight_by_asset_type_and_fund, calculate_weight_by_asset_type_and_manager

# Generate the sample data
sample_df = generate_sample_dataframe()

# Calculate market value by asset type
market_value_by_asset = calculate_market_value_by_asset_type(sample_df)

# Print the result
print("Valeur Marchande par Type d'Actif:")
print(market_value_by_asset)

# Calculate market value by fund, country, and asset type
market_value_by_fund_country_asset = calculate_market_value_by_fund_country_asset_type(sample_df)

# Print the result for the new calculation
print("\nValeur Marchande par Fonds, Pays et Type d'Actif:")
print(market_value_by_fund_country_asset)

# Calculate weight by fund for each title
df_with_weight = calculate_weight_by_fund(sample_df)

# Print the dataframe with the new 'Weight by Fund' column
print("\nDataFrame avec Poids par Fonds:")
print(df_with_weight)

# Calculate weight by asset type and fund for each title
df_with_weight_by_asset_and_fund = calculate_weight_by_asset_type_and_fund(sample_df)

# Print the dataframe with the new 'Weight by Asset Type and Fund' column
print("\nDataFrame avec Poids par Type d'Actif et par Fonds:")
print(df_with_weight_by_asset_and_fund)

# Calculate weight by asset type and manager for each title
df_with_weight_by_asset_and_manager = calculate_weight_by_asset_type_and_manager(sample_df)

# Print the dataframe with the new 'Weight by Asset Type and Manager' column
print("\nDataFrame avec Poids par Type d'Actif et par Gestionnaire:")
print(df_with_weight_by_asset_and_manager)