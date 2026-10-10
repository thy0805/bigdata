import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / 'Detaituan8910'
QA = PROJECT / '.agent/qa/word-w011-20261010'
SOURCE = PROJECT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
OUTPUT = PROJECT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((QA / name).read_text(encoding='utf-8-sig'))


def save(name, value):
    (QA / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


verification = read('verification.json')
probe = read('field-probe.json')
diff = read('page-diff.json')
changes = read('changes.json')
native = read('word-readback.json')
preservation = read('preservation.json')
assert digest(SOURCE) == '4a47523a0bfe9c2a035df66c9fedff2e33a776dcb8c2ec01b50be8dd0d33f591'
assert digest(OUTPUT) == 'fafe4d7485601ba667a468990c1c80e188bf0e7126dd3edaf51059dfca3e2006'
assert verification['passed'] == 37 and verification['total'] == 38
assert not [c for c in verification['checks'] if c['status'] == 'FAIL']
assert probe['status'] == 'PASS' and len(probe['checks']) == 9
assert len(changes) == 18 and native['pages'] == diff['page_count'] == 67
assert preservation['matching'] == 1568 and len(preservation['unreadable']) == 3

notes = {
    1: 'Bìa ngoài: khung, logo, danh sách và bố cục nguyên ảnh nguồn.',
    2: 'Bìa trong: khung, logo, giảng viên và danh sách nguyên ảnh nguồn.',
    10: 'Danh mục thuật ngữ nguyên W01; tên HGB vẫn ngắt trước “or” do cột hẹp. Điểm thẩm mỹ có sẵn, ngoài phạm vi sửa Bảng 5.1; không tự sửa trang đầu.',
    12: 'Danh mục bảng nhận caption Bảng 5.3 mới và số trang đúng.',
    43: 'Bảng 3.1: Giờ:phút: / giây xuống dòng theo cụm, không đổi đơn vị hay cỡ chữ.',
    44: 'Chú nguồn Bảng 3.2 văn phong báo cáo; đường bảng và số liệu đủ.',
    46: 'Chú nguồn Bảng 3.4 làm sạch; khung Hình 3.1 vẫn đen.',
    56: 'Bảng 5.1: HistGradient / BoostingRegressor tách camel-case, không cắt giữa từ.',
    59: 'Lời dẫn Hình 5.2 gọn; hai khung đen nguyên kích thước.',
    60: 'Chú nguồn Bảng 5.2 thay QA bằng kiểm thử trình duyệt; bảng nguyên số liệu.',
    62: '5.15 và Bảng 5.3: 119 chức năng/vận hành + 7 hồ sơ riêng; caption, dòng bảng, trang không tràn.',
    63: '5.16 dùng văn phong học thuật; giữ giới hạn chưa coldboot, chưa autostart và chưa kịch bản trình diễn.',
}
page_rows = []
for n in range(1, 68):
    path = QA / 'render' / f'page-{n:03d}.png'
    assert path.exists()
    page_rows.append({'page': n, 'review': 'PASS_NO_NEW_VISUAL_DEFECT',
                      'reviewed_individually': True, 'detail': 'original',
                      'changed_from_w01': n in diff['changed_pages'],
                      'sha256': digest(path),
                      'note': notes.get(n, 'Đã xem riêng: không thấy lỗi thị giác mới; đối chiếu page-diff.')})
visual = {'status': 'PASS_WITH_EXISTING_OUT_OF_SCOPE_COSMETIC_NOTE',
          'method': 'Native Word PDF export; PDFium scale 2; all 67 final PNGs individually viewed at original resolution.',
          'pages_reviewed': 67, 'changed_pages': diff['changed_pages'],
          'pixel_identical_pages': len(diff['identical_pages']),
          'new_defects': [], 'existing_out_of_scope': [{'page': 10, 'note': notes[10]}],
          'pages': page_rows}
save('visual-verification.json', visual)
lines = ['# Rà thị giác W01.1', '',
         'Đã xem riêng cả 67 PNG cuối ở độ phân giải gốc, không chỉ contact sheet. Native Word xuất PDF, PDFium render scale 2.', '',
         '9 trang thay đổi: ' + ', '.join(map(str, diff['changed_pages'])) + '. 58 trang còn lại giống pixel W01. Không có lỗi thị giác mới trong phạm vi sửa.', '',
         'Lưu ý có sẵn ngoài phạm vi: trang 10, tên HGB trong danh mục thuật ngữ ngắt trước “or”. Trang này giống pixel nguồn; giữ nguyên theo yêu cầu bảo toàn trang đầu. Không gọi toàn tài liệu “hoàn hảo” và không tự sửa lan.', '',
         '| Trang vật lý | So W01 | Kết quả xem riêng |', '| --- | --- | --- |']
lines += [f"| {p['page']} | {'Thay đổi' if p['changed_from_w01'] else 'Giống pixel'} | {p['note']} |" for p in page_rows]
(QA / 'page-review.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
lines = ['# Diff trước/sau W01.1', '',
         '18 sửa đúng whitelist: 11 nhánh văn bản, 5 ô nhãn Bảng 5.3, 2 chỗ ngắt dòng mềm. Không đổi giá trị số hoặc cỡ chữ. Nội dung field REF/SEQ/STYLEREF được giữ.', '',
         'Các đoạn có field chỉ liệt kê nhánh prose sửa, không phải toàn paragraph. `changes.json` là diff máy đọc được.', '']
for i, change in enumerate(changes, 1):
    lines += [f"## {i}. {change.get('location', change['kind'])}", '',
              'Trước:', '', '> ' + change['before'].replace('\n', ' ↵ '), '',
              'Sau:', '', '> ' + change['after'].replace('\n', ' ↵ '), '']
(QA / 'CHANGES.md').write_text('\n'.join(lines), encoding='utf-8')
summary = {'pages': native['pages'], 'tables': native['tables'], 'inline_shapes': native['inline_shapes'],
           'equations': native['equations'], 'toc_and_lists': native['toc'], 'covers': 2,
           'black_placeholders': 7, 'references': 21, 'caption_count': 23,
           'source_sha256': digest(SOURCE), 'output_sha256': digest(OUTPUT),
           'headings_and_captions_preserved': True, 'fulltext_published': False}
save('word-summary.json', summary)
final = {'word_status': 'VERIFIED', 'user_acceptance': 'PENDING_THY_GPT_WEB',
         'scope': 'W01.1 only; no W02, app, data, model, PPT or demo changes.',
         'structural_semantic': {'passed': 37, 'applicable_word_checks': 37, 'source': 'verification.json'},
         'raw_verification_status': 'INCOMPLETE', 'raw_verification_checks': {'pass': 37, 'incomplete': 1, 'fail': 0, 'total': 38},
         'live_field_probe': {'passed': 9, 'total': 9, 'artifact_unchanged': True},
         'visual': {'pages_reviewed': 67, 'changed_pages': diff['changed_pages'], 'identical_pages': 58, 'new_defects': 0,
                    'existing_out_of_scope_note': 'Page 10 glossary HGB wrapping; unchanged W01.'},
         'source_guards': {'matching': 37, 'total': 37},
         'historical_snapshot_preservation': preservation,
         'summary': summary, 'stop': 'Await Thy/GPT Web approval. W02 not authorized.'}
save('final-verification.json', final)
review = '''# Bàn giao W01.1 — sửa nhỏ sau rà soát GPT Web

## Kết luận

Word W01.1 VERIFIED trong phạm vi sửa nhỏ; chờ Thy/GPT Web nghiệm thu. Không mở W02. Bản mới vẫn 67 trang, 18 bảng, 7 khung ảnh đen, 5 Equation, 3 mục lục/danh mục tự động và 21 tài liệu tham khảo có hyperlink. Hai bìa, font/style, hình và số liệu giữ nguyên W01.

## Thay đổi

- Mục 5.15–5.16 và nhãn/caption Bảng 5.3 dùng văn phong báo cáo thay ngôn ngữ điều phối nội bộ. Giữ rõ 119 phép kiểm chức năng/vận hành và 7 phép kiểm hồ sơ, không trình bày 126 là toàn bộ kiểm chức năng.
- Rút gọn vài chú nguồn ở Chương 3–5 và một lời dẫn hình; không viết lại chương hoặc bổ sung số liệu.
- Bảng 3.1: ngắt mềm đơn vị Time theo cụm. Bảng 5.1: ngắt tên mô hình tại ranh giới HistGradient/BoostingRegressor. Tên, đơn vị, cỡ chữ, hình học bảng không đổi.
- Diff chính xác: [CHANGES.md](CHANGES.md), [changes.json](changes.json), 18 điểm sửa; live field và số caption giữ nguyên.

## Ba lớp kiểm

1. Cấu trúc: 18 bảng, 5 công thức, 7 khung đen/media byte-identical; styles/numbering/theme, section/header/footer và field instructions bảo toàn. 37 guard nguồn nguyên hash.
2. Ngữ nghĩa: đúng whitelist văn bản/ô bảng; số liệu và bảng ML không đổi; không còn cụm điều phối mục tiêu trong Chương 3–5; không nâng phạm vi kiểm thử. 37/37 phép kiểm thuộc Word đạt.
3. Artifact: Word native cập nhật field và đọc lại 67 trang; probe thêm/xóa bảng, hình, heading/TOC trên bản QA đạt 9/9, không đổi hash output. Đã xem riêng 67 ảnh cuối; 9 trang đổi, 58 trang giống pixel. Bảng 5.3 mới xuất hiện đúng trong danh mục.

Font được kiểm lại theo mẫu trường trong Mauwword, không chỉ dựa vào W01 cũ. Xem [font-audit.json](font-audit.json), [field-probe.json](field-probe.json), [page-review.md](page-review.md), [final-verification.json](final-verification.json).

## Giới hạn và lịch sử kiểm — cần đọc

- Snapshot ngoài phạm vi Word: 1.568/1.571 file đọc được khớp hash, không có file đọc được bị đổi/mất. Ba đường dẫn python/python3/python3.12 của venv-probe Phase1 là reparse links không đọc được ở Windows/WSL (“No such device”). Trạng thái kiểm snapshot là INCOMPLETE, không tuyên bố 1.571/1.571 lần này. Không sửa môi trường; không thấy thay đổi dữ liệu/model từ guard nguồn.
- Raw verification tổng hợp giữ INCOMPLETE 37 PASS + 1 INCOMPLETE. Gate Word riêng VERIFIED dựa trên 37 kiểm Word, 9 field probe và 67 trang đã rà. Đây không phải nghiệm thu của Thy/GPT Web.
- Trang 10 danh mục thuật ngữ còn cách ngắt tên HGB chưa đẹp từ W01. Giống pixel nguồn, ngoài hai ô bảng được phép sửa; không sửa trang đầu đã khóa. Không có lỗi thị giác mới được phát hiện.
- Giữ verification-attempt1/preservation-attempt1, không sửa lịch sử FAIL thành PASS. Hai báo lỗi bookmark/field cũ là so ID TOC tự sinh: Word cập nhật sinh 114 ID mới. Kiểm cuối đối chiếu tên bookmark ổn định, ánh xạ 114 ID một-một, vị trí và toàn bộ field code, tất cả PAGEREF trỏ đích tồn tại.
- Không chạy lại Flink, train/refit, tính lại metric Test hoặc sửa app. Lịch tuần/phân công chưa chốt vẫn trống. W02/PPT/demo chưa được phép.

## File Word gửi trực tiếp

`D:\\Hoctap\\bigdata\\Detaituan8910\\BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx`

SHA-256: `fafe4d7485601ba667a468990c1c80e188bf0e7126dd3edaf51059dfca3e2006`.

W01 nguồn: SHA-256 `4a47523a0bfe9c2a035df66c9fedff2e33a776dcb8c2ec01b50be8dd0d33f591`, checkpoint `d66a3c9`. Không ghi đè. DOCX/PDF/PNG/fulltext/probe copy không phát hành GitHub; chỉ hồ sơ kiểm và helper. Thy cần gửi DOCX trực tiếp kèm link review này.

## Điểm dừng

Dừng chờ Thy/GPT Web duyệt W01.1. Không coi W02 được phê duyệt từ việc W01.1 VERIFIED.
'''
(QA / 'review.md').write_text(review, encoding='utf-8')
evidence = ['artifact.md', 'changes.json', 'CHANGES.md', 'preflight.json', 'applied.json',
            'verification.json', 'preservation.json', 'field-probe.json', 'font-audit.json',
            'page-diff.json', 'page-review.md', 'visual-verification.json', 'word-summary.json',
            'final-verification.json', 'review.md', 'verification-attempt1.json', 'preservation-attempt1.json']
save('manifest.json', {'source_checkpoint': 'd66a3c9cf7b3ec09e3a97faef2ac6df8e2c80559',
                      'source': {'path': str(SOURCE), 'sha256': digest(SOURCE)},
                      'output': {'path': str(OUTPUT), 'sha256': digest(OUTPUT)},
                      'word_status': 'VERIFIED', 'snapshot_status': 'INCOMPLETE',
                      'evidence': [{'file': name, 'sha256': digest(QA / name)} for name in evidence],
                      'private_local': ['W01-native.pdf', 'render/', 'word-readback.json', 'W01-field-probe.docx']})
print(json.dumps({'word_status': final['word_status'], 'pages': 67, 'word_checks': '37/37',
                  'fields': '9/9', 'snapshot': '1568/1571; 3 unreadable', 'output_sha256': digest(OUTPUT)}, ensure_ascii=False))
