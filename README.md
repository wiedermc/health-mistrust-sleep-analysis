
# Health Information Mistrust, Preventive Behavior, and Sleep Quality

This repository contains data and analysis scripts for the manuscript:

**"Health Information Mistrust, Preventive Health Behavior, and Sleep Quality: A Population-Based Study"**  
Submitted to *Healthcare 2025*

---

## 📦 Dataset

- **`Gesundheitskompetenz_MistrustIndex_Annotated.csv`**  
  Cleaned, weighted, and annotated dataset from a representative population-based survey in South Tyrol (Italy).  
  Includes:
  - Mistrust Index (4–16 scale)
  - Preventive health behaviors (Health Behavior Checklist items)
  - Sleep quality (B-PSQI)
  - Sociodemographics and chronic illness indicators
  - Population weights (`GEwicht`)

---

## 📊 Table Mapping

| **Table (Manuscript)** | **Script Filename**                              | **Description**                                                      |
|------------------------|--------------------------------------------------|----------------------------------------------------------------------|
| Table 1                | `table1_analysis.py`                              | Weighted and unweighted descriptives of the study sample             |
| Table 2                | `table2_weighted_sociodemographics_mistrust.py`  | Sociodemographic characteristics by mistrust group (weighted)        |
| Table 3                | `table3_preventive_behavior_mistrust.py`         | Preventive behaviors by mistrust group (weighted)                    |
| Table 4                | `table2_analysis.py`                              | Linear regression: mistrust → sleep quality                          |
| Table 5                | `table3_analysis.py`                              | Linear regression: behavior → sleep quality                          |
| Table 6                | `table6_mediation_model.py`                       | Mediation analysis: preventive behavior as mediator                  |

> 🛠️ **Note**: Earlier drafts (e.g. `README-2.md`, `README-5_mediation.md`, etc.) are outdated and can be deleted.

---

## ⚙️ How to Run

1. Clone this repository  
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Run a script, for example:

```bash
python table6_mediation_model.py
```

---

## 📄 License

This project is released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
