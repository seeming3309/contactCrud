# 部署教學（依你的上傳專案量身訂做）

此專案包含：
- **後端**：FastAPI（`app/`），API 路徑以 `/api` 開頭，WebSocket `/ws`
- **前端**：Vite + Vue（`frontend/`）

你將得到兩個可以測試的連結：
- GitHub Pages（前端）：`https://<你的帳號>.github.io/<repo 名稱>/`
- Render（後端 API）：`https://<你的服務>.onrender.com/api/health`

---

## 一、把原始碼放上 GitHub

1. 在 GitHub 建立 repo（建議 public）：**不要**先勾選初始化 README。
2. 把這包內容（不是 zip）上傳：
   - 方法A：網頁 → **Add file → Upload files** → 拖進整個專案內容（含 `app/`、`frontend/`、`.github/workflows/` 等）
   - 方法B：git 指令：
     ```bash
     git init
     git add .
     git commit -m "init"
     git branch -M main
     git remote add origin https://github.com/<你>/<repo>.git
     git push -u origin main
     ```

---

## 二、部署後端（FastAPI）到 Render

1. 到 https://render.com → New + → **Web Service** → 連接剛剛的 GitHub repo。
2. 設定：
   - **Build Command**：`pip install -r requirements.txt`
   - **Start Command**：`uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. 建立後等待部署完成，拿到網址：`https://<你的服務>.onrender.com`
4. 測試健康檢查：`https://<你的服務>.onrender.com/api/health` 應回傳 `status: ok`。

> FastAPI CORS 目前允許所有來源（`allow_origins=["*"]`），能先讓你測試順利。若要限定來源，請改 `app/main.py` 的 CORS 設定。

---

## 三、部署前端（Vite）到 GitHub Pages

### 3.1 設定 API Base（GitHub Pages 與 Render 網域不同）
打開 `frontend/.env.production`，把 `VITE_API_BASE` 改成你的後端網址：
```
VITE_API_BASE="https://<你的服務>.onrender.com/api"
```

### 3.2 設定 GitHub Pages 的 base 路徑
我們已調整 `frontend/vite.config.js`，會從環境變數 `VITE_BASE` 讀取 base。  
在 GitHub Actions 檔 `.github/workflows/deploy-pages.yml`：
```yaml
env:
  VITE_BASE: "/REPO_NAME/"
```
請把 **REPO_NAME** 換成你的 repo 名稱（前後都有斜線）。

### 3.3 啟用 GitHub Pages
1. Push 完以上變更後，進 repo 的 **Settings → Pages**，**Source** 選 **GitHub Actions**。
2. 到 **Actions** 觀察 `Deploy Vite to GitHub Pages` 工作流（約 1～2 分鐘）
3. 成功後，**Pages** 會出現你的前端網址：
   - `https://<你的帳號>.github.io/<repo 名稱>/`

---

## 四、在前端測試 API
打開上述前端網址，點擊「新增 / 重新整理」，Network 應看到請求送到：
`https://<你的服務>.onrender.com/api/contacts` 等路由並回應 200。

---

## 五、常見問題
- **白畫面 / assets 404**：`VITE_BASE` 沒有設對，或沒加斜線（應為 `/repo/`）。
- **CORS 錯誤**：先用現在的萬用 `*` 測試；上線再把 `allow_origins` 精準列出 `https://<你的帳號>.github.io`。
- **Render 502**：`--port $PORT` 是否正確？`Start Command` 模組路徑 `app.main:app` 是否正確？
- **Pages 設定找不到**：請先 push 至少一次，且確認是在「該 repo」的 Settings（非個人帳號 Settings）。

祝部署順利！
