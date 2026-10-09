$ErrorActionPreference = 'Stop'
$taskWord = $null
$taskDoc = $null
$taskPath = 'D:\Hoctap\bigdata\Detaituan8910\BaoCao_PhanTich_DuDoan_DienNang_UCI_20261008.docx'
try {
    $taskWord = New-Object -ComObject Word.Application
    $taskAlerts = $taskWord.DisplayAlerts
    $taskSecurity = $taskWord.AutomationSecurity
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskDoc = $taskWord.Documents.Open($taskPath, $false, $false, $false)
    $taskDoc.Fields.Update() | Out-Null
    foreach ($taskToc in $taskDoc.TablesOfContents) {
        $taskToc.Update()
        $taskToc.Range.ParagraphFormat.RightIndent = $taskWord.CentimetersToPoints(2.5)
    }
    $taskDoc.Repaginate()
    foreach ($taskToc in $taskDoc.TablesOfContents) { $taskToc.UpdatePageNumbers() }
    $taskDoc.Save()
    [ordered]@{pages=$taskDoc.ComputeStatistics(2); maths=$taskDoc.OMaths.Count; captionFields=@($taskDoc.Fields | Where-Object { $_.Code.Text -match 'STYLEREF|SEQ ' } | ForEach-Object { [ordered]@{code=$_.Code.Text; result=$_.Result.Text} })} | ConvertTo-Json -Depth 8
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0) }
    if ($null -ne $taskWord) {
        $taskWord.DisplayAlerts = $taskAlerts
        $taskWord.AutomationSecurity = $taskSecurity
        if ($taskWord.Documents.Count -eq 0) { $taskWord.Quit() }
    }
}
