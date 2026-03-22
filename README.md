# 🔋 Relaxation-Aware Digital Twin (RA-DT) 🧠
## Non-Monotonic Battery Health Forecasting via Shannon Entropy & Markov Networks

---
## 📜 Technical Abstract
Traditional State-of-Health (SoH) models assume degradation is strictly linear. However, electrochemical cells exhibit **Reverse Polarization** during rest, leading to "un-aging" events. This project introduces **RA-DT**, a cyber-physical framework using Shannon Entropy ($H$) to quantify these non-linear transitions. Using a **7,193-cycle dataset**, our **RAMNet** inference engine (675 parameters) maps information-theoretic features to three Markovian states: **$S_0$ (Recovered), $S_1$ (Stable)**, and **$S_2$ (Aged)**.

**Key Finding**: The model achieves **99.81% accuracy**, identifying a **5.34% recovery frequency** where cells returned to a higher-stability equilibrium. This proves that entropy-based signatures are superior to raw capacity metrics for detecting subtle electrochemical restoration.

---
## 📊 Technical Specifications (v5.8)

![RA-DT Technical Spec Sheet](results/technical_spec_sheet.png)

> **Note:** The RAMNet engine is optimized for Edge BMS deployment with only 675 trainable parameters.
---
## 🔬 The Physics: "Un-aging" via Reverse Polarization

Traditional Battery Management Systems (BMS) assume degradation is strictly linear and monotonic. However, electrochemical cells exhibit **Reverse Polarization** during rest periods, leading to a measurable recovery in internal stability. 

By calculating the Shannon Entropy ($H$) of voltage relaxation curves, we quantify the transition from "Turbulent/Aged" states back to "Equilibrium/Fresh" states, allowing the **RAMNet** (Relaxation-Aware Markov Network) to map health state transitions accurately.

---

## 🚀 Key Results

- **🎯 99.81% Accuracy**: RAMNet v5.8 achieves near-perfect state classification on unseen test data.  
- **📈 5.34% Recovery Frequency**: Identified 384 recovery events across a 7,193-cycle lifecycle.  
- **💎 100+ Major "Un-aging" Events**: Statistically verified instances where the battery returned from $S_1$ to a "Fresh" ($S_0$) state.  
- **📊 High-Fidelity Tracking**: Successfully mapped the 2.85–3.92 Shannon Entropy range to physical health states.

---

## 🚀 Quick Start: Initializing the Twin
Follow these steps to recreate the Digital Twin environment and verify the 99.81% accuracy results.

### 1. Environment Setup
```bash
# Clone the repository
git clone [https://github.com/shamidou97/Relaxation-Aware-Digital-Twin.git](https://github.com/shamidou97/Relaxation-Aware-Digital-Twin.git)
cd Relaxation-Aware-Digital-Twin

# Install verified dependencies
pip install -r requirements.txt

```

### 2. Database & Data Seeding
Initialize the "Virtual Memory" by loading the 7,193-cycle training history:

# This creates the database and populates the features (H, Delta V)

```bash
mysql -u [your_user] -p < data/populate_battery_data.sql
```

### 3. Run the RAMNet Engine
```bash
python src/ramnet_trainer.py
```

## 📊 Model Performance Metrics (Test Set $n=1,080$)

| Class | Precision | Recall (Sensitivity) | F1-Score | Physical State      |
|-------|-----------|---------------------|----------|---------------------|
| S₀    | 1.00      | 1.00                | 1.00     | Recovered/Fresh     |
| S₁    | 1.00      | 0.99                | 1.00     | Stable Operation    |
| S₂    | 0.98      | 1.00                | 0.99     | Aged/High Entropy   |

Model Complexity: 675 Trainable Parameters (Optimized for Edge BMS deployment)

## 🏗️ System Architecture
The RA-DT follows a rigorous Cyber-Physical pipeline:

 1. **Extraction**: .mat files $\to$ voltage_V time-series extraction
 2. **Information Physics**: Calculation of Shannon Entropy ($H$) and Voltage Rebound ($\Delta V$).
 3. **Virtual Memory**: Storage of features in a relational MySQL schema.
 4. **Inference**: Deep Learning (PyTorch) mapping of features to Markov States ($S_0, S_1, S_2$).


## 📂 Repository Structure

```text
.
├── data/
│   ├── schema.sql                 # MySQL Database Blueprint (Table Structures)
│   └── populate_battery_data.sql  # The 7,193-cycle training history (Seed data)
├── src/
│   ├── bridge_mat_to_sql.py       # Ingestion & Physics Feature Extraction
│   ├── physics_labeler.py         # State Calibration (Entropy Thresholding)
│   ├── ramnet_trainer.py          # PyTorch Model Training & Evaluation
│   ├── lifecycle_plotter.py       # 7,193-cycle Timeline Visualization
│   └── quantify_gain.py           # Statistical Recovery Frequency Analysis
├── models/
│   └── best_ramnet_v5_8.pth       # Pre-trained Digital Twin Weights
├── results/                       # High-Res Thesis Figures (Loss, CM, Timeline)
└── requirements.txt               # Environment Dependencies

## 🎓 Conclusion & Future Work


This research proves that Shannon Entropy is a robust proxy for battery health recovery. By identifying the 5.34% recovery frequency, we demonstrate that intelligent "Rest Charging" protocols can extend the cycle life of lithium-ion batteries.

Next Steps: Integrating this RAMNet Digital Twin into an ESP32/Arduino environment for real-time hardware-in-the-loop (HIL) testing.


## 🤝 Contact

**Sy Hamidou**
MS in Physics|MS In Electrical Engineering
  * https://www.linkedin.com/in/hamidou-sy-ba699411/