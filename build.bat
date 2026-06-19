@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM ============================================================
REM Aeneas Aligner Windows 构建脚本
REM 运行环境: Windows 10/11, 已安装 Python 3.10+
REM 输出: dist\align.exe
REM ============================================================

echo [INFO] 开始构建 Aeneas Aligner ...

REM 1. 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 python，请先安装 Python 3.10+
    exit /b 1
)

REM 2. 创建虚拟环境
if exist "venv" (
    echo [INFO] 使用已有的 venv
) else (
    echo [INFO] 创建虚拟环境 ...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM 3. 安装依赖
echo [INFO] 安装 Python 依赖 ...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] 依赖安装失败
    exit /b 1
)

REM 4. 下载 FFmpeg (Windows essential build)
if not exist "ffmpeg" (
    echo [INFO] 下载 FFmpeg ...
    curl -L -o ffmpeg.zip "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    if errorlevel 1 (
        echo [ERROR] FFmpeg 下载失败
        exit /b 1
    )
    tar -xf ffmpeg.zip
    for /d %%D in (ffmpeg-*) do (
        move "%%D" "ffmpeg"
        goto :ffdone
    )
    :ffdone
    del ffmpeg.zip
) else (
    echo [INFO] FFmpeg 已存在
)

REM 5. 下载/准备 eSpeak
if not exist "espeak" (
    echo [INFO] 请手动下载 Windows eSpeak 并解压到 espeak 目录
    echo        来源: https://sourceforge.net/projects/espeak/files/espeak/
    echo        需要包含: espeak.exe, libespeak.dll, espeak-data/
    pause
    if not exist "espeak" (
        echo [ERROR] espeak 目录不存在
        exit /b 1
    )
) else (
    echo [INFO] eSpeak 已存在
)

REM 6. 运行 PyInstaller
echo [INFO] 运行 PyInstaller ...
pyinstaller align.spec --clean --noconfirm
if errorlevel 1 (
    echo [ERROR] PyInstaller 构建失败
    exit /b 1
)

echo [OK] 构建完成: dist\align.exe
echo [INFO] 提示: 如果不需要单文件，可改用目录模式以加快启动速度。

endlocal
