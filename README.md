# Aeneas Aligner（音频-文本强制对齐工具）

一个独立的 Windows 命令行工具，基于 [aeneas](https://www.readbeyond.it/aeneas/) 实现音频与文本的强制对齐。

## 功能

- 输入：音频文件 + 已拆分文本文件（每行一个片段）
- 输出：与音频同名的 `.srt` 字幕文件 + `.json` 时间戳文件
- 无需用户安装 Python、FFmpeg、eSpeak 等依赖

## 使用方式

```cmd
align.exe <audio_path> <text_path> [output_dir]
```

示例：

```cmd
align.exe "C:\audio.mp3" "C:\text.txt"
```

输出：
- `C:\audio.srt`
- `C:\audio.json`

## 文本格式要求

文本需按标点预先拆分，每行一个片段。例如：

```text
在黑格尔的所有著作中
没有哪一章比《精神现象学》里讨论「自我意识」的部分更引人注目
即便整本《精神现象学》都晦涩难懂
```

## Windows 本地构建

### 前置要求

- Windows 10/11
- Python 3.10+
- 网络连接（下载 FFmpeg、手动准备 eSpeak）

### 步骤

1. 克隆或解压本项目。
2. 编辑 `build.bat` 中的 eSpeak 下载地址（如果默认地址不可用）。
3. 双击或在 PowerShell 中运行：

```cmd
build.bat
```

4. 构建完成后，`dist\align.exe` 即为最终产物。

## GitHub Actions 自动构建

推送以 `v` 开头的 tag 即可触发构建，并自动发布 Release：

```bash
git tag v1.0.0
git push origin v1.0.0
```

构建产物也可在 Actions 的 Artifacts 中下载。

## 体积说明

由于打包了 Python 运行时、FFmpeg、eSpeak 和 aeneas C 扩展，最终 EXE 体积约为 **150-250 MB**。

## 已知限制

- 当前仅支持 Windows 单文件 EXE。
- 对齐质量依赖于文本拆分是否合理（需与音频内容严格对应）。
- 中文音频需使用 `task_language=zho`，目前代码已固定为中文。如需支持其他语言，可修改 `src/align.py` 中的 `task_language`。

## 许可证

本项目遵循 aeneas 的 AGPL v3 许可证。
