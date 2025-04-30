
# Mediation Analysis: Preventive Behavior and Sleep Quality

This script tests whether various preventive behaviors mediate the relationship between mistrust in professional health information and sleep quality.

## Model:
- X = Mistrust Index
- M = Preventive behavior (Vaccination, Checkups, etc.)
- Y = B-PSQI Sleep Quality score

Each behavior is tested individually. The script estimates:
- Direct and total effects
- Indirect effect (a × b)
- Bootstrapped 95% confidence interval (n=100)

All models adjust for age, gender, education, and chronic illness, and use weighted survey data.

## How to run:

```bash
pip install -r requirements.txt
python table6_mediation_model.py
```
