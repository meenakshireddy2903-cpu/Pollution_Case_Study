# Cleaned Dataset — Column Reference

A guide to every column in the cleaned output files, which rule created or modified it, and what it means.

---

## `raw_cems_data_cleaned.csv`

| # | Column | Type | Rule(s) | Description |
|---|--------|------|---------|-------------|
| 1 | `Record_ID` | string | R9 | Unique row ID (`E00001`–`E06000`). Ensured to be unique and continuous. |
| 2 | `Plant_ID` | string | R13 | Plant identifier (e.g. `PL-01`, `LOC-DEL-01`). Validated against `sensor_master`. |
| 3 | `Stack_ID` | string | R13 | Sensor/stack identifier (e.g. `S-01`, `A-01`). Validated with Plant_ID. |
| 4 | `Flow_Rate_m3_hr` | float | — | Gas flow rate (m³/hr). `NaN` for ambient sensors (no chimney). Untouched by cleaning. |
| 5 | `TS` | datetime | R1, R17 | Timestamp in `YYYY-MM-DD HH:MM:SS` format. Fixed invalid times (24:xx), standardized format, and removed UTC. |
| 6 | `PM2.5` | float | R5, R7, R8, R11, R14 | PM2.5 concentration (µg/m³). Negatives→NaN (R5), BDL→LOD/2 (R11), calibrated (R7), spikes capped (R8), units standardized (R14). |
| 7 | `SO2` | float | R5, R7, R8, R11, R14 | SO2 concentration (µg/m³). Same cleaning pipeline as PM2.5. |
| 8 | `NOx` | float | R5, R7, R8, R11, R14 | NOx concentration (µg/m³). Same cleaning pipeline as PM2.5. |
| 9 | `Unit` | string | R2, R14 | Measurement unit. All standardized to `ug/m3`. Unicode µg/m³ fixed (R2). |
| 10 | `Status` | string | R3, R10, R12 | Canonical status. Trimmed/uppercased (R3), normalized (R12), maintenance applied (R10). |
| 11 | `Lat` | float | R4 | Latitude extracted and validated (range -90 to 90). |
| 12 | `Lon` | float | R4 | Longitude extracted and validated (range -180 to 180). |
| 13 | `Source_Type` | string | R15 | **New column.** Tagged from `sensor_master`. **Values:** `Stack`, `Ambient`, `Unknown`. |
| 14 | `Exceedance_Flag` | string | R19 | **New column.** `EXCEEDANCE` if pollutant exceeds threshold, `OK` otherwise. |

---

## `manual_entries_cleaned.csv`

| # | Column | Type | Rule(s) | Description |
|---|--------|------|---------|-------------|
| 1 | `Log_ID` | string | — | Unique log entry ID (e.g. `L0001`). |
| 2 | `Plant_ID` | string | — | Plant where the manual entry was recorded. |
| 3 | `Lab_PM25_Entry1` | float | R16 | First technician's PM2.5 reading. |
| 4 | `Lab_PM25_Entry2` | float | R16 | Second technician's PM2.5 reading. |
| 5 | `Inspection_Notes` | string | R18 | Free-text notes. Emails and phone numbers removed. |
| 6 | `Diff_Pct` | float | R16 | **New column.** Percentage difference between Entry1 and Entry2. |
| 7 | `QC_Status` | string | R16 | **New column.** `QC_PASS` if diff ≤1%, `QC_FAIL` if diff >1%. |

---

## `cleaning_log.csv` (Audit Trail)

| Column | Description |
|--------|-------------|
| `Record_ID` | Which row was changed. |
| `Column` | Which column was changed. |
| `Old_Value` | Value before the change. |
| `New_Value` | Value after the change. |
| `Rule` | Which rule triggered this change (e.g. `R2`, `R5`, `R14`). |

> Audit log captures all transformations applied to the dataset.

---

## Status Values Explained

| Status | Meaning | How It Got There |
|--------|---------|-----------------|
| `OK` | Normal reading | Original data |
| `FAULT` | Sensor error/offline | R12 normalized invalid statuses |
| `MAINT` | Under maintenance | R10 applied maintenance windows |
| `UNKNOWN` | Missing/invalid status | R12 mapped null/invalid values |
