# Decarbonizing AI Data Centers in Weak-Grid Environments: Techno-Economic Sizing, 24/7 Carbon-Free Energy Matching, and Multi-Day Blackout Resiliency

**Author:** Jamiu Dahunsi  
**Affiliation:** Department of Electrical and Computer Engineering, Carnegie Mellon University (Pittsburgh, PA 15213, USA)  
**Contact:** `jdahunsi@andrew.cmu.edu`  
**Target Publication:** *Applied Energy* (Elsevier) / *IEEE Transactions on Sustainable Energy*

---

## Overview

This repository contains the simulation data, load profiles, optimization scripts, and technical documentation for the techno-economic optimization and resiliency analysis of a **20 MW AI Data Center microgrid located in Lagos, Nigeria**.

The study models the intersection between high-density artificial intelligence compute workloads and vulnerable electrical grid infrastructure in sub-Saharan Africa. The facility is sited in the coastal subsea fiber-optic corridor (landing zone for Google's Equiano and Meta's 2Africa cables), where the national grid experiences 12 to 24 collapses annually.

---

## Key Optimization Findings (Summary Table)

All scenarios were solved using Mixed-Integer Linear Programming (MILP) on the Xendee Microgrid Optimization Platform:

| Metric | Baseline (Captive Fossil) | S1: Economic Least-Cost | S2: 80% Hourly CFE | S3: 95% Hourly CFE | S4: 72h Blackout Survival |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Solar PV Capacity (kW)** | 0 | 41,444 | 95,865 | 113,845 | 97,256 |
| **BESS Storage Capacity (kWh)** | 0 | 0 | 183,645 | 253,105 | 180,910 |
| **Diesel Generator Capacity (kW)** | 20,000 | 17,500 | 0 (New) | 0 (New) | 5,000 |
| **Initial Equipment CapEx ($M)** | $0.00 | $47.96 | $142.85 | $179.97 | $146.08 |
| **Annual Operating Expenses ($M/yr)** | $21.37 | $14.68 | $6.43 | $3.83 | $6.57 |
| **Annual OpEx Savings (%)** | 0.00% | 31.33% | 69.92% | 82.09% | 69.25% |
| **Annual Carbon Emissions (t CO2/yr)**| 73,451 | 45,544 | 17,089 | 7,475 | 17,180 |
| **Carbon Abatement vs Base (%)** | 0.00% | 37.99% | 76.73% | 89.82% | 76.61% |
| **Levelized Cost of Energy ($/kWh)** | $0.1500 | $0.1412 | $0.1693 | $0.1860 | $0.1734 |
| **Simple Payback Period (Years)** | N/A | 7.9 (8.0) | 12.6 (13.0) | 14.3 (14.0) | 13.2 (13.0) |
| **Outage Ride-Through Capability** | Fails | 24 Hours | 24 Hours | 24 Hours | 72 Hours |
| **Loss of Load Probability (LOLP)** | >5.0% | 0.000% | 0.000% | 0.000% | 0.000% |

---

## Repository Structure

```text
├── AI_DataCenter_20MW_8760_Hourly_Load.csv    # Synthesized 8,760-hour facility load curve (141.87 GWh)
├── Clean_Working_Paper_Draft.pdf              # Full 32-page compiled research working paper
├── Figures/                                   # High-resolution 300 DPI publication figures
│   ├── Figure_1_AI_DataCenter_Load_Profile.png
│   ├── Figure_2_Decarbonization_Pareto_Frontier.png
│   ├── Figure_3_Asset_Capacity_Sizing.png
│   └── Figure_4_Cumulative_Cash_Flow_Payback.png
├── Overleaf_Package/                          # Complete LaTeX source files and BibTeX bibliography
│   ├── main.tex
│   └── references.bib
├── Scenario_S1_Results_Data/                  # Raw Xendee solver CSV files for Scenario S1
├── Scenario_S2_Results_Data/                  # Raw Xendee solver CSV files for Scenario S2
├── Scenario_S3_Results_Data/                  # Raw Xendee solver CSV files for Scenario S3
├── Scenario_S4_Results_Data/                  # Raw Xendee solver CSV files for Scenario S4
├── INDEPENDENT_DATA_AUDIT_REPORT.md           # Line-by-line data forensic audit verification
└── README.md                                  # Repository documentation
```

---

## Methodology Highlights

1. **AI Workload Synthesis:** Combines empirical GPU server traces from Google Borg and Microsoft Azure clusters with an ambient-temperature-dependent Power Usage Effectiveness (PUE) model calibrated to ASHRAE TC 9.9 tropical environmental guidelines.
2. **Weak-Grid Intermittency Modeling:** Accounts for post-subsidy commercial diesel fuel costs ($1.30/L), NERC Band A industrial tariffs ($0.150/kWh), and zero reverse-grid power injection constraints ($P_{\text{grid,inj}} = 0$).
3. **Resilience Optimization:** Formulates a 72-hour continuous grid collapse with zero unserved energy ($\text{LOLP}=0.000\%$), proving that solar-plus-storage can replace over 70% of conventional captive fossil generation infrastructure.

---

## Citation & License

This research is conducted under the Department of Electrical and Computer Engineering at Carnegie Mellon University.

If referencing this data or methodology, please cite:
> J. Dahunsi, "Decarbonizing AI Data Centers in Weak-Grid Environments: Techno-Economic Sizing, 24/7 Carbon-Free Energy Matching, and Multi-Day Blackout Resiliency," Working Paper Draft, Carnegie Mellon University, 2026.
