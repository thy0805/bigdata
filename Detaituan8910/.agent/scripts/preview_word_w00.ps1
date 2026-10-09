$ErrorActionPreference = 'Stop'
$qaPath = 'D:\Hoctap\bigdata\Detaituan8910\.agent\qa\word-w00-20261010'
$sourcePath = 'C:\Users\thy\Downloads\HAULYVUNHAN_Chuong2_CoSoLyThuyet_HoanChinh.docx'
$pdfPath = Join-Path $qaPath 'chapter2-readonly-preview.pdf'
if (Test-Path -LiteralPath $pdfPath) { throw 'Preview already exists; do not overwrite.' }
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
$wordDoc = $null
try {
    $wordDoc = $wordApp.Documents.Open($sourcePath, $false, $true, $false)
    $wordDoc.Repaginate()
    $headingPages = @()
    foreach ($paragraph in $wordDoc.Paragraphs) {
        $value = $paragraph.Range.Text.Trim()
        if ($value -match '^2\.\d+\.') {
            $headingPages += @{text=$value; page=$paragraph.Range.Information(3)}
        }
    }
    $wordDoc.ExportAsFixedFormat($pdfPath, 17)
    $result = @{read_only=$wordDoc.ReadOnly; pages=$wordDoc.ComputeStatistics(2); headings=$headingPages; pdf=$pdfPath; source=$sourcePath; saved_to_source=$false}
    $result | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $qaPath 'chapter2-preview.json') -Encoding UTF8
    $result | ConvertTo-Json -Depth 6
} finally {
    if ($null -ne $wordDoc) { $wordDoc.Close(0) }
    $wordApp.Quit(0)
}
