import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import Head from 'next/head'

export default function AlgorithmPage() {
  const router = useRouter()
  const { id } = router.query

  const [metadata, setMetadata] = useState(null)
  const [params, setParams] = useState({})
  const [simulationData, setSimulationData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [simulating, setSimulating] = useState(false)
  const [error, setError] = useState(null)

  // Fetch algorithm metadata
  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetch(`http://127.0.0.1:8000/api/algorithms/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error('Algorithm not found')
        return res.json()
      })
      .then((data) => {
        setMetadata(data)
        // Initialize default parameters
        const initialParams = {}
        data.params.forEach(p => {
          initialParams[p.name] = p.default
        })
        setParams(initialParams)
        setLoading(false)
      })
      .catch((err) => {
        console.error(err)
        setError(err.message)
        setLoading(false)
      })
  }, [id])

  // Run simulation whenever params change
  useEffect(() => {
    if (!id || Object.keys(params).length === 0) return
    setSimulating(true)
    fetch(`http://127.0.0.1:8000/api/simulate/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ params })
    })
      .then((res) => {
        if (!res.ok) throw new Error('Simulation failed')
        return res.json()
      })
      .then((data) => {
        setSimulationData(data)
        setSimulating(false)
      })
      .catch((err) => {
        console.error(err)
        setSimulating(false)
      })
  }, [id, params])

  if (loading) {
    return <div className="loading-container">載入中...</div>
  }

  if (error || !metadata) {
    return (
      <div className="error-container">
        <h3>未找到該演算法或後端伺服器未啟動</h3>
        <p>請確認您的 FastAPI 後端伺服器已在 http://localhost:8000 運行。</p>
        <Link href="/" className="btn-accent" style={{ marginTop: '20px' }}>返回主頁</Link>
      </div>
    )
  }

  const handleParamChange = (name, val, type) => {
    let parsedVal = val
    if (type === 'int') parsedVal = parseInt(val, 10)
    else if (type === 'float') parsedVal = parseFloat(val)
    setParams(prev => ({
      ...prev,
      [name]: parsedVal
    }))
  }

  // Helper to map values from [-4, 4] coordinate space to [0, 500] SVG space
  const mapCoord = (val) => {
    return ((val + 4.0) / 8.0) * 500
  }

  // Generate python code dynamically based on parameters
  const generatePythonCode = () => {
    const lines = []
    lines.push("# -*- coding: utf-8 -*-")
    lines.push("from sklearn.model_selection import train_test_split")
    
    if (id === 'linear_regression') {
      lines.push("from sklearn.linear_model import LinearRegression")
      lines.push("from sklearn.preprocessing import PolynomialFeatures")
      lines.push("from sklearn.pipeline import make_pipeline")
      lines.push("")
      lines.push(`# 階數為 ${params.degree || 2} 的多項式線性回歸`)
      lines.push(`model = make_pipeline(PolynomialFeatures(degree=${params.degree || 2}), LinearRegression())`)
    } else if (id === 'logistic_regression') {
      lines.push("from sklearn.linear_model import LogisticRegression")
      lines.push("")
      lines.push(`# C=${params.C || 1.0}, penalty='${params.penalty || 'l2'}'`)
      lines.push(`model = LogisticRegression(C=${params.C || 1.0}, penalty=${params.penalty === 'none' ? 'None' : `'${params.penalty}'`})`)
    } else if (id === 'decision_tree') {
      lines.push("from sklearn.tree import DecisionTreeClassifier")
      lines.push("")
      lines.push(`# max_depth=${params.max_depth || 4}`)
      lines.push(`model = DecisionTreeClassifier(max_depth=${params.max_depth || 4}, min_samples_split=${params.min_samples_split || 2}, random_state=42)`)
    } else if (id === 'random_forest') {
      lines.push("from sklearn.ensemble import RandomForestClassifier")
      lines.push("")
      lines.push(`# n_estimators=${params.n_estimators || 50}, max_depth=${params.max_depth || 6}`)
      lines.push(`model = RandomForestClassifier(n_estimators=${params.n_estimators || 50}, max_depth=${params.max_depth || 6}, random_state=42)`)
    } else if (id === 'svm') {
      lines.push("from sklearn.svm import SVC")
      lines.push("")
      lines.push(`# kernel='${params.kernel || 'rbf'}', C=${params.C || 1.0}, gamma=${params.gamma || 0.5}`)
      lines.push(`model = SVC(kernel='${params.kernel || 'rbf'}', C=${params.C || 1.0}, gamma=${params.gamma || 0.5}, random_state=42)`)
    } else if (id === 'knn') {
      lines.push("from sklearn.neighbors import KNeighborsClassifier")
      lines.push("")
      lines.push(`# n_neighbors=${params.n_neighbors || 5}, weights='${params.weights || 'uniform'}'`)
      lines.push(`model = KNeighborsClassifier(n_neighbors=${params.n_neighbors || 5}, weights='${params.weights || 'uniform'}')`)
    } else if (id === 'naive_bayes') {
      lines.push("from sklearn.naive_bayes import GaussianNB")
      lines.push("")
      lines.push(`# var_smoothing = 1e-${params.var_smoothing || 9}`)
      lines.push(`model = GaussianNB(var_smoothing=1e-${params.var_smoothing || 9})`)
    } else if (id === 'kmeans') {
      lines.push("from sklearn.cluster import KMeans")
      lines.push("")
      lines.push(`# n_clusters=${params.n_clusters || 4}, init='${params.init_type || 'k-means++'}'`)
      lines.push(`model = KMeans(n_clusters=${params.n_clusters || 4}, init='${params.init_type || 'k-means++'}', random_state=42)`)
    } else if (id === 'pca') {
      lines.push("from sklearn.decomposition import PCA")
      lines.push("")
      lines.push(`# n_components=${params.n_components || 2}`)
      lines.push(`model = PCA(n_components=${params.n_components || 2})`)
    } else if (id === 'mlp') {
      lines.push("from sklearn.neural_network import MLPClassifier")
      lines.push("")
      lines.push(`# hidden_layer_sizes=(${params.hidden_layer_1 || 16}, 8)`)
      lines.push(`model = MLPClassifier(hidden_layer_sizes=(${params.hidden_layer_1 || 16}, 8), activation='${params.activation || 'relu'}', max_iter=${params.max_iter || 300}, random_state=42)`)
    }
    
    lines.push("model.fit(X_train, y_train)")
    lines.push("score = model.score(X_test, y_test)")
    lines.push("print('Model accuracy/score:', score)")
    
    return lines.join('\n')
  }

  return (
    <>
      <Head>
        <title>{metadata.name} | Dynamic Learning dashboard</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
      </Head>

      <header>
        <div className="nav-container">
          <Link href="/" className="logo">JER LIAW</Link>
          <ul className="nav-links">
            <li><Link href="/">Home</Link></li>
            <li><Link href="/#portfolio">Portfolio</Link></li>
            <li><Link href="/#about">About</Link></li>
          </ul>
          <span className="lang-selector">EN ▼</span>
        </div>
      </header>

      <div className="algo-dashboard">
        {/* Sidebar Controls */}
        <div className="sidebar">
          <Link href="/" className="btn-card" style={{ marginBottom: '20px' }}>
            <i className="fa-solid fa-arrow-left"></i> 返回主頁
          </Link>
          <h2 className="sidebar-title">{metadata.name}</h2>
          <p className="sidebar-desc">{metadata.description}</p>
          
          <h4 style={{ margin: '20px 0 10px', fontSize: '14px', textTransform: 'uppercase', color: '#1E293B' }}>
            調整模型超參數 (Parameters)
          </h4>

          {metadata.params.map(p => (
            <div key={p.name} className="control-group">
              <label className="control-label">
                {p.label} 
                {p.type !== 'str' && <span className="range-val">{params[p.name]}</span>}
              </label>
              
              {p.type === 'str' ? (
                <select 
                  className="control-input" 
                  value={params[p.name] || p.default} 
                  onChange={(e) => handleParamChange(p.name, e.target.value, p.type)}
                >
                  {p.options.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              ) : (
                <input 
                  type="range" 
                  className="control-range"
                  min={p.min} 
                  max={p.max} 
                  step={p.type === 'float' ? 0.05 : 1}
                  value={params[p.name] || p.default}
                  onChange={(e) => handleParamChange(p.name, e.target.value, p.type)}
                />
              )}
            </div>
          ))}

          {simulating && <div style={{ fontSize: '12px', color: '#E67E22', fontStyle: 'italic' }}>重新計算模型中...</div>}
        </div>

        {/* Main Content Area */}
        <div className="main-content">
          {/* Section 1: Dynamic Visual Simulation */}
          <div className="panel">
            <h3 className="panel-title">即時視覺化模擬 (Live Simulation Plot)</h3>
            <div className="plot-container">
              {simulationData ? (
                <svg width="500" height="500" style={{ border: '1px solid #E2E8F0', backgroundColor: '#FFFFFF', overflow: 'hidden', borderRadius: '4px' }}>
                  {/* Draw Decision Boundary Grid for Classification */}
                  {simulationData.boundary && simulationData.boundary.map((pt, idx) => (
                    <rect 
                      key={`grid-${idx}`} 
                      x={mapCoord(pt.x) - 6} 
                      y={mapCoord(pt.y) - 6} 
                      width="12" 
                      height="12" 
                      fill={pt.pred === 1 ? 'rgba(74, 144, 226, 0.15)' : 'rgba(230, 126, 34, 0.15)'}
                      stroke="none"
                    />
                  ))}

                  {/* Draw Regression Line */}
                  {simulationData.line && (
                    <path 
                      d={`M ${simulationData.line.map(pt => `${mapCoord(pt.x)} ${mapCoord(pt.y)}`).join(' L ')}`}
                      fill="none" 
                      stroke="#2563EB" 
                      strokeWidth="3.5"
                    />
                  )}

                  {/* Draw Normal Data Points */}
                  {simulationData.points && simulationData.points.map((pt, idx) => {
                    // Determine color based on label (kmeans uses multi-labels, classification uses 0/1)
                    let fill = '#64748B'
                    if (pt.label !== undefined) {
                      const colors = ['#E67E22', '#2563EB', '#10B981', '#F59E0B', '#8B5CF6']
                      fill = colors[pt.label % colors.length]
                    }
                    
                    return (
                      <circle 
                        key={`pt-${idx}`} 
                        cx={mapCoord(pt.x)} 
                        cy={mapCoord(pt.y)} 
                        r={pt.is_support ? 6.5 : 4.5} 
                        fill={fill}
                        stroke={pt.is_support ? '#000000' : 'none'}
                        strokeWidth={pt.is_support ? 2 : 0}
                        className="dot"
                      />
                    )
                  })}

                  {/* Draw K-Means Centroids */}
                  {simulationData.centroids && simulationData.centroids.map((centroid, idx) => (
                    <g key={`centroid-${idx}`}>
                      {/* Big circle outline */}
                      <circle 
                        cx={mapCoord(centroid.x)} 
                        cy={mapCoord(centroid.y)} 
                        r="10" 
                        fill="rgba(239, 68, 68, 0.2)" 
                        stroke="#EF4444" 
                        strokeWidth="2" 
                      />
                      {/* Inner X marker */}
                      <line x1={mapCoord(centroid.x) - 5} y1={mapCoord(centroid.y) - 5} x2={mapCoord(centroid.x) + 5} y2={mapCoord(centroid.y) + 5} stroke="#EF4444" strokeWidth="2.5" />
                      <line x1={mapCoord(centroid.x) + 5} y1={mapCoord(centroid.y) - 5} x2={mapCoord(centroid.x) - 5} y2={mapCoord(centroid.y) + 5} stroke="#EF4444" strokeWidth="2.5" />
                    </g>
                  ))}
                </svg>
              ) : (
                <div style={{ color: '#94A3B8' }}>載入模擬圖表中...</div>
              )}
            </div>
            
            {simulationData && simulationData.metrics && (
              <div style={{ marginTop: '20px' }}>
                <h4 style={{ fontSize: '13px', color: '#64748B', textTransform: 'uppercase', marginBottom: '10px' }}>
                  模型效能指標 (Metrics)
                </h4>
                <div className="metrics-grid">
                  {Object.entries(simulationData.metrics).map(([key, val]) => (
                    <div key={key} className="metric-card">
                      <div className="metric-label">{key}</div>
                      <div className="metric-val">{val}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Section 2: Mathematical Foundations */}
          <div className="panel">
            <h3 className="panel-title">數學基礎與核心公式</h3>
            <p style={{ marginBottom: '10px', fontSize: '14px' }}>該演算法的決策規則或損失函數主要數學表達：</p>
            <div className="math-block">
              {metadata.equation}
            </div>
            <div className="pros-cons-grid" style={{ marginTop: '20px' }}>
              <div className="pros-card">
                <h4>優點 (Pros)</h4>
                <ul>
                  {metadata.pros.map((p, idx) => <li key={idx}>{p}</li>)}
                </ul>
              </div>
              <div className="cons-card">
                <h4>缺點 (Cons)</h4>
                <ul>
                  {metadata.cons.map((c, idx) => <li key={idx}>{c}</li>)}
                </ul>
              </div>
            </div>
          </div>

          {/* Section 3: Executable Code Block */}
          <div className="panel">
            <h3 className="panel-title">可執行 Python 程式碼 (scikit-learn)</h3>
            <p style={{ marginBottom: '10px', fontSize: '14px' }}>
              以下為對應當前超參數設定下的最小可執行 Python 代碼，點擊代碼即可複製：
            </p>
            <pre className="code-pre" onClick={() => {
              navigator.clipboard.writeText(generatePythonCode())
              alert('代碼已複製到剪貼簿！')
            }} style={{ cursor: 'pointer' }}>
              <code>
                {generatePythonCode()}
              </code>
            </pre>
          </div>
        </div>
      </div>
    </>
  )
}
