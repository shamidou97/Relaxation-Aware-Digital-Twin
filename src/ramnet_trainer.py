import torch
import torch.nn as nn
import torch.optim as optim
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

# ==========================================
# 📊 NEW: Global Font Configuration for Publication
# ==========================================
plt.rcParams.update({
    'font.size': 14,          # Base font size for all text
    'axes.titlesize': 18,      # Specific size for subplot titles
    'axes.labelsize': 16,      # Specific size for x and y labels
    'xtick.labelsize': 14,     # Specific size for x-axis ticks
    'ytick.labelsize': 14,     # Specific size for y-axis ticks
    'legend.fontsize': 14,     # Specific size for the legend
    'figure.titlesize': 20     # Specific size for the main figure title
})

# 1. RAMNet Architecture
class RAMNet(nn.Module):
    def __init__(self):
        super(RAMNet, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(2, 16), nn.ReLU(),
            nn.Linear(16, 32), nn.ReLU(),
            nn.Linear(32, 3)
        )
    def forward(self, x): return self.network(x)

def train_and_export_figures():
    # 2. Load and Split Data (Triple Split)
    conn = mysql.connector.connect(host='127.0.0.1', port=3306, user='battery_user', 
                                   password='battery_pass', database='battery_digital_twin')
    df = pd.read_sql("SELECT entropy_h, voltage_rebound, label FROM labeled_cycle_data", conn)
    conn.close()

    X, y = df[['entropy_h', 'voltage_rebound']].values, df['label'].values
    
    # 15% Test Set, 15% Val Set, 70% Train Set
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.176, random_state=42)

    # Scaling
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_val_s, X_test_s = scaler.transform(X_val), scaler.transform(X_test)

    # Tensors
    conv = lambda x: torch.FloatTensor(x)
    X_tr_t, X_va_t, X_te_t = conv(X_train_s), conv(X_val_s), conv(X_test_s)
    y_tr_t, y_va_t, y_te_t = torch.LongTensor(y_train), torch.LongTensor(y_val), torch.LongTensor(y_test)

    model = RAMNet()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)

    history = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}

    # 3. Training Loop
    print(f"🚀 Training on {len(X_train)} cycles...")
    for epoch in range(250):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_tr_t)
        loss = criterion(outputs, y_tr_t)
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            val_out = model(X_va_t)
            v_loss = criterion(val_out, y_va_t)
            train_acc = (outputs.argmax(1) == y_tr_t).float().mean().item()
            val_acc = (val_out.argmax(1) == y_va_t).float().mean().item()

        history['train_loss'].append(loss.item()); history['val_loss'].append(v_loss.item())
        history['train_acc'].append(train_acc); history['val_acc'].append(val_acc)

    # 4. Save Final Brain
    torch.save(model.state_dict(), 'best_ramnet_v5_5.pth')

    # ==========================================
    # 📊 NEW: Exporting Publication-Ready Plots
    # ==========================================
    
    # Plot 1: Learning Curves (High-Visibility)
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(history['train_loss'], label='Train Loss', linewidth=2)
    plt.plot(history['val_loss'], label='Val Loss', linewidth=2, linestyle='--')
    plt.title('Training vs Validation Loss')
    plt.xlabel('Epochs'); plt.ylabel('Loss'); plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.subplot(1, 2, 2)
    plt.plot(history['train_acc'], label='Train Acc', linewidth=2)
    plt.plot(history['val_acc'], label='Val Acc', linewidth=2, linestyle='--')
    plt.title('Training vs Validation Accuracy')
    plt.xlabel('Epochs'); plt.ylabel('Accuracy'); plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('Thesis_LearningCurves_HighVis.png', dpi=300)
    plt.show()

    # Plot 2: Test Set Confusion Matrix (High-Visibility)
    model.eval()
    with torch.no_grad():
        test_out = model(X_te_t)
        y_pred = test_out.argmax(1).numpy()
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    
    # annot_kws ensures the numbers INSIDE the matrix are also large
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['S0 (Recovered)', 'S1 (Stable)', 'S2 (Aged)'],
                yticklabels=['S0 (Recovered)', 'S1 (Stable)', 'S2 (Aged)'],
                cbar=False, annot_kws={"size": 18}) 
    
    plt.title('Final Unseen Test Set: Confusion Matrix')
    plt.xlabel('RAMNet Predicted State')
    plt.ylabel('Electrochemical Ground Truth')
    plt.tight_layout()
    plt.savefig('Thesis_ConfusionMatrix_HighVis.png', dpi=300)
    plt.show()

    print("✅ High-visibility figures saved as PNG.")

if __name__ == "__main__":
    train_and_export_figures()
