
# table6_mediation_model.py
# Mediation analysis: Preventive behavior as mediator between mistrust and sleep quality

import pandas as pd
import numpy as np
from sklearn.utils import resample
from statsmodels.formula.api import ols
from scipy.stats import chi2

# Load dataset
df = pd.read_csv("Gesundheitskompetenz_MistrustIndex.csv", sep=";", encoding="utf-8")
df['GEwicht'] = pd.to_numeric(df['GEwicht'], errors='coerce')
df['Mistrust'] = df['Mistrust_Index']
df['SleepQuality'] = df['bpsqi_score']
df['Gender'] = df['Gender M=0 F=1']
df['Education'] = df['Education New']
chronic_cols = ['Pulmonary Disease', 'CV-Disease', 'Hypertension', 'Nephropathy',
                'Immune Disease', 'Cancer', 'Metabolic Disease', 'Liver Disease', 'Mental Disease']
df['Chronic'] = df[chronic_cols].any(axis=1).astype(int)

# Define HBC mediators
mediators = {
    'HBC-Regular Checkups 10': 'Checkups',
    'HBC-See Dentist 4': 'Dentist',
    'HBC-Gather Info 7': 'Information Seeking',
    'HBC-Discuss Health 12': 'Health Discussion',
    'HBC-Get Shots 15': 'Vaccination'
}

# Run mediation model for each mediator
results = []

for col, label in mediators.items():
    df['Mediator'] = df[col]
    med_df = df[['Mistrust', 'Mediator', 'SleepQuality', 'Age Years', 'Gender', 'Education', 'Chronic', 'GEwicht']].dropna()

    a_model = ols("Mediator ~ Mistrust + Q('Age Years') + Gender + C(Education) + Chronic", data=med_df).fit()
    b_model = ols("SleepQuality ~ Mistrust + Mediator + Q('Age Years') + Gender + C(Education) + Chronic", data=med_df).fit()
    total_model = ols("SleepQuality ~ Mistrust + Q('Age Years') + Gender + C(Education) + Chronic", data=med_df).fit()

    a = a_model.params['Mistrust']
    b = b_model.params['Mediator']
    c_prime = b_model.params['Mistrust']
    c_total = total_model.params['Mistrust']
    indirect = a * b

    boot_indirect = []
    for _ in range(100):
        sample = resample(med_df, replace=True)
        a_bs = ols("Mediator ~ Mistrust + Q('Age Years') + Gender + C(Education) + Chronic", data=sample).fit().params['Mistrust']
        b_bs = ols("SleepQuality ~ Mistrust + Mediator + Q('Age Years') + Gender + C(Education) + Chronic", data=sample).fit().params['Mediator']
        boot_indirect.append(a_bs * b_bs)

    ci_low = np.percentile(boot_indirect, 2.5)
    ci_high = np.percentile(boot_indirect, 97.5)

    results.append({
        "Mediator": label,
        "a (X→M)": round(a, 3),
        "b (M→Y)": round(b, 3),
        "c (total)": round(c_total, 3),
        "c′ (direct)": round(c_prime, 3),
        "Indirect (a*b)": round(indirect, 3),
        "95% CI": f"[{round(ci_low, 3)}, {round(ci_high, 3)}]"
    })

# Display results
table = pd.DataFrame(results)
print(table.to_string(index=False))
