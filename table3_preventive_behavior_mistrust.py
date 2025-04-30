
# table5_preventive_behavior_mistrust.py
# Weighted analysis of preventive health behaviors by mistrust level

import pandas as pd
from scipy.stats import chi2

# Load dataset
df = pd.read_csv("Gesundheitskompetenz_MistrustIndex.csv", sep=";", encoding="utf-8")
df['mistrust_group'] = pd.qcut(df['Mistrust_Index'], q=3, labels=["Low", "Medium", "High"])
df['GEwicht'] = pd.to_numeric(df['GEwicht'], errors='coerce')

# HBC items
hbc_vars = {
    'HBC-Get Shots 15': 'Vaccination',
    'HBC-Regular Checkups 10': 'Checkups',
    'HBC-See Dentist 4': 'Dentist',
    'HBC-Gather Info 7': 'Information Seeking',
    'HBC-Discuss Health 12': 'Health Discussion'
}

# Melt to long format
hbc_data = df[['mistrust_group', 'GEwicht'] + list(hbc_vars.keys())].copy()
hbc_long = hbc_data.melt(id_vars=['mistrust_group', 'GEwicht'], var_name='Item', value_name='Response')
hbc_long['Item Label'] = hbc_long['Item'].map(hbc_vars)
hbc_long = hbc_long.dropna(subset=['Response', 'GEwicht'])

# Function to compute weighted tables and p-values
def weighted_hbc_distribution(df, hbc_vars):
    full_table = []
    for item, label in hbc_vars.items():
        df_item = df[df['Item'] == item]
        pivot = pd.pivot_table(df_item, values='GEwicht', index='Response', columns='mistrust_group', aggfunc='sum', fill_value=0)
        row_totals = pivot.sum(axis=1)
        percent = (pivot.T / row_totals).T * 100
        formatted = pivot.round(0).astype(int).astype(str) + " (" + percent.round(1).astype(str) + "%)"
        formatted.insert(0, "Response", formatted.index)
        formatted["Total N (weighted)"] = row_totals.round(0).astype(int).values
        formatted.reset_index(drop=True, inplace=True)
        formatted["p-value"] = ""
        total = pivot.values.sum()
        row_sums = pivot.sum(axis=1).values.reshape(-1, 1)
        col_sums = pivot.sum(axis=0).values.reshape(1, -1)
        expected = row_sums @ col_sums / total
        chi2_stat = ((pivot.values - expected) ** 2 / expected).sum()
        dof = (pivot.shape[0] - 1) * (pivot.shape[1] - 1)
        p_val = 1 - chi2.cdf(chi2_stat, dof)
        formatted.loc[0, 'p-value'] = round(p_val, 3)
        section_title = pd.DataFrame([[f"--- {label} ---"] + [""] * (formatted.shape[1] - 1)], columns=formatted.columns)
        full_table.append(pd.concat([section_title, formatted], ignore_index=True))
    return pd.concat(full_table, ignore_index=True)

# Generate and display table
final_table = weighted_hbc_distribution(hbc_long, hbc_vars)
print(final_table.to_string(index=False))
