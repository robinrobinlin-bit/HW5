# Changelog (專案開發與變更日誌)

本檔案詳細記錄了今日（2026-06-28）本專案的完整重構、開發、整合與部署步驟。所有變更均遵循 Keep a Changelog 標準與語意化版本規範。

---

## [1.0.0] - 2026-06-28

### 🚀 Added

#### Step 1: 技術白皮書編譯引擎重構與中文化 PDF 輸出
* **目標**：解決原 Markdown 轉 LaTeX/PDF 流程之中文亂碼與字型遺失問題。
* **變更細節**：
  * 放棄依賴 Pandoc 及 LaTeX 虛擬環境，切換為全 Python 自主排版引擎 **ReportLab**。
  * 撰寫 [generate_pdf_reportlab.py](file:///c:/Users/user/Desktop/HW5-1/generate_pdf_reportlab.py) 腳本。
  * 引入並註冊系統內建微軟正黑體字型 `msjh.ttc`（Microsoft JhengHei）與粗體 `msjhbd.ttc`。
  * 精確設計頁面邊距、標題頁（Title Page）、目錄（TOC）、多層級標題（H1, H2, H3）樣式。
  * 建立演算法效能與調參對比表格（包括 Accuracy, F1-Score, Training Time, Inference Latency）。
  * 嵌入 10 大機器學習演算法資訊圖表圖像，生成精緻之 [whitepaper_premium.pdf](file:///C:/Users/user/Desktop/hw8_svm/whitepaper_premium.pdf)。

#### Step 2: 後端 API 伺服器建置 (FastAPI)
* **目標**：提供演算法元數據、即時機器學習模擬與預測邊界，以及 AI 互動對話後端。
* **變更細節**：
  * 在 [backend/main.py](file:///c:/Users/user/Desktop/HW5-1/backend/main.py) 中建立 FastAPI 應用，設定 CORS 跨域請求（支援 `localhost:3000`）。
  * **元數據路由 (`GET /api/algorithms`)**：回傳 10 大演算法的公式、說明、優缺點、參數範圍等。
  * **動態模擬路由 (`POST /api/simulate/{algo_id}`)**：
    * 線性回歸：使用 `PolynomialFeatures` 對噪聲樣本進行 $1 \sim 4$ 階多項式擬合。
    * 分類演算法（邏輯回歸、決策樹、隨機森林、SVM、KNN、Naive Bayes、MLP）：動態接收前端輸入之超參數，以 `make_moons` 生成測試集，並計算分類網格（$40 \times 40$）之決策邊界（Decision Boundary）點。如果是 SVM，則提取支援向量索引以作特殊標記。
    * K-Means 聚類：動態分配樣本分群並計算群中心坐標（Centroids）。
    * PCA 降維：動態接收三維數據，經共變異數矩陣投影，回傳二維降維坐標與解釋方差比。

#### Step 3: 前端視覺化學習面板開發 (Next.js)
* **目標**：建構符合 `quantumwings.github.io` 高質感設計、Montserrat/Cormorant Garamond 字型之響應式動態介面。
* **變更細節**：
  * 建立 Pages 路由架構，包含 [_app.js](file:///c:/Users/user/Desktop/HW5-1/frontend/pages/_app.js)、[index.js](file:///c:/Users/user/Desktop/HW5-1/frontend/pages/index.js) 與 [algorithm/[id].js](file:///c:/Users/user/Desktop/HW5-1/frontend/pages/algorithm/[id].js)。
  * **首頁**：實作高質感 Banner（文字：「Leading enterprises towards excellence. All-round professional managers...」）與十大演算法 Portfolio 卡片網格，採用毛玻璃（Glassmorphism）與懸停動畫。
  * **演算法詳情頁**：
    * 整合滑動參數條（Range Sliders）控制後端模擬。
    * 使用 HTML5 **SVG** 即時繪製二維數據點、擬合曲線、決策邊界與聚類群心。
    * 整合 LaTeX 數學表達式區塊，並展示可隨參數更動即時更新的 `scikit-learn` Python 代碼區塊（點擊即可一鍵複製）。

#### Step 4: AI 學習助理整合與優化
* **目標**：新增讓使用者可隨時詢問演算法相關問題之懸浮式互動視窗。
* **變更細節**：
  * 開發全域組件 [ChatWidget.js](file:///c:/Users/user/Desktop/HW5-1/frontend/components/ChatWidget.js)。
  * 後端新增 `POST /api/chat` 對話接口。實作**雙重問答引擎**：
    * **本地專家問答庫**：當無 `GEMINI_API_KEY` 時，使用語意關鍵字匹配引擎，即時回傳十種演算法的公式推導、過擬合處理、K值選擇等專家回答。
    * **Gemini LLM 引擎**：若偵測到環境變數金鑰，自動升級為調用 Google Gemini API 進行即時自然語言推導回答。
  * 前端實作打字中動畫（Typing Indicator）與訊息滾動聚焦。

#### Step 5: 自動重導向機制實作 (Redirect)
* **目標**：解決手動輸入後端位址 `localhost:8000` 出現 `404 Not Found` 導致使用者困惑的問題。
* **變更細節**：
  * 在 [backend/main.py](file:///c:/Users/user/Desktop/HW5-1/backend/main.py) 中新增根路由阻截器：
    ```python
    @app.get("/")
    def read_root():
        return RedirectResponse(url="http://localhost:3000")
    ```
  * 當使用者於瀏覽器存取 `localhost:8000` 時，系統會自動發送 `307 Temporary Redirect` 將其引導至前端視覺化頁面 `localhost:3000`。

#### Step 6: DevOps 與 Git 雲端同步
* **目標**：整理原始碼並將專案推送至 GitHub 倉庫。
* **變更細節**：
  * 撰寫 [.gitignore](file:///c:/Users/user/Desktop/HW5-1/.gitignore)，分類排除 OS 暫存檔、IDE 設定檔與 Node/Python 依賴庫。
  * 初始化本地 Git 儲存庫並切換預設分支為 `main`。
  * 設定 Git 本地簽章使用者名稱與信箱，防止 commit 失敗。
  * 連結遠端倉庫並成功推送至 GitHub：[https://github.com/robinrobinlin-bit/HW5.git](https://github.com/robinrobinlin-bit/HW5.git)。

---

### 🐛 Fixed
* **修復**：解決 FastAPI 引用 `RedirectResponse` 時，因套件路徑不正確（原從 `fastapi` 導入，應從 `fastapi.responses` 導入）導致後端服務啟動崩潰的 Bug。
* **修復**：修正 python 程式碼中 LaTeX 反斜線與特定轉義字元引發的 `UnicodeEscape SyntaxError`，全面轉換為原始字串 `r"..."` 定義。
