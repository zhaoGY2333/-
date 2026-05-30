# 截图OCR识别与AI总结工具

一个功能强大的截图、OCR识别和AI总结工具，支持多种分析模式和GUI界面。

## 功能特点

- 📸 一键截图功能
- 📝 OCR文字识别（支持中英文）
- 🤖 AI智能分析（基于DeepSeek）
- 🎨 友好的GUI界面
- ⌨️ 全局快捷键快速启动
- 📋 结果一键复制
- 💾 历史记录保存
- 🔌 命令行接口

## 支持的分析模式

1. **总结** - 对内容进行概括性总结
2. **翻译** - 将内容翻译成英文
3. **要点** - 提取关键要点
4. **详细解释** - 对内容进行详细讲解
5. **代码分析** - 分析和解释代码
6. **待办提取** - 从文本中提取待办事项列表

## 安装步骤

### 1. 系统要求

- macOS 10.15+
- Python 3.8+
- Tesseract OCR

### 2. 安装Tesseract

```bash
# 使用 Homebrew 安装
brew install tesseract tesseract-lang
```

### 3. 安装Python依赖

```bash
cd /path/to/screenshot-ocr-understand
pip3 install -r requirements.txt
```

### 4. 配置API Key

复制 `.env` 文件（如果不存在则创建），填入你的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

获取API Key：https://platform.deepseek.com/

## 使用方法

### 方法一：使用GUI界面

```bash
python3 gui.py
```

点击"截图分析"按钮，3秒后自动截图并进行OCR识别和AI总结。

### 方法二：使用命令行

```bash
# 基本使用（使用默认模式）
python3 main.py

# 指定分析模式
python3 main.py --mode summary
python3 main.py --mode code
python3 main.py --mode todo

# 自定义截图延迟时间
python3 main.py --delay 5
```

### 方法三：全局快捷键

```bash
python3 hotkey.py
```

按下 `Ctrl+Shift+A` 快捷键快速启动截图分析（默认分析模式为"总结"）。

> 提示：
> - 如果快捷键无法使用，请尝试以管理员/root权限运行
> - 按 `Ctrl+C` 可退出快捷键程序

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--delay` | int | 3 | 截图延迟时间（秒） |
| `--mode` | string | summary | 分析模式 |

## 分析模式详解

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `summary` | 概括性总结 | 一般文档、网页内容 |
| `translate` | 翻译成英文 | 英文资料翻译 |
| `key_points` | 提取关键要点 | 会议记录、学习笔记 |
| `explain` | 详细解释 | 技术文档、概念解析 |
| `code` | 代码分析 | 代码片段理解 |
| `todo` | 待办提取 | 任务清单、待办列表 |

## 项目结构

```
screenshot-ocr-understand/
├── main.py            # 命令行主程序
├── gui.py             # GUI界面程序
├── hotkey.py          # 全局快捷键程序
├── utils.py           # 工具函数（截图、历史记录）
├── ocr.py             # OCR识别功能
├── ai_summary.py      # AI总结功能
├── requirements.txt   # Python依赖
├── .env               # 环境变量配置
├── .gitignore         # Git忽略文件
├── README.md          # 项目文档
├── temp.png           # 临时截图文件（自动生成）
└── history.txt        # 历史记录文件（自动生成）
```

## 依赖说明

| 依赖库 | 用途 |
|--------|------|
| tkinter | GUI界面 |
| pytesseract | OCR文字识别 |
| Pillow | 图像处理 |
| openai | AI API调用 |
| python-dotenv | 环境变量管理 |
| pyperclip | 剪贴板操作 |
| keyboard | 全局快捷键监听 |

## 常见问题

### 1. OCR识别不准确？

- 确保截图清晰，对比度高
- 可以尝试修改 `ocr.py` 中的预处理参数
- 使用放大截图功能提高小字识别率

### 2. AI响应失败？

- 检查网络连接
- 确认API Key有效
- 检查 `.env` 文件格式是否正确

### 3. 截图失败？

- 为终端授予屏幕录制权限（系统设置 → 隐私与安全性 → 屏幕录制）
- 重启终端后重试

## 开发者

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
