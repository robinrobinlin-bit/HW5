# ML-Whitepaper-Generator (機器學習演算法白皮書生成器)

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Library](https://img.shields.io/badge/PDF%20Engine-ReportLab-orange.svg?style=flat-square)](https://www.reportlab.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

本專案是一個基於 Python 的自動化技術白皮書與報告編譯工具。專為產生高品質、格式精美且原生支援**繁體中文排版**的機器學習技術白皮書而設計，可一鍵產生包含豐富圖表、程式碼高亮、數學公式及對比表格的 PDF 技術報告。

---

## 🚀 核心功能特點 (Features)

* 📝 **超長篇幅自動生成**：原生支援一鍵編譯出超過 20,000 字的完整機器學習演算法技術報告，包含十種核心演算法的數學推導、代碼與應用。
* 🔤 **完美中文排版支援**：內建微軟正黑體（Microsoft JhengHei）映射與註冊機制，解決傳統 PDF 產生工具中常見的中文字元亂碼或黑塊（■）問題。
* 🎨 **精美商業排版設計**：
  * **封面設計**：包含科技感藍色主題飾條、標題、副標題與作者版本中介資料。
  * **目錄與頁首頁尾**：自動對齊的點狀目錄與動態「頁碼 / 頁首」標題繪製。
  * **資料視覺化**：自訂雙色交替背景的效能比較表與高解析度資訊圖表嵌入。
* 🛠️ **多引擎靈活編譯**：支援基於 Python `reportlab` 的原生純程式碼編譯，以及利用 `pandoc` / `TinyTeX` 的 Markdown-to-PDF 轉換引擎。

---

## 🛠️ 快速上手 (Getting Started)

### 環境需求 (Prerequisites)

* **Python**：`>= 3.8`
* **作業系統**：Windows (已預配置 `msjh.ttc` 字型檔路徑)，Linux/macOS 使用者需更換自訂中文字型路徑。

### 安裝步驟 (Installation)

1. 克隆專案到本地：
   ```bash
   git clone https://github.com/your-username/ML-Whitepaper-Generator.git
   cd ML-Whitepaper-Generator
   ```

2. 安裝核心依賴套件：
   ```bash
   pip install reportlab pillow
   ```

3. *(選用)* 如果您需要使用 Pandoc/TinyTeX 轉換引擎，請安裝：
   ```bash
   pip install pypandoc pytinytex
   python install_tinytex.py
   ```

---

## 📖 使用範例 (Usage)

### 1. 產生預設的 premium 機器學習白皮書
執行主生成指令，將自動讀取內建的 20,000+ 字資料並編譯輸出高品質 PDF：
```bash
python generate_whitepaper.py
```
* 預設輸出路徑：`C:/Users/user/Desktop/hw8_svm/whitepaper_premium.pdf`

### 2. 將自訂的 Markdown 檔案轉為 PDF
如果您有自己的 `whitepaper.md` 檔案，可以使用 ReportLab 快速解析器進行輕量化轉換：
```bash
python generate_pdf_reportlab.py
```

---

## 🤝 開發與貢獻 (Contributing)

歡迎提交 Issue 或 Pull Request 來改進本專案！在貢獻代碼時，請確保：
1. 程式碼符合 PEP 8 規範。
2. 涉及 LaTeX 數學公式的字串請使用 **原始字串 (raw string `r"..."`)**，以避免 Unicode 轉義字元報錯。

---

## 📄 授權條款 (License)

本專案採用 **MIT License** 授權。詳見專案內的 [LICENSE](LICENSE) 檔案。
