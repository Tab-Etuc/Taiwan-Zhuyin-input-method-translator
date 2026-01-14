# Bopomofo Translator (Taiwan-Zhuyin-input-method-translator)



A Python tool to fix accidentally typed Zhuyin (Bopomofo) alphanumeric characters back to Traditional Chinese. It supports both CLI and a background clipboard monitoring service.

[README (Traditional Chinese)](README_zh-TW.md)

## Features

- **CLI Tool**: Convert text directly in the terminal (e.g., `su3cl3` -> `你好`).
- **Clipboard Monitor**: Fix text quietly in the background. Press `Ctrl+Alt+V` to fix the selected text or clipboard content immediately.
- **Dual Mode**:
  - **Online Mode (Default)**: Uses Google Input Tools API for smart phrase selection.
  - **Offline Mode**: Uses a local mapping algorithm (Standard Daqian/Ta-Chien Layout) for privacy or offline use.
- **Smart Correction**: Automatically handles mixed input and typos using recursive translation logic.

## Installation

1. Clone the repository
   
2. Install the package using pip:
   ```bash
   pip install .
   ```

   For development (editable mode):
   ```bash
   pip install -e .
   ```

## Usage

### Command Line Interface (CLI)

After installation, you can use the `bopomofo` command anywhere:

**Single phrase conversion:**
```bash
bopomofo su3cl3
# 輸出: 你好
```

**Interactive Mode:**
```bash
bopomofo
# 進入互動介面，輸入 exit 離開
```

**Offline Mode:**
```bash
bopomofo -l su3cl3
# 輸出: ㄋㄧˇㄏㄠˇ
```

### Clipboard Monitor Service

Start the background service to fix typos across your system:

`bopomofo-monitor` 

**How to use:**
1. Select the garbled text (like `ji394su3`) in any application.
2. Copy it (`Ctrl+C`) - *Optional if you just typed it and it is still selected*.
3. Press the hotkey **`Ctrl+Alt+V`**.
4. The tool will translate the text and paste the corrected result automatically.

## Configuration

You can configure the tool via environment variables:

- `BOPOMOFO_HOTKEY`: Custom hotkey for the monitor (default: `ctrl+alt+v`).
- `LOG_LEVEL`: Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

## Development

Run tests with pytest:
```bash
pip install pytest requests-mock
pytest
```

## License

MIT
