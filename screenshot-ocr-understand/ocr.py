import pytesseract
import os
from PIL import Image

def preprocess_image(image_path):
    """图片预处理：灰度化 + 放大2倍"""
    temp_path = "temp_preprocessed.png"
    img = Image.open(image_path)
    # 转为灰度图
    img_gray = img.convert('L')
    # 放大2倍
    width, height = img_gray.size
    img_resized = img_gray.resize((width * 2, height * 2), Image.LANCZOS)
    # 保存临时文件
    img_resized.save(temp_path)
    return temp_path

def recognize_text(image_path, lang='chi_sim+eng'):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    img = Image.open(image_path)
    # 使用中英文混合识别
    text = pytesseract.image_to_string(img, lang=lang)
    return text

def process_image(image_path):
    try:
        # 预处理图片
        processed_path = preprocess_image(image_path)
        
        # 识别文字
        text = recognize_text(processed_path, lang='chi_sim+eng')
        
        # 清理临时文件
        if os.path.exists(processed_path) and processed_path != image_path:
            os.remove(processed_path)
        
        if not text or not text.strip():
            print("未识别到任何文字")
            return ""
        
        # 清理多余空白
        text = text.strip()
        return text
    
    except Exception as e:
        print(f"处理图片时发生错误: {e}")
        return ""