param([string]$InputDoc, [string]$JsonPath)
$ErrorActionPreference = 'Stop'
$taskWord = $null
$taskDoc = $null
function Find-TaskText([string]$Text) {
    foreach ($taskP in $taskDoc.Paragraphs) {
        if ($taskP.Style.NameLocal -notmatch '^TOC ' -and $taskP.Range.Text.TrimEnd([char]13,[char]7) -eq $Text) {
            return $taskP.Range.Duplicate
        }
    }
    throw "Không tìm thấy: $Text"
}
function Insert-TaskHeading([string]$Before, [string]$Label, [string]$Style) {
    $taskTarget = Find-TaskText $Before
    $taskStart = $taskTarget.Paragraphs.Item(1).Range.Start
    $taskRange = $taskDoc.Range($taskStart, $taskStart)
    $taskRange.InsertBefore($Label + [char]13)
    $taskInserted = $taskDoc.Range($taskStart, $taskStart + $Label.Length + 1)
    $taskInserted.Style = $taskDoc.Styles.Item($Style)
    return $taskInserted
}
try {
    $taskWord = New-Object -ComObject Word.Application
    $taskAlerts = $taskWord.DisplayAlerts
    $taskSecurity = $taskWord.AutomationSecurity
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskDoc = $taskWord.Documents.Open($InputDoc, $false, $true, $false)
    $taskProbe = Insert-TaskHeading 'Cấu trúc và các thuộc tính của dữ liệu' 'Kiểm thử chèn heading' 'Heading 21'
    $taskDoc.Repaginate()
    $taskInsertedNumber = $taskProbe.ListFormat.ListString
    $taskShifted = (Find-TaskText 'Cấu trúc và các thuộc tính của dữ liệu').ListFormat.ListString
    $taskDoc.TablesOfContents.Item(1).Update()
    $taskTocInserted = $taskDoc.TablesOfContents.Item(1).Range.Text.Contains('Kiểm thử chèn heading')
    $taskProbe.Delete() | Out-Null
    $taskDoc.Repaginate()
    $taskRestored = (Find-TaskText 'Cấu trúc và các thuộc tính của dữ liệu').ListFormat.ListString
    $taskLevel3 = Insert-TaskHeading 'Cấu trúc và các thuộc tính của dữ liệu' 'Kiểm thử mục cấp ba' 'Heading 31'
    $taskDoc.Repaginate()
    $taskLevel3Number = $taskLevel3.ListFormat.ListString
    $taskDoc.TablesOfContents.Item(1).Update()
    $taskTocLevel3 = $taskDoc.TablesOfContents.Item(1).Range.Text.Contains('Kiểm thử mục cấp ba')
    $taskLevel3.Delete() | Out-Null
    foreach ($taskType in @('FigureCaption', 'TableCaption')) {
        $taskStart = $taskDoc.Content.End - 1
        $taskLabel = if ($taskType -eq 'FigureCaption') { 'Hình 9.1. Kiểm thử danh mục hình' } else { 'Bảng 9.1. Kiểm thử danh mục bảng' }
        $taskRange = $taskDoc.Range($taskStart, $taskStart)
        $taskRange.InsertAfter([char]13 + $taskLabel + [char]13)
        $taskP = Find-TaskText $taskLabel
        $taskP.Style = $taskDoc.Styles.Item($taskType)
    }
    $taskFigureList = $false
    $taskTableList = $false
    $taskDoc.TablesOfContents.Item(2).Update()
    $taskDoc.TablesOfContents.Item(3).Update()
    $taskFigureText = $taskDoc.TablesOfContents.Item(2).Range.Text
    $taskTableText = $taskDoc.TablesOfContents.Item(3).Range.Text
    $taskFigureList = $taskFigureText.Contains('Kiểm thử danh mục hình')
    $taskTableList = $taskTableText.Contains('Kiểm thử danh mục bảng')
    $taskReport = [ordered]@{path=$InputDoc; changes_saved=$false; inserted_h2=$taskInsertedNumber; following_h2=$taskShifted; restored_h2=$taskRestored; toc_detects_inserted=$taskTocInserted; inserted_h3=$taskLevel3Number; toc_detects_h3=$taskTocLevel3; figure_list_detects_caption=$taskFigureList; table_list_detects_caption=$taskTableList; figure_probe_result=$taskFigureText; table_probe_result=$taskTableText}
    $taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $JsonPath -Encoding utf8
    $taskReport | ConvertTo-Json -Depth 8
    if ($taskInsertedNumber -ne '3.2.' -or $taskShifted -ne '3.3.' -or $taskRestored -ne '3.2.' -or $taskLevel3Number -ne '3.1.1.' -or !$taskTocInserted -or !$taskTocLevel3 -or !$taskFigureList -or !$taskTableList) { throw 'Kiểm thử numbering/field thất bại' }
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0) }
    if ($null -ne $taskWord) {
        $taskWord.DisplayAlerts = $taskAlerts
        $taskWord.AutomationSecurity = $taskSecurity
        if ($taskWord.Documents.Count -eq 0) { $taskWord.Quit() }
    }
}
