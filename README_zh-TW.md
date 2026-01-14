# 臺灣忘記切換注音輸入法之翻譯機 (Bopomofo Translator)

這是一個 Python 工具，用來將不小心在英文模式下打出的注音亂碼（如 `su3cl3`）還原回正確的繁體中文（`你好`）。支援命令行操作 (CLI) 與背景剪貼簿監聽服務。

[English README](README.md)

## 功能特色

- **命令行工具 (CLI)**：在終端機直接轉換文字。
- **剪貼簿監聽器**：背景執行，按下快捷鍵 `Ctrl+Alt+V` 即可自動修復選取或剪貼簿中的亂碼文字。
- **雙模式支援**：
  - **線上模式 (預設)**：使用 Google Input Tools API 進行智慧選詞，準確度高。
  - **離線模式**：使用本地端的注音符號映射演算法 (標準大千鍵盤)，無需網路即可運作。
- **智慧修正**：支援長句與混合輸入的遞迴修正。

## 安裝步驟

1. clone 專案到本機

2. 使用 pip 安裝：
   ```bash
   pip install .
   ```

   開發者模式 (編輯即生效)：
   ```bash
   pip install -e .
   ```

## 使用教學

### 命令行介面 (CLI)

安裝後，你可以直接在終端機使用 `bopomofo` 指令：

**單句轉換：**
```bash
bopomofo su3cl3
# 輸出: 你好
```

**互動模式：**
```bash
bopomofo
# 進入互動介面，輸入 exit 離開
```

**離線模式 (顯示注音符號)：**
```bash
bopomofo -l su3cl3
# 輸出: ㄋㄧˇㄏㄠˇ
```

### 剪貼簿監聽服務 (桌面小工具)

啟動背景服務以在任何軟體中修復文字：

```bash
bopomofo-monitor
```

**使用方法：**
1. 在任何應用程式中選取打錯的亂碼 (例如 `ji394su3`)。
2. 複製它 (`Ctrl+C`)。
3. 按下快捷鍵 **`Ctrl+Alt+V`**。
4. 程式會自動翻譯並將正確的中文貼上蓋過原文。

## 設定

可以透過環境變數調整設定：

- `BOPOMOFO_HOTKEY`: 自訂監聽熱鍵 (預設: `ctrl+alt+v`)。
- `LOG_LEVEL`: 日誌詳細程度 (`DEBUG`, `INFO`, `WARNING`, `ERROR`)。

## 開發

執行測試：
```bash
pip install pytest requests-mock
pytest
```

## 授權

MIT
