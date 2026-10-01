# AI 代码审查助手

读入代码，自动识别严重问题（bug/安全/资源泄漏）、改进建议、亮点。

## 特性
- 按严重程度分级输出（🔴 严重 / 🟡 建议 / 🟢 亮点）
- 标注位置 + 给出修改方案

## 快速开始
```bash
export LLM_API_KEY="你的Key"
python main.py your_code.py
```

## 应用场景
- 代码提交前自检
- Code Review 辅助
- 代码质量提升

## License
MIT
