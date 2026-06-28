import { useState, useEffect } from 'react'
import Link from 'next/link'
import Head from 'next/head'

export default function Home() {
  const [algorithms, setAlgorithms] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Map algorithm IDs to icons
  const getIcon = (id) => {
    const icons = {
      linear_regression: 'fa-solid fa-chart-line',
      logistic_regression: 'fa-solid fa-percentage',
      decision_tree: 'fa-solid fa-sitemap',
      random_forest: 'fa-solid fa-tree',
      svm: 'fa-solid fa-bezier-curve',
      knn: 'fa-solid fa-people-arrows-left-right',
      naive_bayes: 'fa-solid fa-calculator',
      kmeans: 'fa-solid fa-circle-nodes',
      pca: 'fa-solid fa-compress',
      mlp: 'fa-solid fa-brain'
    }
    return icons[id] || 'fa-solid fa-gear'
  }

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/algorithms')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch algorithms')
        return res.json()
      })
      .then((data) => {
        setAlgorithms(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error(err)
        setError(err.message)
        setLoading(false)
        // Fallback metadata if API is offline
        setAlgorithms([
          {id: "linear_regression", name: "線性回歸 (Linear Regression)", description: "建立自變量與應變量之間的線性映射關係，採用最小二乘法 (OLS) 求解最佳適應線。"},
          {id: "logistic_regression", name: "邏輯回歸 (Logistic Regression)", description: "使用 Sigmoid 函數將線性預測映射至 (0, 1) 區間，預測二元分類的後驗機率。"},
          {id: "decision_tree", name: "決策樹 (Decision Tree)", description: "透過基尼不純度或資訊增益遞迴劃分特徵空間，建構樹狀判定規則。"},
          {id: "random_forest", name: "隨機森林 (Random Forest)", description: "結合 Bagging 自助抽樣與隨機特徵選擇，集成多棵決策樹進行投票，有效降低方差。"},
          {id: "svm", name: "支援向量機 (Support Vector Machine, SVM)", description: "最大化分類間隔超平面，並透過核函數將低維非線性數據投影到高維空間以實現線性分類。"},
          {id: "knn", name: "K-最近鄰 (K-Nearest Neighbors, KNN)", description: "基於距離度量，尋找空間中最近的 K 個鄰居進行多數投票分類。"},
          {id: "naive_bayes", name: "朴素貝葉斯 (Naive Bayes)", description: "基於貝葉斯定理與特徵條件獨立性假設，快速計算各個類別的後驗概率。"},
          {id: "kmeans", name: "K-Means 聚類 (K-Means Clustering)", description: "無監督聚類演算法，透過交替分配最近質心與更新質心位置，劃分數據為 K 個簇。"},
          {id: "pca", name: "主成分分析 (PCA)", description: "無監督線性降維技術，透過投影矩陣將特徵投影至最大方差的正交子空間上。"},
          {id: "mlp", name: "多層感知器 (MLP Classifier)", description: "前饋全連接神經網絡，通過一個或多個隱藏層與非線性激活函數擬合極其複雜的映射。"}
        ])
      })
  }, [])

  return (
    <>
      <Head>
        <title>JER LIAW | 機器學習演算法動態學習平台</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
      </Head>

      {/* Header */}
      <header>
        <div className="nav-container">
          <Link href="/" className="logo">
            JER LIAW
          </Link>
          <ul className="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#portfolio">Portfolio</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
          <span className="lang-selector">EN ▼</span>
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="hero">
        <div className="hero-content fade-in">
          <h1>Leading enterprises towards excellence</h1>
          <p>
            All-round professional managers with expertise in business management and information technology. 
            Explore and master 10 core machine learning algorithms through interactive dynamic visual simulations.
          </p>
          <a href="#portfolio" className="btn-accent">View Portfolio</a>
        </div>
      </section>

      {/* Portfolio Section */}
      <section id="portfolio" className="portfolio-section">
        <h2 className="section-title">機器學習演算法 (10 Core Themes)</h2>
        <div className="grid">
          {algorithms.map((algo) => (
            <div key={algo.id} className="card">
              <div>
                <div className="card-icon">
                  <i className={getIcon(algo.id)}></i>
                </div>
                <h3 className="card-title">{algo.name}</h3>
                <p className="card-description">{algo.description}</p>
              </div>
              <Link href={`/algorithm/${algo.id}`} className="btn-card">
                開始互動學習 <i className="fa-solid fa-arrow-right-long"></i>
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="about-section">
        <div className="about-content">
          <h2 className="section-title">關於本專案</h2>
          <p>
            本平台為一創新的「軟動態網頁學習系統」，前端基於 Next.js (React) 開發，後端採用 FastAPI 驅動。
            旨在提供互動式的視覺化教學環境，讓學習者能直觀地調整模型的各項超參數，並即時看到預測邊界或聚類效果的變化。
          </p>
          <p>
            這不僅僅是理論，更是將數學基礎（拉格朗日乘子法、高斯分布、梯度下降等）轉換為幾何視覺介面的實踐展示。
          </p>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact-section">
        <h2 className="section-title">聯絡我們</h2>
        <p>如有學術討論或專案合作需求，歡迎隨時聯絡我們。</p>
        <Spacer height={20} />
        <a href="mailto:info@example.com" className="btn-accent">發送郵件</a>
      </section>

      {/* Footer */}
      <footer>
        <p>© 2026 JER LIAW. All rights reserved. 機器學習演算法動態視覺化學習平台.</p>
      </footer>
    </>
  )
}

function Spacer({ height }) {
  return <div style={{ height: `${height}px` }} />
}
