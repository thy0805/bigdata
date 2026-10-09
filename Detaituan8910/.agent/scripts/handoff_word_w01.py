import hashlib
import json
import posixpath
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from lxml import etree

PROJECT = Path(__file__).resolve().parents[2]
QA = PROJECT / '.agent/qa/word-w01-20261010'
OUTPUT = PROJECT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_v1_20261010.docx'
EXPECTED = '4a47523a0bfe9c2a035df66c9fedff2e33a776dcb8c2ec01b50be8dd0d33f591'


def read(name):
    return json.loads((QA / name).read_text(encoding='utf-8-sig'))


def save(name, data):
    (QA / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def markdown(name, text):
    (QA / name).write_text(text.rstrip() + '\n', encoding='utf-8')


sha = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
assert sha == EXPECTED
verification = read('verification.json')
probe = read('field-probe.json')
native = read('word-readback.json')
fonts = read('font-audit.json')
preservation = read('preservation.json')
references = read('reference-audit.json')
changes = read('content-changelog.json')
assert verification['status'] == probe['status'] == 'PASS'
assert native['pages'] == 67
assert not fonts['output']['font_exceptions']
captions = [p for p in native['paragraphs'] if p['style'] in ('TableCaption', 'FigureCaption')]
assert len(captions) == 23
registry = read('image-registry.json')
ns = {'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with zipfile.ZipFile(OUTPUT) as archive:
    document = etree.fromstring(archive.read('word/document.xml'))
    relationships = etree.fromstring(archive.read('word/_rels/document.xml.rels'))
    targets = {node.get('Id'): node.get('Target') for node in relationships}
    for image in registry['images']:
        drawing = next(node for node in document.xpath('//wp:docPr', namespaces=ns)
                       if node.get('name') == f"W01_{image['image_id']}_{image['key']}")
        rid = drawing.getparent().xpath('.//a:blip/@r:embed', namespaces=ns)[0]
        image['authoring_media'] = image.get('authoring_media', image['media'])
        image['media'] = targets[rid]
        image['relationship_id'] = rid
        image['drawing_name'] = drawing.get('name')
        image['media_sha256'] = hashlib.sha256(archive.read(posixpath.normpath('word/' + targets[rid]))).hexdigest()
        paragraph = next(p for p in captions if p['text'] == image['caption'])
        image['printed_page'] = paragraph['page']
        image['physical_page'] = paragraph['physical_page']
registry['resolved_against_output_sha256'] = sha
registry['note'] = 'Word chuẩn hóa tên và dùng chung image part cho ảnh đen giống nhau; kiểm theo drawing relationship, không theo tên file lúc authoring.'
save('image-registry.json', registry)

summary = {key: native[key] for key in ('pages', 'words', 'tables', 'inline_shapes', 'equations', 'toc', 'sections')}
summary.update(output_name=OUTPUT.name, sha256=sha, captions=[{key: p[key] for key in ('text', 'page', 'physical_page')} for p in captions])
save('word-summary.json', summary)
counts = Counter(change['chapter'] for change in changes)
manifest = {'at': datetime.now(timezone.utc).isoformat(), 'status': 'VERIFIED_TECHNICAL_ACCEPTANCE_PENDING',
            'source_checkpoint': 'ff0e5d7d5422e0381c3fedaaabbbc4416286156f',
            'output': str(OUTPUT), 'sha256': sha, 'pages': 67,
            'source_guards': read('preflight.json')['guards'],
            'counts': {'tables_total': 18, 'tables_captioned': 15, 'tables_new': 11,
                       'figures_captioned': 8, 'black_placeholders': 7, 'original_figures': 1,
                       'chapter2_sections': 14, 'chapter_sections': 69, 'native_equations': 5,
                       'reference_hyperlinks': 21, 'toc_and_lists': 3},
            'change_records_by_chapter': dict(counts), 'acceptance': 'PENDING_THY_GPT_WEB',
            'next_phase': 'W02_NOT_AUTHORIZED', 'phase4': 'INCOMPLETE_I04_DEFERRED'}
save('manifest.json', manifest)
visual = {'status': 'PASS', 'output_sha256': sha, 'render': 'Native Word PDF → PDFium scale 2',
          'inspection': 'Main agent inspected each final page PNG at original resolution in this turn; not only contact sheets.',
          'reviewed_pages': list(range(1, 68)), 'resolution': [1191, 1684],
          'findings': [], 'limits': ['Seven black slots intentionally await separately approved W02.',
                                    'Unconfirmed assignment/history/contribution fields intentionally blank.']}
save('visual-verification.json', visual)
save('final-verification.json', {'status': 'VERIFIED', 'acceptance': 'PENDING_THY_GPT_WEB', 'output_sha256': sha,
                               'structural_semantic': {'status': 'PASS', 'passed': len(verification['checks']), 'evidence': 'verification.json'},
                               'live_fields': {'status': 'PASS', 'passed': len(probe['checks']), 'evidence': 'field-probe.json'},
                               'visual': {'status': 'PASS', 'pages': 67, 'evidence': 'visual-verification.json; page-review.md'},
                               'font': {'status': 'PASS', 'evidence': 'font-audit.json'},
                               'preservation': preservation,
                               'references': {'hyperlinks': 21, 'reachable': references['reachable'],
                                              'restricted_or_unverified': references['restricted_or_unverified'],
                                              'evidence': 'reference-audit.json; REFERENCE_REVIEW.md'},
                               'limitations': visual['limits'],
                               'history': 'verification-attempt1.json records 66/69. Original verification.json is an intermediate gate; this aggregate records completed field and visual gates. No historic failure was rewritten.'})

rows = ['# Danh sách bảng và hình W01', '', 'Có 18 bảng thực tế: 3 bảng phần đầu và 15 bảng có caption. Trong 8 hình có caption, Hình 1.1 là hình gốc; 7 hình mới chỉ là khung đen chờ W02.', '', '| Caption | Trang nội dung | Trang vật lý |', '| --- | --- | --- |']
rows.extend(f"| {p['text']} | {p['page']} | {p['physical_page']} |" for p in captions)
rows.extend(['', '11 bảng mới: Bảng 3.1–3.4, 4.1–4.4 và 5.1–5.3. Registry image-registry.json chứa vị trí, nguồn dự kiến và media relationship thực tế của 7 khung đen.', '', 'Thứ tự Hình 5.1 Tổng quan → Hình 5.2 giới thiệu dữ liệu → Hình 5.3 Phân tích → Hình 5.4 Dự báo đã kiểm.'])
markdown('TABLE_FIGURE_LIST.md', '\n'.join(rows))
rows = ['# Thay đổi nội dung W01', '', 'Nguồn W00 ff0e5d7. Đây là hồ sơ diff, không phải dữ liệu thực nghiệm mới.', '', f'Chương 1: {counts[1]} đoạn thay; Chương 2: {counts[2]} bản ghi thay đổi/chuẩn hóa; Chương 5: {counts[5]} tiêu đề. Số bản ghi Chương 2 không đồng nghĩa 67 mục: toàn chương có 14 mục.', '', 'Mở đầu, Chương 3–5, Kết luận và Lời cảm ơn đã viết theo nguồn thực nghiệm đã khóa. Không chạy lại Flink, train hoặc Test evaluation. Lịch sử tuần, phần công việc của Phát và tỷ lệ đóng góp chưa xác nhận vẫn để trống.']
for index, change in enumerate(changes, 1):
    location = change.get('section', f"B{change.get('block', change.get('source_block', ''))}")
    rows.extend(['', f"## {index}. Chương {change['chapter']} · {location}", '', change.get('reason', '')])
    for key, label in [('before', 'Trước'), ('after', 'Sau')]:
        if key in change:
            rows.extend(['', f"{label}: {change[key]}"])
markdown('CHAPTER_CHANGES.md', '\n'.join(rows))
rows = ['# Rà tài liệu tham khảo W01', '', '21 mục [1]–[21] ở cuối báo cáo có hyperlink thật; không có [n] trong thân bài. Kiểm URL không đồng nghĩa đọc được mọi full text.', '', '18 liên kết trả HTTP 200. [9] gặp lỗi SSL từ client kiểm cục bộ; PDF đã được đọc qua công cụ web trong lượt này. [10] trang IEEE bị hạn chế, metadata DOI đã đối chiếu Crossref; không tuyên bố đã mở toàn văn IEEE. [12] client nhận 403, nội dung trang đã đọc bằng công cụ web. Không giả nhận tất cả link đều HTTP 200.', '', '[4] giữ năm trích dẫn UCI 2006; không nhầm với thời điểm donation 2012. [20] đã sửa sang trang group aggregation chính thức Flink 2.3 và n.d.; nguồn mới truy cập 10/10/2026. Những ngày truy cập nguồn cũ giữ theo hồ sơ gốc.', '', '| Mục | Nguồn | Trạng thái kiểm URL |', '| --- | --- | --- |']
for ref in references['references']:
    title = ref['title'].replace('|', '\\|')
    rows.append(f"| {ref['reference']} | [{title}]({ref['url']}) | {ref['status']} |")
markdown('REFERENCE_REVIEW.md', '\n'.join(rows))
markdown('page-review.md', '''# Kiểm hình thức toàn bộ W01

Artifact SHA-256: ''' + sha + '''

Main agent đã xem riêng từng PNG cuối cùng 1–67 ở độ phân giải gốc 1191×1684; không suy ra từ contact sheet. Render bằng native Word và PDFium sau khi cập nhật trường. LibreOffice bundled không khả dụng ở môi trường này; hai lần thử có lỗi được giữ trong QA cục bộ, không xem đó là render thành công.

| Trang vật lý | Nội dung | Kết quả |
| --- | --- | --- |
| 1–2 | Hai bìa, khung, logo, tên/MSSV/giảng viên | PASS, bảo toàn nguồn |
| 3–4 | Lịch tuần và phân công | PASS, ô chưa xác nhận giữ trống |
| 5 | Lời cảm ơn | PASS, 9 dòng thực tế |
| 6–8 | Mục lục tự động | PASS, tên dài xuống dòng và số trang rõ |
| 9–10 | Thuật ngữ | PASS, header bảng lặp; thêm HGB/Train/Validation/Test |
| 11–12 | Danh mục hình/bảng | PASS, 8 hình/15 bảng và số theo chương |
| 13 | Mở đầu, bắt đầu trang Arab 1 | PASS |
| 14–27 | Chương 1 và Hình 1.1 gốc | PASS, MAE/RMSE trang 21 rõ; hình gốc trang 27 giữ nguyên |
| 28–41 | Chương 2, 14 mục Hậu | PASS, công thức trang 35–36 rõ, lý thuyết tách triển khai BATCH |
| 42–48 | Chương 3 | PASS, bảng không cắt chữ, 2 khung đen đúng chỗ |
| 49–54 | Chương 4 | PASS, feature/split/metric rõ, 4.14 không tạo trang gần trống riêng |
| 55–63 | Chương 5 | PASS, 4 khung đen, H5.2 trước H5.3; B5.3 có REF thật |
| 64 | Kết luận | PASS |
| 65–67 | Tài liệu tham khảo | PASS, số Arab tiếp tục; hyperlink dài xuống dòng đọc được |

Không phát hiện trang trắng thừa, chữ bị cắt, overlap hoặc ký tự công thức hỏng. Một số tên tiếng Anh dài xuống dòng trong ô bảng; không tràn khỏi ô. Giữ bảng nguyên khối có thể để khoảng trắng cuối trang, không phải trang trắng bất thường. Bảy khung đen là placeholder có chủ ý, không phải hình thực nghiệm hoàn tất.
''')
markdown('format-final.md', '''# Định dạng cuối W01

- Đối chiếu trực tiếp mẫu Mauwword/Mau bao cao_Do an_Khoa luan_2025.docx: Times New Roman; nội dung 13; chương 18 đậm; mục lớn 14; bảng 12. Công thức dùng Cambria Math chuẩn Word; chú nguồn bảng mới 11 nghiêng là vai trò riêng.
- A4, lề trái 3,5 cm và các lề còn lại 2,5 cm. Hai bìa giữ khung/logo và role font của nguồn. Phần đầu Roman, từ Mở đầu Arab 1.
- Final dùng Heading 1 built-in cho chương, clone hình thức ChapterTitle nguồn. Caption STYLEREF Heading 1 lấy số chương kết hợp SEQ reset theo cấp 1; không lấy nguyên chữ tiêu đề chương. Heading21/Heading31 là style thật có numbering.
- Đã phục hồi keepNext trong 7 bảng nguồn để không chia bảng cũ sai; 11 bảng mới header lặp/height tự động/caption trên.
- Mục lục, danh mục hình/bảng và 18 REF cập nhật trong Word. Probe thêm/xóa heading, bảng, hình trên bản QA riêng đạt 9/9; 23 caption phục hồi và DOCX chính giữ nguyên hash.
- Lượt verification đầu 66/69 chưa đạt: phép kiểm ảnh cần theo relationship sau Word chuẩn hóa tên; so TOC cần chuẩn hóa chữ hoa; B5.3 thiếu REF thật. Đã sửa kiểm tra đúng cấu trúc và thêm REF thật, lượt cuối 69/69. Không xóa hồ sơ FAIL cũ.
- Chương 1 chỉ thay bốn đoạn đã duyệt; không thêm đoạn HGB ở 1.8. Hai đoạn 4.14 rút gọn để tránh trang gần trống. Nội dung/số liệu thực nghiệm không thay.
''')
markdown('review.md', '''# Bàn giao W01 — Word 67 trang

**VERIFIED kỹ thuật; chờ Thy/GPT Web nghiệm thu. Không phải bản nộp cuối vì còn 7 khung ảnh đen chờ W02.**

File Word gửi trực tiếp, không có trong GitHub:

`''' + str(OUTPUT) + '''`

SHA-256: `''' + sha + '''`

## Đã thực hiện

- Ghép đủ 14 mục Chương 2 của Hậu, sửa có chọn lọc theo W00; giữ Chương 1 ngoài bốn đoạn đã duyệt, bốn bảng/hình/công thức gốc.
- Hoàn thành Mở đầu, Chương 3–5, Kết luận và Lời cảm ơn 9 dòng từ dữ liệu/kết quả đã khóa. Không tạo số liệu, train/refit/Test evaluation hoặc chạy Flink mới.
- Thêm 11 bảng và 7 khung đen; 18 bảng tổng/15 bảng caption, 8 hình caption gồm 1 hình gốc. Sửa 5.6–5.8 theo SQL BATCH, không gán KeyBy/Watermark/window streaming cho pipeline đã chạy.
- Giữ hai bìa, khung, logo, nhóm và giảng viên. Font khớp mẫu trường Mauwword. Mục lục và danh mục/numbering/REF thật hoạt động.
- Không còn [n] trong thân bài; cuối báo cáo 21 mục tham khảo có hyperlink thật.

## Bằng chứng cần đọc

1. [final-verification.json](final-verification.json): tổng hợp từng lớp kiểm, không cộng chồng các số kiểm thành một thành tích mới.
2. [verification.json](verification.json), [field-probe.json](field-probe.json): 69/69 cấu trúc/ngữ nghĩa và 9/9 live insert/delete trên QA copy. File verification.json là gate trung gian; trạng thái hoàn tất nằm ở final-verification.json.
3. [page-review.md](page-review.md), [visual-verification.json](visual-verification.json), [font-audit.json](font-audit.json): xem riêng đủ 67 trang và so font mẫu. PDF/PNG/read-back toàn văn giữ local.
4. [CHAPTER_CHANGES.md](CHAPTER_CHANGES.md), [content-changelog.json](content-changelog.json): Ch1 bốn đoạn, Ch2 67 bản ghi thay/chuẩn hóa trên 14 mục, Ch5 ba tiêu đề.
5. [TABLE_FIGURE_LIST.md](TABLE_FIGURE_LIST.md), [image-registry.json](image-registry.json), [word-summary.json](word-summary.json): caption, vị trí trang và khung W02.
6. [REFERENCE_REVIEW.md](REFERENCE_REVIEW.md), [reference-audit.json](reference-audit.json): 21 hyperlink, 18 HTTP200; ba hạn chế truy cập được ghi riêng.
7. [manifest.json](manifest.json), [preflight.json](preflight.json), [preservation.json](preservation.json): 30 nguồn khóa và 1.571/1.571 artifact giữ hash.
8. [format-final.md](format-final.md), [checklist.md](checklist.md): sửa số theo chương/flow và lịch sử gate 66/69 được bảo toàn.

## Còn chờ

Thy/GPT Web duyệt W01; W02 ảnh thật cần yêu cầu riêng. Lịch làm việc đã diễn ra, công việc Phát và tỷ lệ đóng góp chưa có xác nhận nên giữ ô trống. Ba hạn chế URL không được mô tả thành mọi nguồn đều full-text mở. Coldboot/autostart vẫn theo giới hạn QA ứng dụng cũ. I04 DEFERRED, toàn Phase4 không được tuyên bố hoàn tất.

**Điểm dừng: không tự W02, Word vòng mới, PowerPoint, demo/video hoặc thay app/data/model.**
''')
assert hashlib.sha256(OUTPUT.read_bytes()).hexdigest() == sha
print(json.dumps({'status': 'PASS', 'output_sha256': sha, 'pages': 67, 'changes': dict(counts), 'registry_resolved': len(registry['images'])}, ensure_ascii=False))
