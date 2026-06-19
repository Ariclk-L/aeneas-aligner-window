#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeneas 音频-文本强制对齐工具
命令行: align.exe <audio_path> <text_path> [output_dir]
输出: 与音频同名的 .srt 和 .json 文件
"""

import os
import sys
import argparse
import chardet
from pathlib import Path


def get_resource_base_path():
    """获取资源文件基准路径（兼容 PyInstaller 和本地开发）"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 单文件运行时的临时目录
        return Path(sys._MEIPASS)
    else:
        # 本地开发：取脚本所在目录
        return Path(os.path.dirname(os.path.abspath(__file__)))


def setup_environment():
    """设置 FFmpeg 和 eSpeak 的 PATH"""
    base = get_resource_base_path()
    ffmpeg_bin = base / 'ffmpeg' / 'bin'
    espeak_bin = base / 'espeak'

    path_parts = [str(ffmpeg_bin), str(espeak_bin)]
    current_path = os.environ.get('PATH', '')
    if current_path:
        path_parts.append(current_path)
    os.environ['PATH'] = os.pathsep.join(path_parts)

    # 可选：设置 eSpeak 数据目录（如果打包时包含）
    espeak_data = espeak_bin / 'espeak-data'
    if espeak_data.exists():
        os.environ['ESPEAK_DATA_PATH'] = str(espeak_data)


def detect_and_convert_to_utf8(input_path, output_path=None):
    """检测文件编码并转换为 UTF-8"""
    with open(input_path, 'rb') as f:
        raw = f.read()
    detected = chardet.detect(raw)
    encoding = detected.get('encoding') or 'utf-8'
    confidence = detected.get('confidence', 0)
    print(f"[INFO] 检测到文本编码: {encoding} (置信度: {confidence:.2f})")

    try:
        text = raw.decode(encoding, errors='replace')
    except Exception:
        text = raw.decode('utf-8', errors='replace')

    if output_path is None:
        output_path = input_path
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return output_path


def run_alignment(audio_path, text_path, output_dir):
    """调用 aeneas 执行强制对齐"""
    from aeneas.executetask import ExecuteTask
    from aeneas.task import Task

    audio_path = Path(audio_path).resolve()
    text_path = Path(text_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = audio_path.stem
    srt_path = output_dir / f"{stem}.srt"
    json_path = output_dir / f"{stem}.json"

    # 统一文本编码为 UTF-8
    utf8_text = output_dir / f"{stem}_utf8.txt"
    detect_and_convert_to_utf8(str(text_path), str(utf8_text))

    # 生成 SRT
    srt_config = (
        "task_language=zho|"
        "os_task_file_format=srt|"
        "is_text_type=plain"
    )
    task_srt = Task(config_string=srt_config)
    task_srt.audio_file_path_absolute = str(audio_path)
    task_srt.text_file_path_absolute = str(utf8_text)
    task_srt.sync_map_file_path_absolute = str(srt_path)
    ExecuteTask(task_srt).execute()
    task_srt.output_sync_map_file()
    print(f"[OK] 已生成 SRT: {srt_path}")

    # 生成 JSON
    json_config = (
        "task_language=zho|"
        "os_task_file_format=json|"
        "is_text_type=plain"
    )
    task_json = Task(config_string=json_config)
    task_json.audio_file_path_absolute = str(audio_path)
    task_json.text_file_path_absolute = str(utf8_text)
    task_json.sync_map_file_path_absolute = str(json_path)
    ExecuteTask(task_json).execute()
    task_json.output_sync_map_file()
    print(f"[OK] 已生成 JSON: {json_path}")

    # 清理临时 UTF-8 文本
    try:
        utf8_text.unlink()
    except Exception:
        pass

    return srt_path, json_path


def main():
    parser = argparse.ArgumentParser(
        description="Aeneas 音频-文本强制对齐工具"
    )
    parser.add_argument("audio", help="音频文件路径（mp3/wav/aac 等）")
    parser.add_argument("text", help="已拆分文本文件路径（每行一个片段）")
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="输出目录（可选，默认与音频同目录）"
    )
    args = parser.parse_args()

    audio_path = Path(args.audio)
    text_path = Path(args.text)

    if not audio_path.exists():
        print(f"[ERROR] 音频文件不存在: {audio_path}", file=sys.stderr)
        sys.exit(1)
    if not text_path.exists():
        print(f"[ERROR] 文本文件不存在: {text_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else audio_path.parent

    # 设置环境（FFmpeg / eSpeak）
    setup_environment()

    try:
        run_alignment(str(audio_path), str(text_path), str(output_dir))
    except Exception as e:
        print(f"[ERROR] 对齐失败: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
