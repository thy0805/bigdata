param([string]$InputDoc, [string]$PdfPath, [string]$JsonPath, [switch]$Update)
$ErrorActionPreference = 'Stop'
$taskWord = $null
$taskDoc = $null
try {
    $taskWord = New-Object -ComObject Word.Application
    $taskAlerts = $taskWord.DisplayAlerts
    $taskSecurity = $taskWord.AutomationSecurity
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskDoc = $taskWord.Documents.Open($InputDoc, $false, !$Update, $false)
    if ($Update) {
        $taskDoc.Fields.Update() | Out-Null
        foreach ($taskToc in $taskDoc.TablesOfContents) {
            $taskToc.Update()
            $taskToc.Range.ParagraphFormat.RightIndent = $taskWord.CentimetersToPoints(1)
        }
        $taskDoc.Repaginate()
        foreach ($taskToc in $taskDoc.TablesOfContents) { $taskToc.UpdatePageNumbers() }
        $taskDoc.Save()
    }
    $taskDoc.Repaginate()
    $taskHeadings = @()
    foreach ($taskP in $taskDoc.Paragraphs) {
        if ($taskP.OutlineLevel -lt 10) {
            $taskHeadings += [ordered]@{text=$taskP.Range.Text.TrimEnd([char]13,[char]7); level=$taskP.OutlineLevel; style=$taskP.Style.NameLocal; number=$taskP.Range.ListFormat.ListString; physical_page=$taskP.Range.Information(3); page=$taskP.Range.Information(1)}
        }
    }
    $taskSections = @()
    foreach ($taskS in $taskDoc.Sections) {
        $taskSections += [ordered]@{first_page=$taskS.Range.Information(3); width=$taskS.PageSetup.PageWidth; height=$taskS.PageSetup.PageHeight; top=$taskS.PageSetup.TopMargin; bottom=$taskS.PageSetup.BottomMargin; left=$taskS.PageSetup.LeftMargin; right=$taskS.PageSetup.RightMargin}
    }
    $taskTocs = @()
    foreach ($taskToc in $taskDoc.TablesOfContents) { $taskTocs += $taskToc.Range.Text }
    $taskDoc.ExportAsFixedFormat($PdfPath,17)
    $taskReport = [ordered]@{path=$InputDoc; pages=$taskDoc.ComputeStatistics(2); sections=$taskSections; headings=$taskHeadings; toc_count=$taskDoc.TablesOfContents.Count; tocs=$taskTocs; table_count=$taskDoc.Tables.Count; figures=$taskDoc.InlineShapes.Count}
    $taskReport | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $JsonPath -Encoding utf8
    [ordered]@{pages=$taskReport.pages; headings=$taskHeadings.Count; toc_count=$taskReport.toc_count; tables=$taskReport.table_count} | ConvertTo-Json
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0) }
    if ($null -ne $taskWord) {
        $taskWord.DisplayAlerts = $taskAlerts
        $taskWord.AutomationSecurity = $taskSecurity
        if ($taskWord.Documents.Count -eq 0) { $taskWord.Quit() }
    }
}
