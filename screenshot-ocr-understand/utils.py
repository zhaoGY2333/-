import subprocess
import time
import os
from datetime import datetime

def screenshot(filename="temp.png", delay=3, region=None):
    if delay > 0:
        print(f"准备截图，{delay}秒后开始...")
        for i in range(delay, 0, -1):
            print(f"{i}...")
            time.sleep(1)
    
    filepath = os.path.abspath(filename)
    
    if region:
        x, y, width, height = region
        subprocess.run([
            "screencapture",
            "-R", f"{x},{y},{width},{height}",
            filepath
        ])
    else:
        subprocess.run(["screencapture", filepath])
    
    print(f"截图已保存到: {filepath}")
    
    return filepath

def interactive_screenshot(filename="temp.png"):
    """交互式框选截图，让用户用鼠标选择区域"""
    print("请用鼠标拖动选择要截图的区域...")
    print("提示：鼠标变成十字准星后，按住左键拖动选择区域，松开完成截图")
    filepath = os.path.abspath(filename)
    
    # 使用 macOS 系统的交互式截图命令 (-s 表示选择模式)
    try:
        result = subprocess.run(["screencapture", "-s", filepath])
        
        if result.returncode == 0 and os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            if file_size > 0:
                print(f"交互式截图成功，已保存到: {filepath}")
                return filepath
        
        print("截图已取消或失败")
        return None
    except Exception as e:
        print(f"截图出错: {e}")
        return None

def save_history(ocr_text, ai_summary, mode="summary"):
    """保存历史记录到 history.txt 文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_file = "history.txt"
    
    # 格式化内容，确保不会有换行符导致格式混乱
    ocr_text_clean = ocr_text.replace('\n', '\\n')
    ai_summary_clean = ai_summary.replace('\n', '\\n')
    
    line = f"{timestamp} | {mode} | {ocr_text_clean} | {ai_summary_clean}\n"
    
    # 追加写入
    try:
        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(line)
        print(f"历史记录已保存到: {os.path.abspath(history_file)}")
    except Exception as e:
        print(f"保存历史记录失败: {e}")

def read_history(limit=10):
    """读取最近的历史记录"""
    history_file = "history.txt"
    if not os.path.exists(history_file):
        return []
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 返回最近的 limit 条
        history = []
        for line in reversed(lines[-limit:]):
            parts = line.strip().split(' | ', 3)
            if len(parts) == 4:
                timestamp, mode, ocr_text, ai_summary = parts
                # 恢复换行符
                ocr_text = ocr_text.replace('\\n', '\n')
                ai_summary = ai_summary.replace('\\n', '\n')
                history.append({
                    'timestamp': timestamp,
                    'mode': mode,
                    'ocr_text': ocr_text,
                    'ai_summary': ai_summary
                })
        return history
    except Exception as e:
        print(f"读取历史记录失败: {e}")
        return []
