# Checkpoint phát hành ứng dụng

Commit sản phẩm/QA: `853974cbf3d858efc2d4209c1ba1e60ffc1c650a`, push lên thy0805/bigdata main.

`remote-readback-1.json`: **9/9** = remote main khớp HEAD và tám file/ảnh trên raw GitHub giống Git blob. Snapshot scan trước commit:285file/index bằng disk,0finding theo các pattern đã kiểm. Đây không phải bảo đảm không tồn tại mọi loại bí mật có thể có.

Folder bàn giao GitHub: `Detaituan8910/.agent/qa/phase4-app-20261009/`. Đọc `review.md` trước, sau đó verification126/126, preservation1571/1571, các QA riêng và REPORT_EVIDENCE_MAP.md.

Gói local `Phase4_App_QA_20261009.zip`:46file có checksum,47ZIPentries,645825byte; SHA256 `c16745be8ec6229b4d69792f1a4cb295c2d470b192569ac0d566be647a5e5924`. Nội dung được chụp trước publication; context trong ZIP là snapshot tại đóng gói, context trên GitHub có thêm receipt sau push. ZIP không gồm raw,Office,fixture,runtime hoặc host-process inventory.

Checkpoint sau commit sản phẩm chỉ bổ sung điều phối/receipt và công cụ đọc lại GitHub; không thay code dashboard, dữ liệu, model hoặc QA đã kiểm. Receipt cuối `remote-readback.json` lưu local-only và phải khớp HEAD khi tra; không commit receipt tự chứa commit hiện hành để tránh vòng tự tham chiếu.

Git whitespace gate mặc định coi CRLF trong JSON Windows là trailing whitespace do `.gitattributes` giữ byte. Kiểm lại với `core.whitespace=cr-at-eol` đạt; không chuyển newline làm đổi hash evidence.

I01/I02/I03/I05 VERIFIED trong phạm vi đã kiểm; **I04 DEFERRED, toàn Phase4 INCOMPLETE**, nghiệm thu Thy/GPT Web PENDING. App localhost8501 và Flink localhost8081 chỉ ở máy Thy; không deploy website công khai, không coldboot/autostart hoặc Word/PPT/I04/Phase5.
