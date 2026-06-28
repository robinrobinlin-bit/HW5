# Changelog (變更日誌)

所有本專案的重大變更都將記錄於此檔案中。

本專案格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，並遵循 [Semantic Versioning (語意化版本)](https://semver.org/lang/zh-TW/) 規範。

---

## [1.0.0] - 2026-06-28

### 🚀 Added
* **機器學習十項核心演算法技術白皮書 PDF**：
  * 使用 ReportLab 引擎自動編譯輸出超過 20,000 字中英雙語白皮書檔案 `whitepaper_premium.pdf`。
  * 註冊微軟正黑體 (`msjh.ttc`) 與粗體字型，解決傳統 PDF 的中文字元亂碼與黑塊 (■) 問題。
  * 內嵌 LaTeX 數學公式與標準的 `scikit-learn` Python 代碼區塊。
  * 嵌入高解析度的「十大機器學習演算法資訊圖表」。
  * 整合包含 Accuracy、F1 分數、訓練時間與預測延遲的演算法效能對比基準測試表。
* **動態學習網頁系統 (Next.js + FastAPI)**：
  * **前端 (Next.js)**：建構以 `quantumwings.github.io` 設計風格為範本的極簡高級感響應式介面，使用 Cormorant Garamond 與 Montserrat 字型。
  * **後端 (FastAPI)**：實作機器學習模型即時訓練端點，接收超參數並使用 `scikit-learn` 進行擬合計算。
  * **互動式模擬畫布 (SVG Plot)**：實作 SVM 支持向量高亮、K-Means 動態質心更新 (X 標記)、PCA 三維轉二維投影、線性回歸多項式曲線擬合，以及六種分類器的動態背景決策邊界渲染。
* **AI 互動學習助理**：
  * 在網頁右下角新增懸浮式 AI 聊天助理元件 `ChatWidget.js`。
  * 後端新增 `POST /api/chat` 對話路由，支援 `GEMINI_API_KEY` 環境變數偵測，自動在 Gemini LLM 與本機機器學習專家問答庫之間切換。
  * 新增打字中動畫狀態，並在訊息傳遞時自動滾動至底部。
* **專案建置與組態**：
  * 新增功能完善的 `README.md`，提供安裝流程、使用範例與專案架構。
  * 新增 `.gitignore` 設定檔，全面屏蔽操作系統垃圾檔、IDE 配置、Python 虛擬環境 (`.venv`) 與 Node.js 依賴 (`node_modules`)。
  * 保留多種備用 PDF 轉換指令檔（如 `install_tinytex.py`、`generate_pdf.py`）。

### ⚡ Changed
* 重構原本 Markdown 轉換 PDF 失敗的 Pandoc/LaTeX 流程，全面切換為基於 ReportLab 的純 Python 自動化排版生成方案。

---

> 註：此版本為專案的初始發布版本，已在本機測試環境 (`localhost:3000` 與 `localhost:8000`) 通過完整 HTTP 連線與模擬功能驗證。
