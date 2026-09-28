import pandas as pd
import numpy as np

# 1. Ingest the raw fictionalized dataset
df = pd.read_csv('distributor_sales_2026_Q2.csv')

# 2. Standardize text for cleaner SQL matching (uppercase, strip whitespace)
df['customer_name_clean'] = df['customer_name'].str.upper().str.strip()
df['customer_address_clean'] = df['customer_address'].str.upper().str.strip()

# 3. Handle missing Customer IDs (Flag them for the exception report)
df['customer_id'] = df['customer_id'].fillna('MISSING_ID')

# 4. Process negative values (Ensure returns are mathematically handled, not deleted)
# We keep the negative amount but ensure the transaction_type explicitly flags it.
df.loc[df['sales_amount'] < 0, 'transaction_type'] = 'Return/Credit'
df.loc[df['sales_amount'] > 0, 'transaction_type'] = 'Sale'

# 5. Create the exception review flag
df['needs_review'] = np.where(df['customer_id'] == 'MISSING_ID', True, False)

# Export the clean staging table for SQL ingestion
df.to_csv('stg_distributor_sales.csv', index=False)
print(f"Processing complete: {len(df[df['needs_review'] == True])} records flagged for review.")