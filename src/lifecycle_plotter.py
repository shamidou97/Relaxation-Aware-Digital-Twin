import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Increase font for the final "Thesis Masterpiece" plot
plt.rcParams.update({'font.size': 16, 'axes.titlesize': 20, 'axes.labelsize': 18})

def plot_battery_lifecycle():
    try:
        # 1. Connect to SQL
        conn = mysql.connector.connect(
            host='127.0.0.1', port=3306,
            user='battery_user', password='battery_pass', database='battery_digital_twin'
        )
        
        # 2. Fetch History (Assuming insertion order is chronological)
        # We use a subquery to generate a cycle index on the fly
        query = """
        SELECT 
            ROW_NUMBER() OVER () as cycle_index, 
            label 
        FROM labeled_cycle_data
        """
        
        # Note: Using SQLAlchemy engine is preferred by pandas, 
        # but the raw connection still works for this simple query.
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print("⚠️ Database is empty. Synchronize your .mat data first!")
            return

        # 3. Create the Timeline Plot
        plt.figure(figsize=(15, 7))
        
        # Plotting the state transitions as a step function
        plt.step(df['cycle_index'], df['label'], where='post', 
                 color='#34495e', linewidth=2.5, label='Digital Twin State')
        
        # 4. Highlight "Un-aging" / Recovery Points (State 1 -> State 0)
        # We find where current label is 0 but the previous was 1
        recovery = df[(df['label'] == 0) & (df['label'].shift(1) == 1)]
        
        if not recovery.empty:
            plt.scatter(recovery['cycle_index'], recovery['label'], 
                        color='#27ae60', s=150, zorder=5, label='Recovery (S1 → S0)')

        # Formatting for Thesis
        plt.yticks([0, 1, 2], ['S0 (Fresh/Rec)', 'S1 (Stable)', 'S2 (Aged)'])
        plt.xlabel('Cumulative Cycle Number')
        plt.ylabel('Markov Health State')
        plt.title('Non-Monotonic Battery Health: Detecting Recovery via Shannon Entropy')
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.legend(loc='upper left', frameon=True)
        
        plt.tight_layout()
        plt.savefig('Thesis_Lifecycle_Transitions.png', dpi=300)
        print("🚀 Plot saved as 'Thesis_Lifecycle_Transitions.png'.")
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    plot_battery_lifecycle()
