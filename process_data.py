import pandas as pd
import glob

# Read and combine CSV files
all_files = glob.glob("data/*.csv")
combined_df = pd.concat([pd.read_csv(file) for file in all_files], ignore_index=True)

# Filter for Pink Morsels and create an explicit copy
pink_morsels_df = combined_df[combined_df['product'] == 'pink morsel'].copy()

# Clean price column (remove $ and convert to float)
pink_morsels_df.loc[:, 'price'] = (
    pink_morsels_df['price']
    .str.replace('$', '', regex=False)
    .astype(float)
)

# Calculate sales
pink_morsels_df.loc[:, 'sales'] = (
    pink_morsels_df['price'] * pink_morsels_df['quantity']
)

# Save output
pink_morsels_df[['sales', 'date', 'region']].to_csv(
    'processed_pink_morsels.csv', index=False
)
