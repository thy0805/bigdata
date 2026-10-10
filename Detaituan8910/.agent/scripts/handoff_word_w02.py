import hashlib
import json
import posixpath
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

from lxml import etree

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / 'Detaituan8910'
BASE = PROJECT / '.agent/qa'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
OUTPUTS = [('word-w02-20261010', 'W02', '507b242603573c6bce5849c1c84c32963bef94b03cdca32c7ee21cd53b20ba96'), ('word-w021-20261010', 'W02_1', 'db0cf6ef43ae2887e76ebf10711c3bd425961b00b940f99f0963e16df2223788')]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


guards = read(BASE / 'word-w011-20261010/preflight.json')['guards']
preservation = [{'path': path, 'expected': expected, 'actual': digest(Path(path))} for path, expected in guards.items()]
assert len(preservation) == 37 and all(p['expected'] == p['actual'] for p in preservation)
source = PROJECT / 'BaoCao_PhanTich_DuDoan_DienNang_UCI_W01_1_v1_20261010.docx'
assert digest(source) == '876945c3b6913b1f495fe89900eff4d70a07823db8aff3ce7ca7d979f9cb5b34'
registry = read(BASE / 'word-w02-20261010/image-registry.json')
origin = {'F31': 'hourly-table.png; sáu bản ghi thật trong hourly-table-records.json', 'F32': 'source-images/image6.png, crop biểu đồ Tổng quan', 'F41': 'source-images/image5.png, crop biểu đồ Thực tế/HGB', 'F51': 'source-images/image6.png, Tổng quan', 'F52': 'source-images/image7.png, dataset UCI và 11 đặc trưng', 'F53': 'source-images/image8.png, Phân tích', 'F54': 'source-images/image9.png, Dự báo'}
pages = {'F31': 46, 'F32': 48, 'F41': 53, 'F51': 59, 'F52': 60, 'F53': 62, 'F54': 63}

for folder, version, expected in OUTPUTS:
    qa = BASE / folder
    verification = read(qa / 'verification.json')
    output = Path(verification['output'])
    assert digest(output) == expected == verification['sha256']
    assert verification['status'] == 'PASS' and verification['passed'] == verification['total']
    assert all(c['status'] == 'PASS' for c in verification['checks'])
    native = read(qa / 'word-readback.json')
    render = read(qa / 'render-pages.json')
    review = qa / 'page-review.md'
    assert review.is_file() and '69' in review.read_text(encoding='utf-8')
    assert native['pages'] == render['page_count'] == 69
    assert len(render['pages']) == 69 and all(Path(p['image']).is_file() for p in render['pages'])
    with ZipFile(output) as z:
        doc = etree.fromstring(z.read('word/document.xml'))
        rels = {n.get('Id'): n.get('Target') for n in etree.fromstring(z.read('word/_rels/document.xml.rels'))}
        paras = doc.xpath('./w:body/w:p', namespaces=NS)
        resolved = []
        for item in registry:
            p = paras[item['paragraph_index']]
            rid = p.xpath('.//a:blip/@r:embed', namespaces=NS)[0]
            part = posixpath.normpath('word/' + rels[rid])
            resolved.append({**item, 'authoring_relationship_id': item['relationship_id'], 'relationship_id': rid, 'part': part, 'sha256': hashlib.sha256(z.read(part)).hexdigest(), 'source': origin[item['key']], 'physical_page': pages[item['key']], 'status': 'VERIFIED'})
    save(qa / 'image-registry-final.json', resolved)
    gate = {'status': 'VERIFIED', 'technical_result': 'PASS', 'acceptance': 'PENDING_THY_GPT_WEB', 'at': datetime.now(timezone.utc).isoformat(), 'output': str(output), 'sha256': expected, 'source_sha256': verification['source_sha256'], 'pages': 69, 'structural_semantic_checks': {'passed': verification['passed'], 'total': verification['total'], 'evidence': 'verification.json'}, 'artifact_verification': {'native_Word_field_update': True, 'tables': native['tables'], 'inline_images': native['inline_shapes'], 'equations': native['equations'], 'toc_lists': native['toc'], 'render_pages': 69, 'individual_PNG_review_pages': 69, 'evidence': ['word-readback.json (local only)', 'render-pages.json (local only)', 'page-review.md']}, 'preservation': preservation, 'limits': ['37 explicit source/product/template guards, not renewed whole-runtime audit', '21 DOCX external links preserved; no fresh HTTP availability audit', 'Native Word/PDFium rendering; bundled LibreOffice renderer unavailable', 'Existing glossary long-name wrap on physical page 10 retained outside scope', 'Three-week schedule organizes work; elapsed calendar weeks not independently established'], 'forbidden_actions_performed': [], 'next_action': 'STOP for Thy/GPT Web acceptance; no PowerPoint, app, model, demo or video'}
    if version == 'W02_1':
        gate['page_diff'] = read(qa / 'page-diff.json')
        changes = read(qa / 'changes.json')
        gate['schedule'] = changes['schedule_after']
        gate['reference_access_dates_removed'] = len(changes['access_date_changes'])
        gate['references_and_external_links'] = 21
    save(qa / 'final-verification.json', gate)
    evidence = ['verification.json', 'final-verification.json', 'changes.json', 'page-review.md', 'image-registry-final.json']
    save(qa / 'manifest.json', {'version': version, 'status': 'VERIFIED_TECHNICAL_ACCEPTANCE_PENDING', 'artifact': {'path': str(output), 'sha256': expected, 'pages': 69, 'delivery': 'Direct DOCX only, not public GitHub'}, 'evidence': [{'path': name, 'sha256': digest(qa / name)} for name in evidence]})
    image_rows = '\n'.join('| ' + ' | '.join([i['caption'], str(i['physical_page']), i['source']]) + ' |' for i in resolved)
    specific = ('W02 chỉ thay câu dẫn/hình và phân công Phát. Lịch và ngày truy cập giữ nguyên đến W02.1.' if version == 'W02' else 'W02.1 chỉ đổi lịch từ 5 cột/10 tuần trống thành 4 cột/3 tuần và bỏ 21 cụm ngày truy cập. 65/69 trang giống pixel W02; chỉ trang 3, 67, 68, 69 đổi. 17 bảng còn lại, toàn bộ hình/crop/công thức/nội dung chương giữ nguyên.')
    body = f'''# Bàn giao {version.replace('_', '.')}\n\nVERIFIED kỹ thuật; **chờ Thy/GPT Web nghiệm thu**, không tự khóa Word.\n\nFile gửi trực tiếp: `{output}`\n\nSHA-256: `{expected}`. Số trang Microsoft Word và bản render: **69**. Không có DOCX/PDF/PNG/full-text trên GitHub.\n\n{specific}\n\n## Kết quả kiểm tra\n\n- Cấu trúc và ngữ nghĩa: {verification['passed']}/{verification['total']} PASS tại verification.json. Final-verification.json bổ sung kiểm artifact và rà riêng 69 PNG; không sửa trạng thái lịch sử trong raw evidence.\n- 18 bảng, 5 công thức native, 3 mục lục/danh mục tự động, 8 caption hình và 15 caption bảng; field không lỗi, đích PAGEREF còn tồn tại.\n- Bảy hình thật đúng slot, không ảnh đen; giữ tỷ lệ/crop Word, caption cùng trang. Hình 1.1 và hai logo bìa không thay.\n- Bỏ dẫn hình/bảng thừa bằng 14 diff whitelist; giữ phương pháp, số liệu, công thức. Danh sách trước/sau: ../word-w02-20261010/CHANGES.md và changes.json.\n- Phát: Chương 3, 4, 5; lập trình hệ thống; báo cáo Word; xử lý, trình bày dữ liệu Excel. Không điền tỷ lệ đóng góp.\n- Bảo toàn 37 nguồn/sản phẩm/mẫu theo hash; không train/refit, đổi metric, chạy Flink hoặc sửa ứng dụng. Không ghi đè Word nguồn.\n\n## Bảy hình và nguồn\n\n| Caption | Trang vật lý | Nguồn local QA W02 |\n| --- | --- | --- |\n{image_rows}\n\nImage-registry-final.json ghi part/relationship/hash thực tế sau khi Word lưu, không dùng relationship ID authoring làm mapping cuối. H3.1 là ảnh bảng từ sáu dòng CSV thật, có giờ đầy đủ/thiếu/NULL; H3.2 là crop đúng đồ thị trong ảnh Tổng quan của Thy. Không dùng ảnh mạng.\n\n## Lịch và tài liệu tham khảo ở bản cuối W02.1\n\nLịch đúng Tuần/Nội dung công việc/Thành viên/Trạng thái. Tuần 1 cả nhóm đã thực hiện; tuần 2 Phát đã thực hiện theo phân công trực tiếp và artifact xử lý/mô hình; tuần 3 cả nhóm đang thực hiện/phối hợp rà soát, chuẩn bị trình bày. Đây là tổ chức đầu việc đề xuất, không nhật ký ba tuần lịch sử được xác minh; không gán ngày hoặc nhận đã thuyết trình.\n\nBỏ 21 cụm “Truy cập ngày 08/10/2026.”, giữ 21 nguồn đánh số, tác giả, năm công bố, DOI, phiên bản, URL và hyperlink. Mẫu trường có ví dụ ngày truy cập, chưa thấy quy định bắt buộc. Kiểm hyperlink là cấu trúc DOCX/URL được bảo toàn, không phải kiểm HTTP mới của 21 website.\n\n## Giới hạn và điểm dừng\n\nTrang 10 còn ngắt tên dài trong glossary như nguồn; ngoài scope nên giữ. Chữ phụ ảnh toàn dashboard cần zoom; không cắt KPI/trục/đơn vị. Native Word/PDFium đã kiểm; renderer đóng gói thiếu soffice, không tuyên bố đã kiểm mọi renderer. Cache/runtime toàn máy không được audit lại; preservation chỉ 37 nguồn chuẩn nêu trong final gate.\n\nCác snapshot APPLIED_UNVERIFIED trong changes/verification/word-readback là lịch sử bước trước rà thị giác; gate hiện hành là final-verification.json và page-review.md. Dừng chờ duyệt W02.1, không chuyển PowerPoint/demo/code.\n'''
    (qa / 'review.md').write_text(body, encoding='utf-8')

changes = read(BASE / 'word-w02-20261010/changes.json')
parts = ['# W02 — thay đổi trước và sau', '', 'Chỉ 14 đoạn thân bài có span/câu dẫn được bỏ, cùng một ô phân công Phát. Chỉ số paragraph là zero-based trong OOXML nguồn.', '']
for item in changes:
    parts.extend([f"## Paragraph {item.get('index', 'ô phân công')}", '', '**Trước:** ' + (item['before'] or '(ô trống)'), '', '**Sau:** ' + item['after'], ''])
(BASE / 'word-w02-20261010/CHANGES.md').write_text('\n'.join(parts), encoding='utf-8')
print(json.dumps({'status': 'VERIFIED', 'outputs': [read(BASE / f / 'final-verification.json')['sha256'] for f, _, _ in OUTPUTS], 'preservation': '37/37', 'acceptance': 'PENDING_THY_GPT_WEB'}, ensure_ascii=False))
