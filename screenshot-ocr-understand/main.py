import argparse
import pyperclip
from utils import screenshot, save_history
from ocr import process_image
from ai_summary import summarize

def main():
    parser = argparse.ArgumentParser(description="截图OCR识别与AI总结工具")
    parser.add_argument("--delay", type=int, default=3, help="截图延迟秒数")
    parser.add_argument("--mode", type=str, default="summary", 
                        choices=["summary", "translate", "key_points", "explain", "code", "todo"],
                        help="分析模式: summary(总结), translate(翻译), key_points(提取要点), explain(详细解释), code(代码分析), todo(待办提取)")
    args = parser.parse_args()
    
    print("="*60)
    print("       截图OCR识别与AI总结工具")
    print("="*60)
    print(f"模式: {args.mode}")
    print(f"截图延迟: {args.delay}秒")
    print("="*60)
    
    print("\n[1/4] 准备截图...")
    image_path = screenshot(delay=args.delay)
    
    print("\n[2/4] 正在识别文字...")
    text = process_image(image_path)
    
    if not text:
        print("未能识别到文字，程序退出")
        return
    
    print("\n[3/4] 识别结果:")
    print("-" * 60)
    print(text)
    print("-" * 60)
    
    print("\n[4/4] 正在生成AI总结...")
    summary_text = summarize(text, mode=args.mode)
    print("\nAI分析结果:")
    print("-" * 60)
    print(summary_text)
    print("-" * 60)
    
    # 保存历史记录
    print("\n[保存历史记录]")
    save_history(text, summary_text, mode=args.mode)
    
    while True:
        choice = input("\n是否复制结果到剪贴板? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            break
        print("请输入 y 或 n")
    
    if choice == 'y':
        pyperclip.copy(summary_text)
        print("已复制到剪贴板!")
    
    print("\n" + "="*60)
    print("                     完成")
    print("="*60)

if __name__ == "__main__":
    main()
