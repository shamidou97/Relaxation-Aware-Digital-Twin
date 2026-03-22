import scipy.io
import numpy as np
import mysql.connector
from scipy.stats import entropy

# --- THE PHYSICS ENGINE ---
def calculate_shannon_entropy(voltage_signal, bins=100):
    # Converts raw voltage into a probability distribution
    # Crucial for detecting "Reverse Polarization" complexity
    hist, _ = np.histogram(voltage_signal, bins=bins, density=True)
    hist = hist[hist > 0] 
    return entropy(hist)

def run_bridge(file_path):
    print(f"🚀 Bridging Physical Data: {file_path}")
    try:
        # 1. Load the structured .mat file
        mat = scipy.io.loadmat(file_path)
        
        # Based on your Inspector: 'data' contains the time-series signals
        raw_data = mat['data'][0, 0]
        
        # 2. Extract Voltage and Calculate Delta V
        # voltage_V is the internal field we identified
        v_signal = raw_data['voltage_V'].flatten()
        delta_v = np.max(v_signal) - np.min(v_signal)
        
        # 3. Calculate Shannon Entropy (H)
        h_val = calculate_shannon_entropy(v_signal)

        # 4. Connect to Digital Twin Memory (SQL)
        conn = mysql.connector.connect(
            host='127.0.0.1', port=3306,
            user='battery_user', password='battery_pass', database='battery_digital_twin'
        )
        cursor = conn.cursor()

        # 5. Insert the "Information Physics" into the Twin
        query = "INSERT INTO labeled_cycle_data (entropy_h, voltage_rebound, label) VALUES (%s, %s, %s)"
        cursor.execute(query, (float(h_val), float(delta_v), 1)) # Default to S1 (Stable)
        
        conn.commit()
        print(f"✅ SUCCESS: H={h_val:.5f} | ΔV={delta_v:.5f} | Saved to SQL.")

    except Exception as e:
        print(f"❌ Error during bridge: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close(); conn.close()

if __name__ == "__main__":
    run_bridge()
