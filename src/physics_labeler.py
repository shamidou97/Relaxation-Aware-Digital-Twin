import mysql.connector

# --- CALIBRATED THRESHOLDS BASED ON YOUR SQL OUTPUT ---
S0_MAX = 2.95  # Anything below this is S0
S2_MIN = 3.15  # Anything above this is S2

try:
    conn = mysql.connector.connect(
        host='127.0.0.1', port=3306,
        user='battery_user', password='battery_pass', database='battery_digital_twin'
    )
    cursor = conn.cursor()

    print(f"🏷️  Labeling based on range [2.85 - 3.22]...")

    # 1. Clear old labels if any
    cursor.execute("UPDATE labeled_cycle_data SET label = 1") # Default to S1
    
    # 2. Update S0 (Fresh)
    cursor.execute(f"UPDATE labeled_cycle_data SET label = 0 WHERE entropy_h < {S0_MAX}")
    
    # 3. Update S2 (Aged)
    cursor.execute(f"UPDATE labeled_cycle_data SET label = 2 WHERE entropy_h >= {S2_MIN}")

    conn.commit()
    print(f"✅ Success! Labels applied to {cursor.rowcount} cycles.")

except mysql.connector.Error as err:
    print(f"❌ SQL Error: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close(); conn.close()
