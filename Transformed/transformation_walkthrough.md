# Transformation Phase — Walkthrough

## What Was Done
Built and executed the full transformation pipeline (`notebooks/transformation.py` → `.ipynb`) applying transformation rules (T1–T20) to the cleaned CEMS data.

## Input Data
| File | Source |
|------|--------|
| `cleaned/raw_cems_data_cleaned.csv` | Cleaned CEMS data |
| `datasets/sensor_master.csv` | Sensor metadata |
| `datasets/regulatory_thresholds.csv` | Legal limits |
| `datasets/transformation/meteorology_data.csv` | Weather data |
| `datasets/transformation/aqi_standards_cpcb.csv` | AQI breakpoints |
| `datasets/transformation/emission_factors.csv` | Emission factors |
| `datasets/transformation/industry_control_measures.csv` | Control measures |
| `datasets/transformation/compliance_penalty_rules.csv` | Penalty rules |

## Rules Applied

| Rule | What It Does | Output |
|------|-------------|--------|
| **T1** | Per-pollutant exceedance flags | `Exceed_PM25`, `Exceed_SO2`, `Exceed_NOx`, `Any_Exceedance` |
| **T2** | AQI computation | `AQI_PM25`, `AQI_SO2`, `AQI_NOx`, `AQI_Overall`, `AQI_Category` |
| **T3** | Emission load calculation | `Load_PM25_kg_day`, `Load_SO2_kg_day`, `Load_NOx_kg_day` |
| **T4** | Rolling averages | `PM25_24h_avg`, `SO2_24h_avg`, `NOx_24h_avg` |
| **T5** | Source contribution score | `Wind_Contribution_Score` |
| **T6** | Compliance rate | `transformed/dev/compliance_report.csv` |
| **T7** | Episode detection | `transformed/dev/episodes.csv` |
| **T8** | Spatial interpolation | `transformed/dev/spatial_grid.csv` |
| **T9** | Health risk score | `Health_Risk_Score` |
| **T10** | Hourly profiles | `transformed/dev/hourly_profile.csv` |
| **T11** | Meteorology join | `Wind_Speed_kmh`, `Wind_Dir_deg`, `Temp_C`, `Humidity_RH` |
| **T12** | Emission factor comparison | `transformed/dev/emission_factor_comparison.csv` |
| **T13** | Drift detection | `transformed/dev/drift_alarms.csv` |
| **T14** | Data availability analysis | `transformed/dev/gap_analysis.csv` |
| **T15** | Regulatory reporting | `transformed/dev/regulatory_report_stack.csv`, `transformed/dev/regulatory_report_ambient.csv` |
| **T16** | ML features | `transformed/dev/model_features.csv` |
| **T17** | Hotspot ranking | `transformed/dev/hotspot_ranking.csv` |
| **T18** | Control impact | `transformed/dev/control_impact.csv` |
| **T19** | Penalty estimation | `transformed/dev/penalty_estimate.csv` |
| **T20** | Open data extract | `transformed/dev/open_data_extract.csv` |

## Output Files Summary (13 files in `transformed/dev/`)
- **Main dataset**: `transformed_cems.csv`
- **Derived tables**: compliance, episodes, spatial, drift, regulatory, ML, hotspot, control impact, penalty, emission factors, open data

## Testing
- Pipeline executed successfully
- All output files generated
- Verified outputs

## Key Files

- `notebooks/transformation.ipynb`
- `transformation_plan.md`