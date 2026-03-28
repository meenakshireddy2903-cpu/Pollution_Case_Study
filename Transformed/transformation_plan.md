# Transformation Plan — All 20 Rules

## Overview

Transform cleaned CEMS data into analysis-ready outputs. Each rule produces a new column, derived table, or analytical output.

**Input:** Cleaned datasets from Phase 2 + reference datasets.

---

## New Datasets to Generate (All Clean — No Messiness)

### Node 6: `meteorology_data.csv`
Hourly weather data.

*(No change — matches your implementation)*

### Node 7: `aqi_standards_cpcb.csv`
AQI breakpoint table.

*(No change)*

### Node 8: `emission_factors.csv`
Emission factors by sector.

*(No change)*

### Node 9: `industry_control_measures.csv`
Control equipment installation logs.

*(No change)*

### Node 10: `compliance_penalty_rules.csv`
Penalty rules.

*(No change)*

---

## Transformation Rules — Execution Order



---



#### T1: Exceedance flags
- **Input:** Cleaned data + thresholds  
- **Output:** `Exceed_PM25`, `Exceed_SO2`, `Exceed_NOx`, `Any_Exceedance`  
- **Logic:** Direct comparison of pollutant values with thresholds (no resampling)

---

#### T4: Rolling 24-hour averages
- **Output:** `PM25_24h_avg`, `SO2_24h_avg`, `NOx_24h_avg`  
- **Logic:** Rolling window (based on 15-min data)

---

#### T10: Diurnal profiles
- **Output:** `Hour`, `DayOfWeek`, `hourly_profile.csv`  
- **Logic:** Group by hour

---



#### T2: AQI computation
- **Output:** `AQI_PM25`, `AQI_SO2`, `AQI_NOx`, `AQI_Overall`, `AQI_Category`

---

#### T9: Health risk index
- **Output:** `Health_Risk_Score`, `Date`

---



#### T3: Emission load
- **Output:** `Load_PM25_kg_day`, `Load_SO2_kg_day`, `Load_NOx_kg_day`

---

#### T12: Emission factor comparison
- Output table only (no column added to main dataset)

---



#### T11: Meteorology join
- **Output:** `Wind_Speed_kmh`, `Wind_Dir_deg`, `Temp_C`, `Humidity_RH`

---

#### T5: Source contribution
- **Output:** `Wind_Contribution_Score`

---



#### T6: Compliance rate
- Output: `compliance_report.csv`, `compliance_report_monthly.csv`

---

#### T15: Regulatory reports
- Output: reporting tables

---

#### T19: Penalty estimation
- Output: `penalty_estimate.csv`

---



#### T7: Episode detection
- Output: `episodes.csv`

---

#### T13: Drift detection
- Output: `drift_alarms.csv`

---



#### T8: Spatial grid
- Output: `spatial_grid.csv`

---

#### T17: Hotspot ranking
- Output: `hotspot_ranking.csv`

---



#### T16: Model features
- Output: `model_features.csv`

---



#### T18: Control impact
- Output: `control_impact.csv`

---

#### T14: Gap analysis
- Output: summary metrics (no GAP_FILLED dependency)

---

#### T20: Open data extract
- Output: `open_data_extract.csv`
- Remove internal identifiers

---

## Output Files Summary

| Output File | Rules | Description |
|-------------|-------|-------------|
| `transformed_cems.csv` | T1–T5, T9–T11 | Main dataset |
| `hourly_profile.csv` | T10 | Hourly averages |
| `compliance_report.csv` | T6 | Compliance |
| `penalty_estimate.csv` | T19 | Penalties |
| `episodes.csv` | T7 | Events |
| `drift_alarms.csv` | T13 | Drift |
| `spatial_grid.csv` | T8 | Map |
| `hotspot_ranking.csv` | T17 | Ranking |
| `model_features.csv` | T16 | ML |
| `control_impact.csv` | T18 | Impact |
| `open_data_extract.csv` | T20 | Public data |