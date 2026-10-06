"""GUIDE Phần 3 - Người tuyển chọn skill (skill curator): tự viết skill từ các lần chạy thất bại.   >>> SINH VIÊN CÀI ĐẶT curate_skills <<<

Pseudo-code: guides/pseudocode/04_curator.md
Kiểm tra:    pytest tests/test_04_curator.py
Chạy thật:   python -m lab.curator
"""
import json
import re
from pathlib import Path

from .model import make_model
from .tasks import ROOT, eval_markers   # có sẵn: định danh của tác vụ đánh giá, tính lúc chạy

# ---- CÓ SẴN, KHÔNG SỬA: kiểm tra và tách khối skill (phần dễ sai và liên quan bảo mật) ----------------
SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(text: str, expected_name: str | None = None) -> list[str]:
    """Kiểm tra nội dung một SKILL.md. Trả về danh sách vấn đề (rỗng = hợp lệ).

    Quy tắc: có khối YAML frontmatter; `name` chữ thường/số/gạch ngang (tối đa 64 ký tự) và bằng `expected_name`
    nếu được truyền; có `description` (tối đa 1024 ký tự); phần thân tối đa 80 dòng; không chứa chuỗi nào của
    `eval_markers()`. Quy tắc về `name` cũng là biện pháp bảo mật: tên khối do LLM sinh ra được dùng để tạo
    đường dẫn, nên `../evil` không được lọt qua.
    """
    problems = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.strip() + "\n", re.S)
    if not m:
        return ["missing YAML frontmatter"]
    front, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    n = name.group(1).strip() if name else ""
    if not SAFE_NAME.fullmatch(n) or len(n) > 64:
        problems.append("invalid name")
    elif expected_name is not None and n != expected_name:
        problems.append("name differs from the block name")
    if not desc or len(desc.group(1).strip()) > 1024:
        problems.append("missing or too long description")
    if len(body.strip().splitlines()) > 80:
        problems.append("body longer than 80 lines")
    low = text.lower()
    for marker in eval_markers():
        if marker in low:
            problems.append(f"mentions evaluation material: {marker}")
    return problems


def parse_skill_blocks(reply: str) -> list[tuple[str, str]]:
    """Tách câu trả lời của LLM thành danh sách (name, nội dung SKILL.md).

    Khuôn dạng: `=== SKILL: <name> ===` ... `=== END ===`. Một khối kết thúc ở điểm nào đến trước trong ba điểm:
    `=== END ===`, tiêu đề `=== SKILL:` kế tiếp, hoặc cuối văn bản (LLM đôi khi quên dòng END).
    """
    pattern = re.compile(r"^=== SKILL: (\S+) ===[ \t]*\n(.*?)(?=^=== END ===|^=== SKILL: |\Z)", re.S | re.M)
    return [(name, text.strip()) for name, text in pattern.findall(str(reply))]
# --------------------------------------------------------------------------------------------------


def curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]:
    """Đọc các lần chạy của TÁC VỤ HỌC (role == "learn") trong `source_condition`, nhờ LLM viết skill, ghi file.

    Các bước: nạp run.json + trace.md -> (nếu không có check nào thất bại: in cảnh báo và trả về [] mà KHÔNG gọi LLM)
    -> dựng prompt -> model.invoke(prompt) -> parse_skill_blocks -> validate_skill(text, expected_name=name)
    -> ghi `<out_dir>/<name>/SKILL.md`. Mặc định `out_dir` = <gốc lab>/skills/auto (dùng `ROOT` từ lab.tasks).
    Giữ tối đa `max_skills` skill hợp lệ; skill không hợp lệ bị bỏ qua.
    Prompt chứa, với mỗi check thất bại, TÊN và trường `detail` (lời nhận xét của bot đánh giá: phát biểu quy tắc bị vi phạm)
    cùng phần cuối của vết (trace). Với tác vụ học, `detail` chỉ phát biểu quy tắc, không chứa đáp án.
    Tuyệt đối KHÔNG đưa dữ liệu của tác vụ đánh giá (role == "eval") vào prompt.
    model mặc định: make_model() (lab.model).
    Trả về: danh sách đường dẫn SKILL.md đã ghi.
    """
    output_dir = Path(out_dir) if out_dir is not None else ROOT / "skills" / "auto"
    runs = []
    for run_path in sorted((Path(results_dir) / source_condition).glob("*/run.json")):
        try:
            run = json.loads(run_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if run.get("role") != "learn":
            continue
        failed = [
            (check.get("name", "unnamed check"), check.get("detail", ""))
            for check in run.get("checks", [])
            if not check.get("passed", False)
        ]
        trace_path = run_path.with_name("trace.md")
        try:
            trace = trace_path.read_text(encoding="utf-8")[-6000:]
        except OSError:
            trace = ""
        runs.append((run.get("task", run_path.parent.name), failed, trace))

    if not any(failed for _, failed, _ in runs):
        print("warning: không có check thất bại ở tác vụ học")
        return []

    evidence = []
    for task, failed, trace in runs:
        if not failed:
            continue
        check_text = "\n".join(f"- {name}: {detail}" for name, detail in failed)
        evidence.append(f"TASK: {task}\nFAILED CHECKS:\n{check_text}\nTRACE (tail):\n{trace}")
    prompt = f"""You write reusable SKILL.md files for a programming and data-analysis agent.
Below are failed checks, grader feedback, and execution traces from learning tasks only. Infer general process failures, not task-specific answers. Write at most {max_skills} short skills that help on new tasks.

Rules:
- Do not mention task IDs, task-specific file names, answers, or numbers from the evidence.
- Write exactly three complementary skills when the evidence supports code, tabular-data, and log work: one per family.
- Each skill description must say to use it at the beginning and again before completion of its task family. Make the trigger concrete enough that an agent can select it from the task instruction alone.
- The code skill must include a final contract audit for documentation, tests, public-function annotations, and change records when present.
- The tabular-data skill must include a final contract audit for output schema, metadata, normalized values, and required companion files when present.
- The log skill must include a final contract audit for JSON schema, metadata, normalized fields, ordering, and aggregate counts when present.
- Each skill needs YAML frontmatter with a lower-case hyphenated name and a one-sentence description saying when to use it.
- Keep each imperative checklist under 15 lines and prefer verification steps over long procedural explanations.
- Output every skill exactly in this format:
=== SKILL: <name> ===
---
name: <name>
description: <when to use it>
---
<instructions>
=== END ===

LEARNING-RUN EVIDENCE:
{"\n\n".join(evidence)}
"""
    chosen_model = model if model is not None else make_model()
    reply = chosen_model.invoke(prompt).content
    written = []
    for name, text in parse_skill_blocks(str(reply)):
        if len(written) >= max_skills or validate_skill(text, expected_name=name):
            continue
        path = output_dir / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
        written.append(path)
    return written


if __name__ == "__main__":
    for p in curate_skills():
        print("wrote", p)
