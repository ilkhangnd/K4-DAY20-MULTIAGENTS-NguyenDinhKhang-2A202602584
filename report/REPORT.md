# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| | | |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `openai:gpt-4.1-mini`, `0`, `60`.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`; macOS Darwin 27.2.0 arm64; chạy trực tiếp trong `.venv`.
- Số lần chạy tác vụ đã dùng / ngân sách: 9 lượt task học (3 điều kiện × 3 task); ngân sách API không được cung cấp.
- Commit của tag `freeze`:

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): Dự đoán `subagents` không tăng điểm trung bình trên evaluation so với `baseline`, nhưng tăng token. Ở task học, nó đạt 8/27 so với 13/27 của baseline và dùng 126,769 so với 103,304 token; chỉ một trong ba task có lời gọi subagent, nên chi phí điều phối chưa tạo được lợi ích nhất quán.
- H2 (skills-auto so với baseline): Dự đoán `skills-auto` không cải thiện đáng kể evaluation so với `baseline`. Trên task học, hai điều kiện đều đạt 13/27, trong khi cả ba lượt `skills-auto` đều có `skills_read = 0`; vì vậy skill được nạp nhưng chưa có bằng chứng là đã đi vào ngữ cảnh thực thi. Điều này phù hợp với lưu ý trong GUIDE rằng skill tự sinh có thể không chuyển giao sang tác vụ mới.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán điểm evaluation có thể khác và có độ dao động lớn so với task học, vì mỗi task/cấu hình chỉ chạy một lần và evaluation chứa những yêu cầu mới. Do đó không suy diễn hiệu quả tổng quát chỉ từ điểm học; sẽ tách check kỹ thuật và check quy ước trong phân tích sau freeze.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Ở cấu hình Deep Agents mặc định, lab có hai **vai trò** tác tử: (i) tác tử chính đóng vai trò điều phối, đọc yêu cầu, lập kế hoạch và trực tiếp dùng tool để hoàn thành tác vụ; (ii) subagent `general-purpose`, được tạo tạm thời khi tác tử chính cần giao một việc phức tạp hoặc nhiều bước như tìm tệp, nghiên cứu nội dung hoặc xử lý một phần việc độc lập. Vì subagent chỉ được khởi tạo khi gọi tool `task`, số agent chạy thực tế không cố định. Sau Phần 1.1, điều kiện `subagents` sẽ bổ sung các subagent chuyên biệt do nhóm định nghĩa; chúng chưa có trong tour mặc định.

2. Tác tử chính giao việc qua tool `task`: chọn `subagent_type` (mặc định là `general-purpose`) và gửi một prompt mô tả đầy đủ việc cần làm cùng định dạng kết quả mong muốn. Mỗi lần gọi là một subagent stateless: nó chỉ thấy prompt được giao, tự dùng tool để xử lý, rồi trả về một báo cáo cuối cho tác tử chính. Báo cáo này không tự hiển thị cho người dùng; tác tử chính phải đọc, kiểm chứng khi cần và tổng hợp/trả lời tiếp. Các việc độc lập có thể được giao đồng thời.

3. Các tool hiện có gồm `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute` và `task`. Nhóm tool tệp cho phép xem, tìm kiếm và sửa nội dung trong sandbox; `execute` chạy lệnh shell trong sandbox và trả về stdout/stderr cùng mã thoát; `task` dùng để gọi subagent. Mô tả của `general-purpose` cho biết nó có quyền dùng toàn bộ tool như tác tử chính, nên hai vai trò chia sẻ cùng khả năng thao tác tệp và shell. System prompt mặc định của Deep Agents là rỗng; hành vi được định hướng chủ yếu bởi mô tả của các tool. Ví dụ, `task` yêu cầu cung cấp đầy đủ chi tiết và kết quả cần trả về, còn `execute` yêu cầu dùng đường dẫn tuyệt đối và tránh `find`/`grep` trong shell, thay bằng các tool chuyên dụng.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| | | | |

Nhận xét: nhóm lỗi nào chiếm đa số? Skill có thể phòng ngừa nhóm đó không?

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế):
- `subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0):
- Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc):
- Ảnh hưởng đến token và thời gian:

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do:

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| | | | |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
