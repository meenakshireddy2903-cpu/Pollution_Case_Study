Let's officially decide on **10 Sensors** reporting every **15 minutes**. 
*(Math: 10 sensors × 4 times/hour × 24 hours × 30 days = **~28,800 rows per month**).* 

Here is the absolute, detailed, column-by-column breakdown of the **5 Cleaning Datasets**, including the exact percentages of how "messy" the raw data will be to trigger your rules!

---

### 1. `raw_cems_data.csv` (The Core Input Stream)
*   **Total Rows:** ~28,800 rows (Dynamic, grows continuously).
*   **What it is:** The raw, unfiltered 15-minute data stream from all 10 sensors.

**Columns & Expected Values:**
*   `Record_ID`: String (e.g., `E00001` to `E28800`). Unique for every row.
*   `Plant_ID`: String. (e.g., `PL-01`, `LOC-DEL-01`).
*   `Stack_ID`: String. (e.g., `S-01`, `A-01`).
*   `Flow_Rate_m3_hr`: Float. Normally `1000.0` to `5000.0` (Will be `NaN` for Ambient sensors).

*   **`TS` (Timestamp) - *The Messy Distribution:***
    *   **90% Perfect:** `14-03-2026 12:15`
    *   **5% Edge Case (Rule 1):** Ends in `24:10` or `24:15` (needs correction).
    *   **5% Edge Case (Rule 17):** Has timezone like `UTC` (needs removal/standardization).

*   **`PM2.5`, `SO2`, `NOx` - *The Messy Distribution:***
    *   **85% Perfect:** Normal Floats (`15.5` to `400.0`)
    *   **5% Edge Case (Rule 5):** Negative values (`-5.0`, `-12.4`)
    *   **5% Edge Case (Rule 11):** `"<2.0"` or `"BDL"`
    *   **3% Edge Case (Rule 8):** Spikes (`9999.0`, `8500.0`)
    *   **2% Missing:** Null values (filled later)

*   **`Unit` - *The Messy Distribution:***
    *   **80% Perfect:** `ug/m3`
    *   **10% Edge Case (Rule 2):** `µg/m³`
    *   **10% Edge Case (Rule 14):** `mg/Nm3`

*   **`Status` - *The Messy Distribution:***
    *   **70% Perfect:** `OK`, `FAULT`, `MAINT`
    *   **30% Edge Case (Rule 3 & 12):** `" ok "`, `"offline"`, `"down"`, `"Error 404"`

*   **`Lat_Lon` - *The Messy Distribution:***
    *   **98% Perfect:** `13.0827,80.2707`
    *   **2% Edge Case (Rule 4):** Invalid or malformed values (`13.08;80.27`, `-999`)

---

### 2. `sensor_master.csv` (Hardware Specs & Metadata)
*   **Total Rows:** **Exactly 10 Rows.**
*   **What it is:** Reference table for validation, calibration, and tagging (Rule 7, 11, 13, 15).

*(No changes — already matches your implementation)*

---

### 3. `maintenance_logs.csv` (Mechanic Logs)
*   **Total Rows:** ~30 Rows per month (Dynamic).
*   **What it is:** Used for **Rule 10**.

**Correction (important):**
👉 Your pipeline does NOT delete rows  
👉 It **sets pollutant values to NULL and status to `MAINT`**

---

### 4. `manual_entries.csv` (Lab & Inspections)
*   **Total Rows:** ~50 Rows per month (Dynamic).

**Correction:**
👉 Pipeline does NOT halt rows  
👉 It **flags QC_FAIL instead of stopping processing**

---

### 5. `regulatory_thresholds.csv` (Legal Limits)
*   **Total Rows:** **Exactly 6 Rows.**

*(No change — matches your implementation)*

---

### How to use this for your HTML Board

This gives you everything you need to build your visual map:

*   You have the **Volume/Scale** (`28,800 rows` vs `10 rows`)
*   You have the **Exact Column Names**
*   You have the **Data Quality Issues distribution**
*   You clearly show **why cleaning rules R1–R19 are required**