# Checklist Giai đoạn 2B1

Scope canonical: `../../decisions/20261009-phase2b1-approval.md`. Hồ sơ Phase1/2A bất biến. Các thử nghiệm âm/NaN dùng fixture QA riêng, không ghi vào dữ liệu sản phẩm.

| ID | Hạng mục | Nguồn chuẩn | Trạng thái | Evidence | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| B00 | Bootstrap, phê duyệt, source gate, môi trường và preservation | Attachment Thy, Phase2A run a | VERIFIED | verification.json37/37; pip check; preservation933 | Không cài thêm;68 runtime temp cũ ghi preflight |
| B01 | HGB fit Train, dự báo Validation đúng cấu hình | Decision 2B1 | VERIFIED | Run a2/b manifest/runtime/config; fit-witness.json | 22513 Train/11 feature, không Test |
| B02 | D09, timestamp, so baseline và metric độc lập | Phase2A Validation và D09 | VERIFIED | Decimal metrics37/37,4727 timestamp; fixture D09 | kWh, raw/final,0âm |
| B03 | Save/load và hợp đồng inference | Candidate mới | VERIFIED | Save/load0 chênh lệch, verifier tiến trình riêng | Chỉ nạp artifact tự tạo |
| B04 | Leakage, tái lập cùng cấu hình và bảo toàn nguồn | Train/hash/QA | VERIFIED | fit-witness/audit;4artifact a2/b byteidentical;933hash | Không thay tham số |
| B05 | Read-back tài liệu, handoff 8 mục và điểm dừng | Artifact cuối/decision | VERIFIED | documents-verification.json47/47;18MD đọc đủ/link/metric/hash;933file giữ nguyên | Chưa khóa model cuối, chờ Thy duyệt2B2 |
