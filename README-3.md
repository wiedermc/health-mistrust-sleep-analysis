
# Health Mistrust and Sleep Quality Analysis

This repository contains Python scripts for analyzing a population-based survey from South Tyrol on health information mistrust, preventive health behavior, and sleep quality.

## Folder Structure

```
health-mistrust-sleep-analysis/
│
├── table1_analysis.py               # Generates Table 1: Weighted/unweighted descriptives
├── table2_analysis.py               # Generates Table 2: Mistrust and B-PSQI
├── table3_analysis.py               # Generates Table 3: Preventive behavior and B-PSQI
├── mediation_model.py               # Placeholder for future mediation analysis
├── requirements.txt                 # Required Python packages
├── README.md                        # Project overview and usage instructions
└── data/
    └── Gesundheitskompetenz_MistrustIndex.csv   # Source data (not included for privacy)
```

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run analysis scripts:

```bash
python table1_analysis.py
python table2_analysis.py
python table3_analysis.py
```

## Notes

- Regression models include adjustments for age, gender, education level, and chronic disease.
- Robust regression (Huber M-estimator) confirms the stability of results.
- Scripts use `pandas`, `scipy`, and `statsmodels`.

## Author

Project developed as part of population health research in South Tyrol.
