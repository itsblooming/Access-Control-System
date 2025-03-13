import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.cluster import DBSCAN

def analyze_user_behavior(data):
    print("Raw data:", data)  

    if not isinstance(data, (list, np.ndarray)) or len(data) == 0:
        print("Error: Data should be a non-empty list or array of tuples/lists.")
        return

    data = np.array(data, dtype=np.float64)  

    print("Data shape:", data.shape) 

    # Данные должны быть 2D (количество объектов, количество признаков)
    if data.ndim != 2 or data.shape[1] < 2:
        print("Error: Data should have at least 2 features.")
        return

    X = data[:, :2]
    
    # Isolation Forest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    iso_labels = iso_forest.fit_predict(X)
    
    # One-Class SVM
    oc_svm = OneClassSVM(nu=0.1, kernel="rbf", gamma="auto")
    svm_labels = oc_svm.fit_predict(X)
    
    # DBSCAN (подбираем параметры)
    dbscan = DBSCAN(eps=5000, min_samples=3)
    dbscan_labels = dbscan.fit_predict(X)
    
    # Подсчёт аномалий
    iso_anomalies = np.sum(iso_labels == -1)
    svm_anomalies = np.sum(svm_labels == -1)
    dbscan_anomalies = np.sum(dbscan_labels == -1)
    
    print(f"Isolation Forest Anomalies: {iso_anomalies}/{len(X)}")
    print(f"One-Class SVM Anomalies: {svm_anomalies}/{len(X)}")
    print(f"DBSCAN Anomalies: {dbscan_anomalies}/{len(X)}")
    
    # Визуализация
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.scatter(X[:, 0], X[:, 1], c='blue', label='Normal Data')
    ax.scatter(X[iso_labels == -1, 0], X[iso_labels == -1, 1], c='red', label='IsoForest Anomalies', marker='x')
    ax.scatter(X[svm_labels == -1, 0], X[svm_labels == -1, 1], c='purple', label='SVM Anomalies', marker='D')
    ax.scatter(X[dbscan_labels == -1, 0], X[dbscan_labels == -1, 1], c='black', label='DBSCAN Outliers', marker='s')
    
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.legend()
    ax.set_title("Anomaly Detection in User Behavior")
    
    plt.show()
    
    if iso_anomalies > 0 or svm_anomalies > 0 or dbscan_anomalies > 0:
        print("⚠️ Warning: Potential anomaly detected!")
    else:
        print("✅ No anomalies detected.")
