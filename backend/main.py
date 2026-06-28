# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
import os
import urllib.request
import json
from typing import List, Dict, Any, Optional

# Machine learning libraries
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_moons, make_blobs
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

app = FastAPI(title="ML Algorithms Simulation API")

# Enable CORS for the Next.js frontend (running on port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Database of algorithms metadata
ALGORITHMS = {
    "linear_regression": {
        "id": "linear_regression",
        "name": "線性回歸 (Linear Regression)",
        "type": "regression",
        "equation": "y = XW + b",
        "description": "建立自變量與應變量之間的線性映射關係，採用最小二乘法 (OLS) 求解最佳適應線。",
        "pros": ["簡單易懂，計算速度極快", "模型參數具備極佳的物理與統計學可解釋性"],
        "cons": ["無法擬合非線性關係（除非進行特徵多項式轉換）", "對異常值（Outliers）極為敏感"],
        "params": [
            {"name": "degree", "label": "多項式階數", "type": "int", "min": 1, "max": 4, "default": 2},
            {"name": "noise", "label": "雜訊強度", "type": "float", "min": 0.1, "max": 2.0, "default": 0.5}
        ]
    },
    "logistic_regression": {
        "id": "logistic_regression",
        "name": "邏輯回歸 (Logistic Regression)",
        "type": "classification",
        "equation": "p = 1 / (1 + e^{-z})",
        "description": "使用 Sigmoid 函數將線性預測映射至 (0, 1) 區間，預測二元分類的後驗機率。",
        "pros": ["預測速度快，輸出具備機率物理意義", "易於透過 L1/L2 正則化防止過擬合"],
        "cons": ["本質上是線性分類器，無法直接處理複雜的非線性分界"],
        "params": [
            {"name": "C", "label": "正則化強度倒數(C)", "type": "float", "min": 0.01, "max": 10.0, "default": 1.0},
            {"name": "penalty", "label": "懲罰項類型", "type": "str", "options": ["l2", "none"], "default": "l2"}
        ]
    },
    "decision_tree": {
        "id": "decision_tree",
        "name": "決策樹 (Decision Tree)",
        "type": "classification",
        "equation": "Gini = 1 - \\sum p_k^2",
        "description": "透過基尼不純度或資訊增益遞迴劃分特徵空間，建構樹狀判定規則。",
        "pros": ["直觀且易於視覺化，不需要特徵縮放", "能自動處理非線性特徵交互"],
        "cons": ["極易過擬合，對資料的微小變動非常敏感（高方差）"],
        "params": [
            {"name": "max_depth", "label": "最大樹深度", "type": "int", "min": 1, "max": 10, "default": 4},
            {"name": "min_samples_split", "label": "最小分裂樣本數", "type": "int", "min": 2, "max": 20, "default": 2}
        ]
    },
    "random_forest": {
        "id": "random_forest",
        "name": "隨機森林 (Random Forest)",
        "type": "classification",
        "equation": "H(x) = mode(h_t(x))",
        "description": "結合 Bagging 自助抽樣與隨機特徵選擇，集成多棵決策樹進行投票，有效降低方差。",
        "pros": ["極強的抗過擬合能力，泛化效能優異", "內建特徵重要性評估功能"],
        "cons": ["模型體積大，預測速度較慢", "失去單一決策樹的直觀可解釋性"],
        "params": [
            {"name": "n_estimators", "label": "決策樹數量", "type": "int", "min": 10, "max": 200, "default": 50},
            {"name": "max_depth", "label": "最大樹深度", "type": "int", "min": 2, "max": 12, "default": 6}
        ]
    },
    "svm": {
        "id": "svm",
        "name": "支援向量機 (Support Vector Machine, SVM)",
        "type": "classification",
        "equation": "K(x_i, x_j) = e^{-\\gamma ||x_i - x_j||^2}",
        "description": "最大化分類間隔超平面，並透過核函數將低維非線性數據投影到高維空間以實現線性分類。",
        "pros": ["在中小樣本、高維度特徵上表現極為出色", "僅依賴少數支援向量，泛化界限穩健"],
        "cons": ["對大規模數據集計算代價大", "對噪聲數據敏感，參數調整較敏感"],
        "params": [
            {"name": "C", "label": "懲罰係數(C)", "type": "float", "min": 0.1, "max": 20.0, "default": 1.0},
            {"name": "gamma", "label": "RBF核半徑(gamma)", "type": "float", "min": 0.01, "max": 5.0, "default": 0.5},
            {"name": "kernel", "label": "核函數類型", "type": "str", "options": ["rbf", "linear", "poly"], "default": "rbf"}
        ]
    },
    "knn": {
        "id": "knn",
        "name": "K-最近鄰 (K-Nearest Neighbors, KNN)",
        "type": "classification",
        "equation": "d(x, y) = \\sqrt{\\sum (x_i - y_i)^2}",
        "description": "基於距離度量，尋找空間中最近的 K 個鄰居進行多數投票分類。",
        "pros": ["簡單直觀，完全不需要顯式的訓練階段（懶學習）", "能自然適應複雜多變的非線性邊界"],
        "cons": ["預測速度隨訓練集規模增大而急劇變慢", "對特徵量綱敏感，受維度災難影響"],
        "params": [
            {"name": "n_neighbors", "label": "最近鄰居數(K)", "type": "int", "min": 1, "max": 20, "default": 5},
            {"name": "weights", "label": "距離權重方式", "type": "str", "options": ["uniform", "distance"], "default": "uniform"}
        ]
    },
    "naive_bayes": {
        "id": "naive_bayes",
        "name": "朴素貝葉斯 (Naive Bayes)",
        "type": "classification",
        "equation": "P(C_k|x) \\propto P(C_k) \\prod P(x_i|C_k)",
        "description": "基於貝葉斯定理與特徵條件獨立性假設，快速計算各個類別的後驗概率。",
        "pros": ["訓練與預測速度極快，佔用記憶體小", "在文本分類與小樣本場景下表現出色"],
        "cons": ["特徵條件獨立的假設在實務中很難完全成立"],
        "params": [
            {"name": "var_smoothing", "label": "方差平滑係數(1e-x)", "type": "int", "min": 1, "max": 12, "default": 9}
        ]
    },
    "kmeans": {
        "id": "kmeans",
        "name": "K-Means 聚類 (K-Means Clustering)",
        "type": "clustering",
        "equation": "J = \\sum ||x_i - \\mu_j||^2",
        "description": "無監督聚類演算法，透過交替分配最近質心與更新質心位置，劃分數據為 K 個簇。",
        "pros": ["演算法結構簡單，收斂速度快", "易於在大規模數據集上擴展"],
        "cons": ["必須預先指定 K 值", "對初始質心位置敏感，易陷入局部最優"],
        "params": [
            {"name": "n_clusters", "label": "聚類簇數(K)", "type": "int", "min": 2, "max": 8, "default": 4},
            {"name": "init_type", "label": "初始化方式", "type": "str", "options": ["k-means++", "random"], "default": "k-means++"}
        ]
    },
    "pca": {
        "id": "pca",
        "name": "主成分分析 (PCA)",
        "type": "decomposition",
        "equation": "X' = XW",
        "description": "無監督線性降維技術，透過投影矩陣將特徵投影至最大方差的正交子空間上。",
        "pros": ["去除共線性與特徵冗餘，實現資料壓縮", "便於高維數據的二維或三維視覺化"],
        "cons": ["降維後的新主成分失去原始特徵的直觀物理意義"],
        "params": [
            {"name": "n_components", "label": "降維後維度", "type": "int", "min": 1, "max": 2, "default": 2},
            {"name": "noise_3d", "label": "三維噪聲干擾", "type": "float", "min": 0.05, "max": 0.5, "default": 0.1}
        ]
    },
    "mlp": {
        "id": "mlp",
        "name": "多層感知器 (MLP Classifier)",
        "type": "classification",
        "equation": "h^{(l)} = f(W^{(l)}h^{(l-1)} + b^{(l)})",
        "description": "前饋全連接神經網絡，通過一個或多個隱藏層與非線性激活函數擬合極其複雜的映射。",
        "pros": ["具備強大的擬合任意非線性函數的能力", "能處理高複雜度的模式識別"],
        "cons": ["超參數極多，訓練緩慢且容易陷入局部極小值", "屬於黑盒模型，可解釋性差"],
        "params": [
            {"name": "hidden_layer_1", "label": "第一隱藏層節點數", "type": "int", "min": 5, "max": 50, "default": 16},
            {"name": "max_iter", "label": "最大迭代次數", "type": "int", "min": 100, "max": 1000, "default": 300},
            {"name": "activation", "label": "激活函數類型", "type": "str", "options": ["relu", "tanh", "logistic"], "default": "relu"}
        ]
    }
}

class SimulateRequest(BaseModel):
    params: Dict[str, Any]

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

@app.get("/")
def read_root():
    return RedirectResponse(url="http://localhost:3000")

@app.get("/api/algorithms")
def get_algorithms():
    return list(ALGORITHMS.values())

@app.get("/api/algorithms/{algo_id}")
def get_algorithm(algo_id: str):
    if algo_id not in ALGORITHMS:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    return ALGORITHMS[algo_id]

# Generate synthetic dataset helper (returns 2D classification blobs/moons)
def get_classification_data(noise=0.2):
    X, y = make_moons(n_samples=250, noise=noise, random_state=42)
    scaler = StandardScaler()
    X = scaler.fit_transform(X) * 1.5
    return X, y

@app.post("/api/simulate/{algo_id}")
def simulate_algorithm(algo_id: str, req: SimulateRequest):
    params = req.params
    if algo_id not in ALGORITHMS:
        raise HTTPException(status_code=404, detail="Algorithm not found")

    try:
        grid_resolution = 40
        x_min, x_max = -4.0, 4.0
        y_min, y_max = -4.0, 4.0
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, grid_resolution),
                             np.linspace(y_min, y_max, grid_resolution))
        grid_points = np.c_[xx.ravel(), yy.ravel()]

        if algo_id == "linear_regression":
            degree = int(params.get("degree", 2))
            noise = float(params.get("noise", 0.5))
            np.random.seed(42)
            X = np.random.rand(100, 1) * 6 - 3
            y = 0.5 * X**2 + X + 1.0 + np.random.randn(100, 1) * noise
            poly = PolynomialFeatures(degree=degree)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            x_line = np.linspace(-3.5, 3.5, 100).reshape(-1, 1)
            x_line_poly = poly.transform(x_line)
            y_line = model.predict(x_line_poly)
            r2 = float(model.score(X_poly, y))
            mse = float(np.mean((y - model.predict(X_poly)) ** 2))
            points_list = [{"x": float(X[i][0]), "y": float(y[i][0])} for i in range(len(X))]
            line_list = [{"x": float(x_line[i][0]), "y": float(y_line[i][0])} for i in range(len(x_line))]
            return {
                "points": points_list,
                "line": line_list,
                "metrics": {"R2 Score": round(r2, 4), "MSE": round(mse, 4)},
                "extra": {"Coef": [round(c, 3) for c in model.coef_.flatten()], "Intercept": round(float(model.intercept_[0]), 3)}
            }

        elif algo_id == "logistic_regression":
            c_val = float(params.get("C", 1.0))
            penalty = params.get("penalty", "l2")
            X, y = get_classification_data(noise=0.25)
            model = LogisticRegression(C=c_val, penalty=None if penalty == "none" else penalty, solver="lbfgs")
            model.fit(X, y)
            predictions = model.predict(X)
            grid_preds = model.predict(grid_points)
            acc = float(model.score(X, y))
            points_list = [{"x": float(X[i][0]), "y": float(X[i][1]), "label": int(y[i]), "pred": int(predictions[i])} for i in range(len(X))]
            grid_list = [{"x": float(grid_points[i][0]), "y": float(grid_points[i][1]), "pred": int(grid_preds[i])} for i in range(len(grid_points))]
            return {"points": points_list, "boundary": grid_list, "metrics": {"Accuracy": round(acc, 4)}}

        elif algo_id == "decision_tree":
            max_depth = int(params.get("max_depth", 4))
            min_samples_split = int(params.get("min_samples_split", 2))
            X, y = get_classification_data(noise=0.2)
            model = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, random_state=42)
            model.fit(X, y)
            predictions = model.predict(X)
            grid_preds = model.predict(grid_points)
            acc = float(model.score(X, y))
            points_list = [{"x": float(X[i][0]), "y": float(X[i][1]), "label": int(y[i]), "pred": int(predictions[i])} for i in range(len(X))]
            grid_list = [{"x": float(grid_points[i][0]), "y": float(grid_points[i][1]), "pred": int(grid_preds[i])} for i in range(len(grid_points))]
            return {"points": points_list, "boundary": grid_list, "metrics": {"Accuracy": round(acc, 4), "Depth": model.get_depth()}}

        elif algo_id == "random_forest":
            n_estimators = int(params.get("n_estimators", 50))
            max_depth = int(params.get("max_depth", 6))
            X, y = get_classification_data(noise=0.25)
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42, n_jobs=-1)
            model.fit(X, y)
            predictions = model.predict(X)
            grid_preds = model.predict(grid_points)
            acc = float(model.score(X, y))
            importances = [float(imp) for imp in model.feature_importances_]
            points_list = [{"x": float(X[i][0]), "y": float(X[i][1]), "label": int(y[i]), "pred": int(predictions[i])} for i in range(len(X))]
            grid_list = [{"x": float(grid_points[i][0]), "y": float(grid_points[i][1]), "pred": int(grid_preds[i])} for i in range(len(grid_points))]
            return {
                "points": points_list,
                "boundary": grid_list,
                "metrics": {"Accuracy": round(acc, 4)},
                "extra": {"Feature Importances": [round(imp, 4) for imp in importances]}
            }

        elif algo_id == "svm":
            c_val = float(params.get("C", 1.0))
            gamma = float(params.get("gamma", 0.5))
            kernel = params.get("kernel", "rbf")
            X, y = get_classification_data(noise=0.25)
            model = SVC(C=c_val, gamma=gamma, kernel=kernel, random_state=42)
            model.fit(X, y)
            predictions = model.predict(X)
            grid_preds = model.predict(grid_points)
            acc = float(model.score(X, y))
            support_vectors = model.support_.tolist()
            points_list = []
            for i in range(len(X)):
                points_list.append({
                    "x": float(X[i][0]), 
                    "y": float(X[i][1]), 
                    "label": int(y[i]), 
                    "pred": int(predictions[i]),
                    "is_support": i in support_vectors
                })
            grid_list = [{"x": float(grid_points[i][0]), "y": float(grid_points[i][1]), "pred": int(grid_preds[i])} for i in range(len(grid_points))]
            return {"points": points_list, "boundary": grid_list, "metrics": {"Accuracy": round(acc, 4), "Support Vectors count": len(support_vectors)}}

        elif algo_id == "knn":
            n_neighbors = int(params.get("n_neighbors", 5))
            weights = params.get("weights", "uniform")
            X, y = get_classification_data(noise=0.25)
            model = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights)
            model.fit(X, y)
            predictions = model.predict(X)
            grid_preds = model.predict(grid_points)
            acc = float(model.score(X, y))
            points_list = [{"x": float(X[i][0]), "y": float(X[i][1]), "label": int(y[i]), "pred": int(predictions[i])} for i in range(len(X))]
            grid_list = [{"x": float(grid_points[i][0]), "y": float(grid_points[i][1]), "pred": int(grid_preds[i])} for i in range(len(grid_points))]
            return {"points": points_list, "boundary": grid_list, "metrics": {"Accuracy": round(acc, 4)}}

        elif algo_id == "naive_bayes":
            var_smoothing_pow = int(params.get("var_smoothing", 9))
            var_smoothing = 10 ** (-var_smoothing_pow)
            X, y = get_classification_data(noise=0.3)
            model = GaussianNB(var_smoothing=var_smoothing)
            model.fit(X, y)
            predictions = model.predict(X)
            grid_preds = model.predict(grid_points)
            acc = float(model.score(X, y))
            points_list = [{"x": float(X[i][0]), "y": float(X[i][1]), "label": int(y[i]), "pred": int(predictions[i])} for i in range(len(X))]
            grid_list = [{"x": float(grid_points[i][0]), "y": float(grid_points[i][1]), "pred": int(grid_preds[i])} for i in range(len(grid_points))]
            return {"points": points_list, "boundary": grid_list, "metrics": {"Accuracy": round(acc, 4)}}

        elif algo_id == "kmeans":
            n_clusters = int(params.get("n_clusters", 4))
            init_type = params.get("init_type", "k-means++")
            np.random.seed(42)
            X, _ = make_blobs(n_samples=200, centers=4, cluster_std=0.75, random_state=42)
            scaler = StandardScaler()
            X = scaler.fit_transform(X) * 1.5
            model = KMeans(n_clusters=n_clusters, init=init_type, random_state=42, n_init=10)
            model.fit(X)
            labels = model.labels_.tolist()
            centroids = model.cluster_centers_.tolist()
            points_list = [{"x": float(X[i][0]), "y": float(X[i][1]), "label": int(labels[i])} for i in range(len(X))]
            centroids_list = [{"x": float(c[0]), "y": float(c[1]), "id": idx} for idx, c in enumerate(centroids)]
            return {"points": points_list, "centroids": centroids_list, "metrics": {"Inertia (WCSS)": round(model.inertia_, 2)}}

        elif algo_id == "pca":
            n_components = int(params.get("n_components", 2))
            noise_3d = float(params.get("noise_3d", 0.1))
            np.random.seed(42)
            x_raw = np.random.randn(150)
            y_raw = np.random.randn(150)
            z_raw = 0.8 * x_raw + 0.5 * y_raw + np.random.randn(150) * noise_3d
            X_3d = np.column_stack((x_raw, y_raw, z_raw))
            color_labels = (x_raw > 0).astype(int) + (y_raw > 0).astype(int) * 2
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_3d)
            model = PCA(n_components=n_components)
            X_projected = model.fit_transform(X_scaled)
            points_list = []
            for i in range(len(X_scaled)):
                points_list.append({
                    "orig_x": float(X_scaled[i][0]),
                    "orig_y": float(X_scaled[i][1]),
                    "orig_z": float(X_scaled[i][2]),
                    "x": float(X_projected[i][0]),
                    "y": float(X_projected[i][1]) if n_components == 2 else 0.0,
                    "label": int(color_labels[i])
                })
            variance_ratio = [float(r) for r in model.explained_variance_ratio_]
            return {
                "points": points_list,
                "metrics": {
                    "PC1 Variance": round(variance_ratio[0], 4),
                    "PC2 Variance": round(variance_ratio[1], 4) if len(variance_ratio) > 1 else 0.0,
                    "Cumulative Variance": round(sum(variance_ratio), 4)
                }
            }

        elif algo_id == "mlp":
            hidden_layer_1 = int(params.get("hidden_layer_1", 16))
            activation = params.get("activation", "relu")
            max_iter = int(params.get("max_iter", 300))
            X, y = get_classification_data(noise=0.25)
            model = MLPClassifier(hidden_layer_sizes=(hidden_layer_1, 8), activation=activation, max_iter=max_iter, random_state=42, solver="adam")
            model.fit(X, y)
            predictions = model.predict(X)
            grid_preds = model.predict(grid_points)
            acc = float(model.score(X, y))
            points_list = [{"x": float(X[i][0]), "y": float(X[i][1]), "label": int(y[i]), "pred": int(predictions[i])} for i in range(len(X))]
            grid_list = [{"x": float(grid_points[i][0]), "y": float(grid_points[i][1]), "pred": int(grid_preds[i])} for i in range(len(grid_points))]
            return {"points": points_list, "boundary": grid_list, "metrics": {"Accuracy": round(acc, 4), "Loss": round(float(model.loss_), 4)}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

# Local ML Knowledge Base for QA
LOCAL_KNOWLEDGE = {
    "linear_regression": "線性回歸 (Linear Regression) 是建立自變量與應變量線性關係的首選模型。核心公式為 y = XW + b，使用最小二乘法 (OLS) 求解使殘差平方和最小的參數。其基本假設包括線性關係、誤差項獨立同方差與正態分布。參數調優主要是調整多項式特徵階數 (Degree) 以擬合非線性，並使用 Ridge/Lasso 正則化防止過擬合。",
    "logistic_regression": "邏輯回歸 (Logistic Regression) 用於二元分類。它將線性回歸的輸出通過 Sigmoid 函數 1/(1+e^-z) 映射到 (0, 1) 區間，解讀為概率值。核心損失函數為交叉熵 (Cross Entropy)。常見調參為 C 參數（正則化強度的倒數），C 越小正則化越強，能有效防止模型過擬合。",
    "decision_tree": "決策樹 (Decision Tree) 是一種樹狀分類與回歸結構。CART 演算法使用基尼指數 (Gini) 來選擇分裂節點特徵。決策樹最大的優勢是具備極佳的白盒可解釋性，但極易過擬合。調參時建議限制最大樹深度 (max_depth) 或增加葉節點最小樣本數，進行預剪枝。",
    "random_forest": "隨機森林 (Random Forest) 是集成了多棵決策樹的 Bagging 演算法。它在訓練時採用 Bootstrap 自助採樣，並在節點分裂時隨機選擇子特徵，降低樹之間的相關性。優點是泛化能力極強、抗過擬合，且能輸出特徵重要性；缺點是相較於單棵樹失去了直觀可解釋性。",
    "svm": "支援向量機 (Support Vector Machine, SVM) 尋找最大間隔的分離超平面。對於非線性問題，SVM 使用核函數 (Kernel Trick) 如高斯 RBF 核將數據投影到高維空間進行線性分割。核心參數包括 C（對錯誤分類的懲罰係數）和 gamma（決定 RBF 核映射空間的分散半徑）。C 越大，Gamma 越大，模型越容易過擬合。",
    "knn": "K-最近鄰 (KNN) 是一種基於距離度量的懶學習分類器。預測時，它找出與新樣本最近的 K 個訓練樣本，通過多數投票決定類別。KNN 完全沒有顯式的訓練階段，但預測時計算複雜度高。K 值過小容易過擬合，過大容易欠擬合；且使用 KNN 前必須對特徵進行標準化以消除量綱影響。",
    "naive_bayes": "朴素貝葉斯 (Naive Bayes) 基於貝葉斯定理與特徵條件獨立性假設。它通過計算先驗和條件概率，預測樣本屬於各類的後驗概率。雖然獨立假設在實務中常被違背，但它在垃圾郵件分類、情感分析等文本高維稀疏特徵上運算極快且表現極佳。 var_smoothing 是其常見的平滑係數。",
    "kmeans": "K-Means 是一種無監督的質心聚類演算法。它交替執行「將樣本分配給最近質心」與「更新質心為簇內均值」兩步，最小化 WCSS。K-Means 需要預先指定簇數 K（可用手肘法或輪廓係數確定）。它對初始質心敏感，所以建議使用 K-Means++ 初始化以加速收斂。",
    "pca": "主成分分析 (PCA) 是經典的無監督線性降維法。它通過協方差矩陣的特徵值分解或奇異值分解 (SVD)，尋找投影方差最大的正交主成分方向，把高維數據投影到低維空間。主要用於特徵降噪、共線性消除與高維數據的 2D/3D 可視化。",
    "mlp": "多層感知器 (MLP) 是一種前饋人工神經網絡，由輸入層、隱藏層和輸出層組成。它通過權重加權、非線性激活函數（如 ReLU、tanh）以及反向傳播 (Backpropagation) 鏈式法則求導更新參數。它是深度學習的前身，能擬合極為複雜的非線性關係，但參數多、易過擬合且黑盒性強。"
}

@app.post("/api/chat")
def chat_assistant(req: ChatRequest):
    user_msg = req.message.strip().lower()
    
    # Check if Gemini API key is available for real LLM reasoning
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            # Build API endpoint url
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            # Formulate prompt including context of the app
            system_context = (
                "你是一位專業的 AI 機器學習學術與實踐專家助理。正在一個機器學習演算法動態視覺化學習平台中提供諮詢。"
                "請使用親切、專業的語氣，以『繁體中文』回答使用者關於機器學習、模型訓練、這 10 種演算法（線性回歸、邏輯回歸、決策樹、隨機森林、SVM、KNN、朴素貝葉斯、K-Means、PCA、MLP）的數學、調參或概念問題。\n\n"
            )
            
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": system_context + f"使用者提問：{req.message}"}]
                    }
                ]
            }
            
            req_data = json.dumps(payload).encode("utf-8")
            api_req = urllib.request.Request(
                url, 
                data=req_data, 
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(api_req, timeout=12) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                ai_text = res_data["contents"][0]["parts"][0]["text"]
                return {"response": ai_text}
                
        except Exception as e:
            # If Gemini API call fails, fall back to local rule-based database
            print("Gemini API call failed, falling back to local database:", e)
            pass

    # --- Local Expert Rule Engine ---
    response_text = ""
    
    # Simple semantic keyword matching
    if any(k in user_msg for k in ["svm", "支援向量", "向量機", "support vector"]):
        response_text = LOCAL_KNOWLEDGE["svm"]
    elif any(k in user_msg for k in ["random forest", "隨機森林", "rf"]):
        response_text = LOCAL_KNOWLEDGE["random_forest"]
    elif any(k in user_msg for k in ["decision tree", "決策樹", "tree"]):
        response_text = LOCAL_KNOWLEDGE["decision_tree"]
    elif any(k in user_msg for k in ["knn", "最近鄰", "neighbors"]):
        response_text = LOCAL_KNOWLEDGE["knn"]
    elif any(k in user_msg for k in ["linear", "線性回歸", "linear regression"]):
        response_text = LOCAL_KNOWLEDGE["linear_regression"]
    elif any(k in user_msg for k in ["logistic", "邏輯回歸", "logistic regression"]):
        response_text = LOCAL_KNOWLEDGE["logistic_regression"]
    elif any(k in user_msg for k in ["naive bayes", "貝葉斯", "bayes"]):
        response_text = LOCAL_KNOWLEDGE["naive_bayes"]
    elif any(k in user_msg for k in ["kmeans", "k-means", "聚類", "kmeans"]):
        response_text = LOCAL_KNOWLEDGE["kmeans"]
    elif any(k in user_msg for k in ["pca", "主成分", "降維"]):
        response_text = LOCAL_KNOWLEDGE["pca"]
    elif any(k in user_msg for k in ["mlp", "感知器", "神經網路", "network"]):
        response_text = LOCAL_KNOWLEDGE["mlp"]
    elif any(k in user_msg for k in ["overfit", "過擬合", "overfitting"]):
        response_text = "過擬合 (Overfitting) 指模型在訓練集上準確度極高，但在測試集或新數據上表現差。主要因為模型過於複雜、訓練次數過多或數據噪聲大。解決方案包括：1. 增加正則化懲罰（如 Ridge L2 / Lasso L1 或 SVM 中的減小 C 參數）；2. 進行預剪枝限制樹深度；3. 增加訓練數據或採用 Dropout 隨機失活節點。"
    elif any(k in user_msg for k in ["underfit", "欠擬合", "underfitting"]):
        response_text = "欠擬合 (Underfitting) 指模型過於簡單，連訓練數據的底層特徵都無法很好學習。例如用簡單線性回歸去擬合非線性曲線。解決方案包括：1. 增加特徵維度（如進行多項式擴展 PolynomialFeatures）；2. 換用更複雜的非線性模型（如 SVM RBF 核、隨機森林或 MLP）；3. 減少正則化約束。"
    elif any(k in user_msg for k in ["哈囉", "hello", "hi", "你好", "您好"]):
        response_text = "您好！我是您的機器學習 AI 助理。您可以問我任何關於線性回歸、邏輯回歸、SVM、隨機森林、K-Means、PCA、MLP 等演算法的數學公式、參數調參、優缺點或機器學習概念問題！"
    else:
        response_text = (
            "您好！我是您的機器學習學習助理。我能為您詳細解答平台支持的十種演算法的相關知識。\n\n"
            "您可以試著問我以下問題：\n"
            "1. 『什麼是支援向量機 (SVM)？』\n"
            "2. 『如何解決模型的過擬合 (Overfitting)？』\n"
            "3. 『K-Means 與隨機森林各別有什麼優缺點？』\n"
            "4. 『PCA 降維的協方差矩陣是如何分解的？』"
        )
        
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
