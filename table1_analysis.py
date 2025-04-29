
# table1_analysis.py
# Analysis script for computing descriptive statistics (weighted and unweighted) and p-values

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, chi2_contingency
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("Gesundheitskompetenz_MistrustIndex.csv", sep=";", encoding="utf-8")

# Ensure weights are numeric
df['GEwicht'] = pd.to_numeric(df['GEwicht'], errors='coerce')

# Function for weighted mean and standard deviation
def weighted_mean_std(series, weights):
    weighted_mean = np.average(series, weights=weights)
    variance = np.average((series - weighted_mean) ** 2, weights=weights)
    return weighted_mean, np.sqrt(variance)

# Compute mistrust index statistics
mistrust_mean_uw = df['Mistrust_Index'].mean()
mistrust_mean_w, mistrust_std_w = weighted_mean_std(df['Mistrust_Index'], df['GEwicht'])

# Example for PSQI
psqi_mean_uw = df['bpsqi_score'].mean()
psqi_mean_w, psqi_std_w = weighted_mean_std(df['bpsqi_score'], df['GEwicht'])

# Gender comparison (chi-square)
gender_table = pd.crosstab(df['Gender M=0 F=1'], columns="count")
gender_weighted = df.groupby('Gender M=0 F=1')['GEwicht'].sum()
chi2_gender, p_gender, _, _ = chi2_contingency([
    [gender_table.loc[0].values[0], gender_table.loc[1].values[0]],
    [gender_weighted.loc[0], gender_weighted.loc[1]]
])

# Additional statistical calculations can be added here...

print("Weighted and unweighted mean of Mistrust Index:", mistrust_mean_uw, mistrust_mean_w)
print("Weighted and unweighted mean of PSQI:", psqi_mean_uw, psqi_mean_w)
print("Chi-square test for gender: p-value =", p_gender)
