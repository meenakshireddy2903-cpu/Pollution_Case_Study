import numpy as np
import pandas as pd
import re

# load cleaned data
# load cleaned data
df = pd.read_csv('cleaned/cleaned_data.csv')
manual = pd.read_csv('cleaned/manual_cleaned.csv')
sensors = pd.read_csv('cleaned/sensor_master_cleaned.csv')
threshold = pd.read_csv("cleaned/thresholds_cleaned.csv")
maint = pd.read_csv("cleaned/maintenance_cleaned.csv")
audit_df = pd.read_csv("cleaned/cleaning_log.csv")
# ─────────────────────────────
# R1: Timestamp
# ─────────────────────────────
def test_r1_timestamp():
    count = df['TS'].astype(str).str.contains('24:').sum()
    assert count == 0
    print("✅ R1: No 24:xx timestamps —", count)


    
# ─────────────────────────────
# R2: Unit cleaned
# ─────────────────────────────
def test_r2_unit():
    count = df['Unit'].astype(str).str.contains('µ').sum()
    assert count == 0
    print("✅ R2: No unicode units —", count)


# ─────────────────────────────
# R3: Status cleaned
# ─────────────────────────────
def test_r3_status():
    for val in df['Status']:
        if isinstance(val, str):
            assert val == val.strip()
            assert val == val.upper()
    print("✅ R3: Status formatted correctly")


# ─────────────────────────────
# R4: Coordinates
# ─────────────────────────────
def test_r4_coordinates():
    invalid = 0
    
    for i in df.index:
        lat = df.at[i, 'Lat']
        lon = df.at[i, 'Lon']

        if pd.isna(lat) or pd.isna(lon):
            continue

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            invalid += 1

    assert invalid == 0
    print("✅ R4: Coordinates valid —", invalid)


# ─────────────────────────────
# R5: No negatives
# ─────────────────────────────
def test_r5_no_negative():
    for col in ['PM2.5', 'SO2', 'NOx']:
        count = (df[col] < 0).sum()
        assert count == 0
        print(f"✅ R5: No negatives in {col} —", count)


# ─────────────────────────────
# R6: No duplicates
# ─────────────────────────────
def test_r6_duplicates():
    dups = df.duplicated(['Plant_ID','Stack_ID','TS']).sum()
    assert dups == 0
    print("✅ R6: No duplicates —", dups)


# ─────────────────────────────
# R7: Calibration exists
# ─────────────────────────────
def test_r7_calibration():
    count = (audit_df['Rule'] == 'R7').sum()
    assert count > 0
    print("✅ R7: Calibration exists —", count)


# ─────────────────────────────
# R8: No spikes
# ─────────────────────────────
def test_r8_spikes():
    for col in ['PM2.5', 'SO2', 'NOx']:
        count = (df[col] > 5000).sum()
        assert count == 0
        print(f"✅ R8: No spikes in {col} —", count)


# ─────────────────────────────
# R9: Record_ID continuous
# ─────────────────────────────
def test_r9_record_id():
    
    # check no duplicates
    duplicates = df['Record_ID'].duplicated().sum()
    assert duplicates == 0

    # check format
    for val in df['Record_ID']:
        assert str(val).startswith('E')

    print("✅ R9: Record_ID unique and valid")


# ─────────────────────────────
# R10: Maintenance
# ─────────────────────────────
def test_r10_maintenance():
    maint_mask = df['Status'] == 'MAINT'
    #print(df.loc[maint_mask, ['PM2.5', 'SO2', 'NOx']].head(10))
    for col in ['PM2.5', 'SO2', 'NOx']:
        assert df.loc[maint_mask, col].isna().all()

    print("✅ R10: Maintenance rows cleaned")


# ─────────────────────────────
# R11: No BDL
# ─────────────────────────────
def test_r11_no_bdl():
    for col in ['PM2.5', 'SO2', 'NOx']:
        count = 0
        for val in df[col]:
            s = str(val).strip().upper()
            if s == 'BDL' or s.startswith('<'):
                count += 1
        
        assert count == 0
        print(f"✅ R11: No BDL in {col} —", count)


# ─────────────────────────────
# R12: Status valid
# ─────────────────────────────
def test_r12_status():
    valid = ['OK', 'FAULT', 'MAINT', 'DOWN', 'OFFLINE', 'UNKNOWN', 'ERROR', 'GAP_FILLED']
    assert df['Status'].isin(valid).all()
    print("✅ R12: Status values valid")


# ─────────────────────────────
# R13: Mapping
# ─────────────────────────────
def test_r13_mapping():
    df_valid = df.dropna(subset=['Plant_ID','Stack_ID'])

    merged = df_valid.merge(
        sensors[['Plant_ID','Stack_ID']],
        on=['Plant_ID','Stack_ID'],
        how='left',
        indicator=True
    )

    invalid = (merged['_merge'] == 'left_only').sum()

    assert invalid == 0
    print("✅ R13: Mapping valid —", invalid)


# ─────────────────────────────
# R14: Unit check
# ─────────────────────────────
def test_r14_unit():
    assert (df['Unit'] == 'ug/m3').all()
    print("✅ R14: Units correct")


# ─────────────────────────────
# R15: Source_Type
# ─────────────────────────────
def test_r15_source_type():
    valid = ['Stack','Ambient','Unknown']
    assert df['Source_Type'].isin(valid).all()
    print("✅ R15: Source_Type valid")


# ─────────────────────────────
# R16: QC
# ─────────────────────────────
def test_r16_qc():
    for i in manual.index:
        diff = manual.at[i, 'Diff_Pct']
        status = manual.at[i, 'QC_Status']

        if diff > 1:
            assert status == 'QC_FAIL'
        else:
            assert status == 'QC_PASS'

    print("✅ R16: QC correct")


# ─────────────────────────────
# R17: UTC removed
# ─────────────────────────────
def test_r17_utc():
    count = df['TS'].astype(str).str.contains('UTC').sum()
    assert count == 0
    print("✅ R17: No UTC timestamps")


# ─────────────────────────────
# R18: PII removed
# ─────────────────────────────
def test_r18_pii():
    for note in manual['Inspection_Notes']:
        s = str(note)
        assert not re.search(r'\d{10}', s)
        assert not re.search(r'\S+@\S+', s)

    print("✅ R18: No PII")


# ─────────────────────────────
# R19: Exceedance
# ─────────────────────────────
def test_r19_exceedance():
    valid = ['OK','EXCEEDANCE']
    assert df['Exceedance_Flag'].isin(valid).all()
    print("✅ R19: Exceedance valid")



# ─────────────────────────────
# R20: Audit Trail
# ─────────────────────────────
def test_r20_audit_trail():

    # 1. audit file should not be empty
    assert len(audit_df) > 0

    # 2. required columns must exist
    required_cols = ['Rule']
    for col in required_cols:
        assert col in audit_df.columns

    # 3. at least some rules should be present
    expected_rules = ['R2', 'R3', 'R5', 'R6', 'R8', 'R10', 'R11']
    found = audit_df['Rule'].isin(expected_rules).sum()
    assert found > 0

    # 4. row-level logs should exist (with Record_ID)
    if 'Record_ID' in audit_df.columns:
        assert audit_df['Record_ID'].notna().sum() > 0

    print("✅ R20: Audit trail exists and valid —", len(audit_df))
# ─────────────────────────────
# RUN ALL TESTS
# ─────────────────────────────
def run_all_tests():
    test_r1_timestamp()
    test_r17_utc()
    test_r2_unit()
    test_r3_status()
    test_r4_coordinates()
    test_r5_no_negative()
    test_r6_duplicates()
    test_r7_calibration()
    test_r8_spikes()
    test_r9_record_id()
    test_r10_maintenance()
    test_r11_no_bdl()
    test_r12_status()
    test_r13_mapping()
    test_r14_unit()
    test_r15_source_type()
    test_r16_qc()
    #test_r17_utc()
    test_r18_pii()
    test_r19_exceedance()
    test_r20_audit_trail()

if __name__ == "__main__":
    run_all_tests()