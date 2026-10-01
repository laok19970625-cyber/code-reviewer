"""代码审查单元测试。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from reviewer import LLMClient, review_code  # noqa: E402


class FakeLLM(LLMClient):
    def chat(self, messages, temperature=0.2):
        return "[审查报告] " + messages[-1]["content"][:30]


class TestReviewer(unittest.TestCase):
    def test_review_code(self):
        r = review_code("def f():\n    return 1/0\n", FakeLLM())
        self.assertIn("[审查报告]", r)


if __name__ == "__main__":
    unittest.main(verbosity=2)
