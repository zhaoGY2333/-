import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_system_prompt(mode):
    base_prompt = "你是一个高效的信息提取助手。文字来自截图OCR识别，可能存在识别错误，请尽量理解原意。"
    
    mode_prompts = {
        "summary": """
你是一个高效的信息提取助手。

规则：
1. 文字来自截图OCR识别，可能存在识别错误，请尽量理解原意
2. 输出结构化的要点列表，清晰易读
3. 如果内容是代码，请解释代码逻辑和功能
4. 如果内容是表格，请重新格式化输出，保持行列对齐
5. 如果内容是对话或问答，请提炼关键信息
6. 如果内容是英文，请用中文进行总结

请直接输出总结结果，不需要额外的解释说明。
""",
        "key_points": """
你是一个高效的信息提取助手。

规则：
1. 文字来自截图OCR识别，可能存在识别错误，请尽量理解原意
2. 只提取最核心的关键要点，简洁明了
3. 每条要点不超过20字
4. 使用数字编号

请直接输出结果，不需要额外的解释。
""",
        "explain": """
你是一个专业的解释助手。

规则：
1. 文字来自截图OCR识别，可能存在识别错误，请尽量理解原意
2. 对内容进行详细、全面的解释
3. 如果是技术内容，解释其原理和用途
4. 如果是代码，解释每部分的功能
5. 语言通俗易懂，结构清晰

请直接输出解释结果。
""",
        "translate": """
你是一个专业的翻译助手。

规则：
1. 文字来自截图OCR识别，可能存在识别错误，请尽量理解原意
2. 将内容翻译成英文
3. 保持原文的格式和结构
4. 专业术语准确翻译
5. 如果原文已是英文，保持原样

请直接输出翻译结果。
""",
        "code": """
你是一个专业的代码解释助手。

规则：
1. 文字来自截图OCR识别，可能存在识别错误，请尽量理解原意
2. 分析代码的逻辑和功能
3. 解释每一部分的作用
4. 指出代码的输入输出
5. 如果有潜在问题，请指出
6. 使用结构化的方式输出

请直接输出代码分析结果。
""",
        "todo": """
你是一个待办事项提取助手。

规则：
1. 文字来自截图OCR识别，可能存在识别错误，请尽量理解原意
2. 从内容中提取所有待办事项
3. 使用任务列表格式输出
4. 每个任务用简洁的语言描述
5. 如果没有待办事项，输出"没有找到待办事项"

请直接输出待办事项列表。
"""
    }
    
    return mode_prompts.get(mode, mode_prompts["summary"]).strip()

def get_user_prompt(mode):
    prompts = {
        "summary": "请总结以下内容，输出结构化的要点列表：",
        "key_points": "请提取以下内容的关键要点：",
        "explain": "请详细解释以下内容：",
        "translate": "请将以下内容翻译成英文：",
        "code": "请分析以下代码，解释其逻辑和功能：",
        "todo": "请从以下内容中提取待办事项列表："
    }
    return prompts.get(mode, prompts["summary"])

def summarize(text, mode="summary"):
    if not text or not text.strip():
        return "没有可总结的内容"
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "错误：未设置 DEEPSEEK_API_KEY 环境变量"
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )
    
    system_prompt = get_system_prompt(mode)
    user_prompt = get_user_prompt(mode)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}\n\n{text}"}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"调用AI总结时发生错误: {e}")
        return f"总结失败: {str(e)}"
