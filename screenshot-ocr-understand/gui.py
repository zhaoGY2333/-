import tkinter as tk
import pyperclip
import traceback
import os
import subprocess
from utils import save_history
from ocr import process_image
from ai_summary import summarize


def main():
    root = tk.Tk()
    root.title("截图OCR识别与AI总结")
    root.geometry("900x750")
    
    mode_map = {
        "总结": "summary",
        "翻译": "translate", 
        "要点": "key_points",
        "详细解释": "explain",
        "代码分析": "code",
        "待办提取": "todo"
    }
    
    top_frame = tk.Frame(root, padx=10, pady=10)
    top_frame.pack(fill=tk.X)
    
    tk.Label(top_frame, text="分析模式：").pack(side=tk.LEFT)
    mode_var = tk.StringVar(value="总结")
    mode_menu = tk.OptionMenu(top_frame, mode_var, *mode_map.keys())
    mode_menu.pack(side=tk.LEFT, padx=10)
    
    status_label = tk.Label(top_frame, text="就绪", fg="blue", font=("Arial", 12))
    status_label.pack(side=tk.RIGHT)
    
    def update_status(text):
        status_label.config(text=text)
        root.update()
        print(f"[STATUS] {text}")
    
    info_label = tk.Label(root, text="点击下方按钮开始截图", bg="#F5F5F5", font=("Arial", 14), height=5)
    info_label.pack(fill=tk.X, padx=10, pady=5)
    
    btn_frame = tk.Frame(root, padx=10, pady=10)
    btn_frame.pack(fill=tk.X)
    
    analyze_btn = tk.Button(btn_frame, text="📸 选择截图区域", width=18, height=2, 
                           bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
    analyze_btn.pack(side=tk.LEFT, padx=10)
    
    copy_btn = tk.Button(btn_frame, text="📋 复制结果", width=15, height=2,
                        bg="#2196F3", fg="white", font=("Arial", 11, "bold"))
    copy_btn.pack(side=tk.LEFT)
    
    tk.Label(root, text="📝 OCR识别结果", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,0))
    ocr_text = tk.Text(root, height=12, wrap=tk.WORD, font=("Arial", 11))
    ocr_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    ocr_text.insert(tk.END, "OCR识别结果将显示在这里...")
    
    tk.Label(root, text="🤖 AI总结结果", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,0))
    ai_text = tk.Text(root, height=12, wrap=tk.WORD, font=("Arial", 11))
    ai_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    ai_text.insert(tk.END, "AI总结结果将显示在这里...")
    
    def update_info(text, bg_color="#F5F5F5"):
        info_label.config(text=text, bg=bg_color)
        root.update()
    
    def run_analysis():
        try:
            update_status("准备截图...")
            update_info("点击按钮后，使用 Command+Shift+4 快捷键框选区域，\n然后选择保存到桌面，再回来点击确认！", bg_color="#FFF3CD")
            
            # 先让用户用系统快捷键截图保存到桌面
            update_status("请按 Command+Shift+4 截图保存到桌面")
            update_info("请现在按 Command+Shift+4 框选并截图，\n保存到桌面后，点击下方按钮继续！", bg_color="#FFF3CD")
            
            # 创建一个临时确认窗口
            confirm_win = tk.Toplevel(root)
            confirm_win.title("截图确认")
            confirm_win.geometry("400x200")
            
            tk.Label(confirm_win, text="截图完成了吗？", font=("Arial", 14)).pack(pady=20)
            
            def confirm_screenshot():
                confirm_win.destroy()
                process_saved_screenshot()
            
            tk.Button(confirm_win, text="✓ 已截图，继续", command=confirm_screenshot,
                     bg="#4CAF50", fg="white", font=("Arial", 12), height=2, width=20).pack(pady=10)
            
            def cancel_screenshot():
                confirm_win.destroy()
                update_status("已取消")
                update_info("点击下方按钮重新开始", bg_color="#F8D7DA")
            
            tk.Button(confirm_win, text="取消", command=cancel_screenshot,
                     bg="#999999", fg="white", font=("Arial", 12), width=20).pack(pady=5)
            
        except Exception as e:
            update_status(f"错误: {str(e)}")
            update_info(f"发生错误: {str(e)}", bg_color="#F8D7DA")
            print(f"[DEBUG] ERROR: {e}")
            traceback.print_exc()
    
    def process_saved_screenshot():
        try:
            # 查找桌面上最新的截图
            desktop = os.path.expanduser("~/Desktop")
            if not os.path.exists(desktop):
                update_info("找不到桌面文件夹！", bg_color="#F8D7DA")
                return
            
            # 查找最近的截图文件
            screenshot_files = []
            for filename in os.listdir(desktop):
                if filename.startswith("屏幕截图") or filename.startswith("Screenshot"):
                    filepath = os.path.join(desktop, filename)
                    if os.path.isfile(filepath):
                        screenshot_files.append((os.path.getmtime(filepath), filepath))
            
            if not screenshot_files:
                update_info("在桌面找不到截图！请确保截图保存到了桌面。", bg_color="#F8D7DA")
                return
            
            # 找到最新的截图
            screenshot_files.sort(reverse=True, key=lambda x: x[0])
            latest_time, image_path = screenshot_files[0]
            
            file_size = os.path.getsize(image_path)
            update_info(f"找到截图！\n文件: {os.path.basename(image_path)}\n大小: {file_size} 字节", bg_color="#D4EDDA")
            print(f"[DEBUG] 使用图片: {image_path}")
            
            update_status("识别中...")
            ocr_result = process_image(image_path)
            
            if not ocr_result:
                update_status("未识别到文字")
                return
            
            ocr_text.delete(1.0, tk.END)
            ocr_text.insert(tk.END, ocr_result)
            root.update()
            
            mode = mode_map[mode_var.get()]
            update_status("AI总结中...")
            ai_result = summarize(ocr_result, mode=mode)
            
            ai_text.delete(1.0, tk.END)
            ai_text.insert(tk.END, ai_result)
            root.update()
            
            save_history(ocr_result, ai_result, mode=mode)
            update_status("完成")
            
        except Exception as e:
            update_status(f"错误: {str(e)}")
            update_info(f"发生错误: {str(e)}", bg_color="#F8D7DA")
            print(f"[DEBUG] ERROR: {e}")
            traceback.print_exc()
    
    def copy_result():
        content = ai_text.get(1.0, tk.END).strip()
        if content and content != "AI总结结果将显示在这里...":
            pyperclip.copy(content)
            update_status("已复制到剪贴板")
        else:
            update_status("没有内容可复制")
    
    analyze_btn.config(command=run_analysis)
    copy_btn.config(command=copy_result)
    
    root.mainloop()


if __name__ == "__main__":
    main()
