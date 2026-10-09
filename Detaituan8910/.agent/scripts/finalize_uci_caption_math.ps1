param([string]$InputDoc, [string]$JsonPath)
$ErrorActionPreference = 'Stop'
$taskWord = $null
$taskDoc = $null
try {
    $taskWord = New-Object -ComObject Word.Application
    $taskAlerts = $taskWord.DisplayAlerts
    $taskSecurity = $taskWord.AutomationSecurity
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskDoc = $taskWord.Documents.Open($InputDoc, $false, $false, $false)
    $taskDoc.Fields.Update() | Out-Null
    foreach ($taskToc in $taskDoc.TablesOfContents) {
        $taskToc.Update()
        $taskToc.Range.ParagraphFormat.RightIndent = $taskWord.CentimetersToPoints(2.5)
    }
    $taskDoc.Repaginate()
    foreach ($taskToc in $taskDoc.TablesOfContents) { $taskToc.UpdatePageNumbers() }
    $taskCaptions = @()
    foreach ($taskP in $taskDoc.Paragraphs) {
        if ($taskP.Style.NameLocal -in @('TableCaption','FigureCaption')) {
            $taskCaptions += $taskP.Range.Text.TrimEnd([char]13,[char]7)
        }
    }
    if ($taskCaptions.Count -ne 5 -or ($taskCaptions | Where-Object { $_ -notmatch '^(Bảng 1\.[1-4]|Hình 1\.1)\. ' })) { throw 'Caption update failed' }
    $taskDoc.Save()
    $taskReport = [ordered]@{pages=$taskDoc.ComputeStatistics(2); equations=$taskDoc.OMaths.Count; captions=$taskCaptions; fields=@($taskDoc.Fields | Where-Object { $_.Code.Text -match 'STYLEREF|SEQ ' } | ForEach-Object { [ordered]@{code=$_.Code.Text;result=$_.Result.Text} })}
    $taskReport | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $JsonPath -Encoding utf8
    $taskReport | ConvertTo-Json -Depth 8
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0) }
    if ($null -ne $taskWord) {
        $taskWord.DisplayAlerts = $taskAlerts
        $taskWord.AutomationSecurity = $taskSecurity
        if ($taskWord.Documents.Count -eq 0) { $taskWord.Quit() }
    }
}
