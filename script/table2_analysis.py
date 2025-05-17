
# table2_analysis.py
# Script to compute associations between Mistrust Index and sleep quality (PSQI)

import pandas as pd
import numpy as np
from scipy.stats import spearmanr, kruskal
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Load dataset
df = pd.read_csv("Gesundheitskompetenz_MistrustIndex.csv", sep=";", encoding="utf-8")

# Create chronic disease flag
chronic_cols = ['Pulmonary Disease', 'CV-Disease', 'Hypertension', 'Nephropathy',
                'Immune Disease', 'Cancer', 'Metabolic Disease', 'Liver Disease', 'Mental Disease']
df['has_chronic'] = df[chronic_cols].any(axis=1).astype(int)

# Create mistrust tertiles
df['mistrust_group'] = pd.qcut(df['Mistrust_Index'], q=3, labels=["Low", "Medium", "High"])

# Spearman correlation
corr, p_corr = spearmanr(df['Mistrust_Index'], df['bpsqi_score'])

# Kruskal–Wallis test across mistrust tertiles
groups = [group['bpsqi_score'].dropna() for _, group in df.groupby('mistrust_group')]
kruskal_stat, p_kruskal = kruskal(*groups)

# Prepare regression dataset
df_model = df[['bpsqi_score', 'Mistrust_Index', 'Age Years', 'Gender M=0 F=1', 'Education New', 'has_chronic']].dropna()
df_model = df_model.rename(columns={
    'Gender M=0 F=1': 'Gender_binary',
    'Age Years': 'Age_Years',
    'Education New': 'Education_New'
})

# Ordinary least squares regression
X = pd.get_dummies(df_model[['Mistrust_Index', 'Age_Years', 'Gender_binary', 'Education_New', 'has_chronic']], drop_first=True)
y = df_model['bpsqi_score']
X = sm.add_constant(X)
ols_model = sm.OLS(y, X).fit()
ols_summary = ols_model.summary2().tables[1]
ols_r2 = ols_model.rsquared

# Robust regression (Huber's M-estimator)
X_df = X.copy()
X_df['bpsqi_score'] = y
formula = "bpsqi_score ~ " + " + ".join([col for col in X_df.columns if col != "bpsqi_score"])
robust_model = smf.rlm(formula=formula, data=X_df, M=sm.robust.norms.HuberT()).fit()
robust_summary = robust_model.summary2().tables[1]

# Extract relevant results
print("Spearman correlation rho =", corr, "p =", p_corr)
print("Kruskal-Wallis test statistic =", kruskal_stat, "p =", p_kruskal)
print("OLS regression beta =", ols_summary.loc['Mistrust_Index']['Coef.'], "p =", ols_summary.loc['Mistrust_Index']['P>|t|'], "R² =", ols_r2)
print("Robust regression beta =", robust_summary.loc['Mistrust_Index']['Coef.'], "p =", robust_summary.loc['Mistrust_Index']['P>|z|'])
