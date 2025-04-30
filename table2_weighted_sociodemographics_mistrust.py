
# table4_weighted_sociodemographics.py
# Weighted sociodemographic distribution by mistrust level (row-wise % and chi-square p-values)

import pandas as pd
from scipy.stats import chi2_contingency

# Load data
df = pd.read_csv("Gesundheitskompetenz_MistrustIndex.csv", sep=";", encoding="utf-8")
df['mistrust_group'] = pd.qcut(df['Mistrust_Index'], q=3, labels=["Low", "Medium", "High"])
df['GEwicht'] = pd.to_numeric(df['GEwicht'], errors='coerce')

# Clean & map
plot_data = df[['mistrust_group', 'Age Years', 'Gender M=0 F=1', 'Education New', 'Language ', 'GEO', 'GEwicht']].copy()
plot_data['Gender'] = plot_data['Gender M=0 F=1'].map({0: 'Male', 1: 'Female'}).fillna("Unknown")
plot_data['Education'] = plot_data['Education New'].map({1: 'Middle or vocational school', 2: 'High school', 3: 'University'}).fillna("Unknown")
plot_data['Language'] = df['Language '].map({
    'D': 'German', 'A1': 'German', 'I': 'Italian', 'A2': 'Italian',
    'Z': 'Other', 'A3': 'Other', 'A4': 'Other', 'A5': 'Other', 'A5b': 'Other'
}).fillna("Unknown")
plot_data['Region'] = df['GEO'].map({'BZ': 'Urban', 'NB': 'Rural'}).fillna("Unknown")
plot_data['Age Group'] = pd.cut(df['Age Years'], bins=[17, 34, 54, 74, 100], labels=["18–34", "35–54", "55–74", "75+"], include_lowest=True)

# Weighted chi-square function
def weighted_chi2_pvalue(df, var_col):
    weighted_table = pd.pivot_table(df, values='GEwicht', index=var_col, columns='mistrust_group', aggfunc='sum', fill_value=0)
    total = weighted_table.values.sum()
    row_totals = weighted_table.sum(axis=1).values.reshape(-1, 1)
    col_totals = weighted_table.sum(axis=0).values.reshape(1, -1)
    expected = row_totals @ col_totals / total
    observed = weighted_table.values
    chi2_stat = ((observed - expected) ** 2 / expected).sum()
    dof = (observed.shape[0] - 1) * (observed.shape[1] - 1)
    from scipy.stats import chi2
    return round(1 - chi2.cdf(chi2_stat, dof), 3)

# Build table
def weighted_rowwise_distribution(df, var_col, var_label):
    df_valid = df[[var_col, 'mistrust_group', 'GEwicht']].dropna()
    weighted = df_valid.groupby([var_col, 'mistrust_group'])['GEwicht'].sum().unstack(fill_value=0)
    row_totals = weighted.sum(axis=1)
    weighted_perc = (weighted.T / row_totals).T * 100
    merged = weighted.round(0).astype(int).astype(str) + " (" + weighted_perc.round(1).astype(str) + "%)"
    merged.insert(0, "Variable", merged.index)
    merged["Total N (weighted)"] = row_totals.round(0).astype(int).values
    merged.reset_index(drop=True, inplace=True)
    merged["p-value"] = ""
    merged.loc[0, "p-value"] = weighted_chi2_pvalue(df, var_col)
    section_title = pd.DataFrame([[f"--- {var_label} ---"] + [""] * (merged.shape[1] - 1)], columns=merged.columns)
    return pd.concat([section_title, merged], ignore_index=True)

# Generate full table
tabs = [
    weighted_rowwise_distribution(plot_data, "Age Group", "Age Group"),
    weighted_rowwise_distribution(plot_data, "Gender", "Gender"),
    weighted_rowwise_distribution(plot_data, "Education", "Education"),
    weighted_rowwise_distribution(plot_data, "Language", "Language"),
    weighted_rowwise_distribution(plot_data, "Region", "Region")
]
final_table = pd.concat(tabs, ignore_index=True)

# Output
print(final_table.to_string(index=False))
