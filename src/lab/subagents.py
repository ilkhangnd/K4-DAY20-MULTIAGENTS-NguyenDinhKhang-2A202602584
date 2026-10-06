"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": "Use when you need to inspect task instructions, documentation, files, or data and report relevant facts before making a change.",
            "system_prompt": (
                "You are an exploration subagent. Read the requested files carefully, identify requirements, "
                "constraints, and relevant edge cases, then return a concise evidence-based report. Do not modify files."
            ),
        },
        {
            "name": "implementer",
            "description": "Use when a well-scoped implementation or repair is needed and the main agent needs a worker to make the change and verify it.",
            "system_prompt": (
                "You are an implementation subagent. Make only the requested changes, run an appropriate verification, "
                "and report the files changed plus the verification result. Do not claim success without checking it."
            ),
        },
        {
            "name": "reviewer",
            "description": "Use when an independent review is needed to verify requirements, outputs, tests, or edge cases before the main agent finishes.",
            "system_prompt": (
                "You are a review subagent. Independently inspect the requested result against the stated requirements, "
                "look for omissions and edge cases, and return findings with concrete evidence. Do not modify files."
            ),
        },
    ]
