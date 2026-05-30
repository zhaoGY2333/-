import os
import sys
import time
import keyboard
from utils import screenshot, save_history
from ocr import process_image
from ai_summary import summarize


def perform_analysis():
    """执行完整的分析流程"""
    try:
        print("\n📸 准备截图...")
        image_path = screenshot(delay=2)
        
        print("🔍 正在识别文字...")
        ocr_result = process_image(image_path)
        
        if not ocr_result:
            print("❌ 未能识别到文字")
            return
        
        print("💬 识别结果:\n" + "-"*50)
        print(ocr_result)
        print("-"*50)
        
        print("🤖 正在生成AI总结...")
        ai_result = summarize(ocr_result, mode="summary")
        
        print("\n✨ AI总结:\n" + "-"*50)
        print(ai_result)
        print("-"*50)
        
        # 保存历史记录
        save_history(ocr_result, ai_result, mode="summary")
        
        print("✅ 分析完成！结果已保存到历史记录")
        
    except Exception as e:
        print(f"❌ 分析出错: {str(e)}")


def main():
    print("="*60)
    print("           截图OCR识别与AI总结 - 全局快捷键模式")
    print("="*60)
    print("📌 按 F13 快速启动截图分析")
    print("📌 按 Ctrl+C 退出程序")
    print("="*60 + "\n")
    
    # 检查是否以 root 权限运行
    if os.getuid() != 0:
        print("⚠️  提示：全局快捷键功能在 macOS 上需要管理员权限")
        print("    keyboard 库需要特殊权限才能监听全局键盘事件")
        print("\n推荐使用以下替代方案：")
        print("  1. GUI 界面：`python3 gui.py`")
        print("  2. 命令行模式：`python3 main.py`")
        print("\n如仍需使用快捷键功能，请使用 sudo 运行：")
        print("  sudo python3 hotkey.py")
        print("\n（但 macOS 的系统完整性保护可能阻止此操作）")
        return
    
    # 注册全局快捷键 - 使用 F13 (通常未被占用)
    try:
        keyboard.add_hotkey('f13', perform_analysis)
        print("✅ 快捷键已注册，等待按下 F13...\n")
        
        # 保持程序运行
        keyboard.wait()
        
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except PermissionError:
        print("\n❌ 权限不足：keyboard 库在 macOS 上需要特殊权限")
        print("\n推荐使用以下替代方案：")
        print("  1. GUI 界面：`python3 gui.py`")
        print("  2. 命令行模式：`python3 main.py`")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        print("\nkeyboard 库在 macOS 上可能存在兼容性问题")
        print("建议使用 GUI 界面：`python3 gui.py`")
        print("或命令行模式：`python3 main.py`")


if __name__ == "__main__":
    main()
