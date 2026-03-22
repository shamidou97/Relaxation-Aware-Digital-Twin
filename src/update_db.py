import mysql.connector

try:
    # Connect through your tunnel
    conn = mysql.connector.connect(
        host='127.0.0.1', 
        port=3306, 
        user='battery_user', 
        password='battery_pass', 
        database='battery_digital_twin'
    )
    cursor = conn.cursor()

    # The SQL command to update your 'Memory'
    print("🔄 Updating SQL Schema...")
    cursor.execute("ALTER TABLE labeled_cycle_data ADD COLUMN label INT DEFAULT 0;")
    conn.commit()
    print("✅ Success: 'label' column added.")

except mysql.connector.Error as err:
    if err.errno == 1060:
        print("💡 Note: The 'label' column already exists. No changes needed.")
    else:
        print(f"❌ Error: {err.msg}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
