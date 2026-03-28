# Walkthrough: Dataset Generation

# Datasets

The following 5 raw datasets are generated:

raw_cems_data.csv        (27,135 rows)

sensor_master.csv        (10 rows)

maintenance_logs.csv     (30 rows)

manual_entries.csv       (50 rows)

regulatory_thresholds.csv (6 rows)


## Distribution Verification

Actual vs target percentages for [dev/raw_cems_data.csv](file:///s:/1.capg_case_Study/datasets/dev/raw_cems_data.csv):

| Column | Messy Type | Actual | Target |
|---|---|---|---|
| `TS` | Midnight `24:xx` (Rule 1) | 5.4% | 5% |
| `TS` | UTC suffix (Rule 17) | 5.2% | 5% |
| `Unit` | Unicode `µg/m³` (Rule 2) | 10.0% | 10% |
| `Unit` | `mg/Nm3` (Rule 14) | 10.1% | 10% |
| `Status` | Messy/untrimmed (Rules 3,12) | 28.6% | 30% |
| `PM2.5` | Negatives (Rule 5) | 4.7% | 5% |
| `PM2.5` | BDL strings (Rule 11) | 5.0% | 5% |
| `PM2.5` | Spikes (Rule 8) | 3.1% | 3% |
| `Lat_Lon` | Invalid (Rule 4) | 1.2% | 2% |

> [!NOTE]
> Row counts are slightly below 6K/28.8K because some records are intentionally missing to simulate real-world data gaps.

## Spot-Check Highlights

Verified in the raw CSV:
- `24:xx` timestamps like `28-02-2026 24:45` ✓
- UTC timestamps like `28-02-2026 19:30 UTC` ✓
- Swapped coordinates like `77.209,28.6139` ✓
- Impossible coords like `13.0833,-999.0` ✓
- Semicolons in coords like `13.0827;80.2707` ✓
- BDL strings: `BDL`, `<5.0`, `< 2.0` ✓
- Spikes: `9999.0`, `8500.0`, `7777.0`, `6500.0` ✓
- Messy statuses: `" ok "`, `offline`, `Error 404`, `DOWN  ` ✓
- Ambient sensors have NULL flow rates ✓
- Record IDs may have gaps (simulating missing data scenarios) ✓