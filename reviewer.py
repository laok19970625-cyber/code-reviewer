"""AI 代码审查助手：读入代码 -> LLM 提出改进建议（bug / 性能 / 可读性 / 安全）。"""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path


class LLMClient:
    def __init__(self, api_key=None, api_base=None, model=None):
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.api_base = (api_base or os.environ.get("LLM_API_BASE", "https://open.bigmodel.cn/api/paas/v4")).rstrip("/")
        self.model = model or os.environ.get("LLM_MODEL", "glm-4-flash")

    def chat(self, messages, temperature=0.2):
        if not self.api_key:
            raise RuntimeError("未配置 LLM_API_KEY，请设置环境变量后重试。")
        url = f"{self.api_base}/chat/completions"
        payload = {"model": self.model, "messages": messages, "temperature": temperature}
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]


REVIEW_PROMPT = (
    "你是一名资深软件工程师，请审查下面的代码，按优先级输出：\n"
    "1) 🔴 严重问题（bug、安全隐患、资源泄漏）\n"
    "2) 🟡 改进建议（性能、可读性、可维护性）\n"
    "3) 🟢 亮点\n"
    "每个问题请标注大致位置并给出修改建议。用中文，直接、具体。"
)


def review_code(code: str, llm: LLMClient | None = None) -> str:
    llm = llm or LLMClient()
    messages = [
        {"role": "system", "content": REVIEW_PROMPT},
        {"role": "user", "content": f"```\n{code}\n```"},
    ]
    return llm.chat(messages)


def review_file(path: str, llm: LLMClient | None = None) -> str:
    code = Path(path).read_text(encoding="utf-8")
    return review_code(code, llm)
