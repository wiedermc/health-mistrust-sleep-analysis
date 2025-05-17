
# table3_analysis.py
# Analysis script: Association between preventive health behaviors and sleep quality (B-PSQI)

import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Load dataset
df = pd.read_csv("Gesundheitskompetenz_MistrustIndex.csv", sep=";", encoding="utf-8")

# Create chronic disease flag
chronic_cols = ['Pulmonary Disease', 'CV-Disease', 'Hypertension', 'Nephropathy',
                'Immune Disease', 'Cancer', 'Metabolic Disease', 'Liver Disease', 'Mental Disease']
df['has_chronic'] = df[chronic_cols].any(axis=1).astype(int)

# Select and rename relevant HBC items
hbc_items = {
    'HBC-Get Shots 15': 'HBC_GetShots15',
    'HBC-Regular Checkups 10': 'HBC_Checkups10',
    'HBC-See Dentist 4': 'HBC_Dentist4',
    'HBC-Gather Info 7': 'HBC_Info7',
    'HBC-Discuss Health 12': 'HBC_Discuss12'
}
df = df.rename(columns=hbc_items)

# Prepare model data
all_vars = ['bpsqi_score', 'Age Years', 'Gender M=0 F=1', 'Education New', 'has_chronic'] + list(hbc_items.values())
df_model = df[all_vars].dropna()
df_model = df_model.rename(columns={
    'Age Years': 'Age_Years',
    'Gender M=0 F=1': 'Gender_binary',
    'Education New': 'Education_New'
})

# Correlation analysis
print("Spearman correlations:")
for var in hbc_items.values():
    corr, pval = spearmanr(df[var], df['bpsqi_score'], nan_policy='omit')
    print(f"{var}: ρ = {corr:.2f}, p = {pval:.3f}")

# Regression models
print("\nOLS Regression (adjusted):")
for var in hbc_items.values():
    formula = f"bpsqi_score ~ {var} + Age_Years + Gender_binary + C(Education_New) + has_chronic"
    model = smf.ols(formula=formula, data=df_model).fit()
    print(f"{var}: β = {model.params[var]:.2f}, 95% CI = {model.conf_int().loc[var].values}, p = {model.pvalues[var]:.3f}, R² = {model.rsquared:.3f}")

# Robust regression
print("\nRobust Regression (Huber M-estimator):")
for var in hbc_items.values():
    formula = f"bpsqi_score ~ {var} + Age_Years + Gender_binary + C(Education_New) + has_chronic"
    model = smf.rlm(formula=formula, data=df_model, M=sm.robust.norms.HuberT()).fit()
    print(f"{var}: β = {model.params[var]:.2f}, 95% CI = {model.conf_int().loc[var].values}, p = {model.pvalues[var]:.3f}")
