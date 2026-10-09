param([string]$DocumentPath, [string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$taskWord = $null
$taskDoc = $null
try {
    $taskWord = New-Object -ComObject Word.Application
    $taskWord.Visible = $false
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskDoc = $taskWord.Documents.Open($DocumentPath, $false, $false, $false)
    $taskDoc.Fields.Update() | Out-Null
    $taskDoc.Fields.Update() | Out-Null
    foreach ($taskToc in $taskDoc.TablesOfContents) {
        $taskToc.Update()
        $taskToc.Range.ParagraphFormat.RightIndent = $taskWord.CentimetersToPoints(2.5)
    }
    $taskDoc.Repaginate()
    $taskDoc.Fields.Update() | Out-Null
    foreach ($taskToc in $taskDoc.TablesOfContents) { $taskToc.UpdatePageNumbers() }
    $taskDoc.Save()
    $taskPdf = Join-Path $OutputDirectory 'W01-native.pdf'
    $taskDoc.ExportAsFixedFormat($taskPdf, 17)
    $taskParagraphs = @()
    foreach ($taskParagraph in $taskDoc.Paragraphs) {
        $taskStyle = [string]$taskParagraph.Style.NameLocal
        $taskRange = $taskParagraph.Range
        $taskStartRange = $taskRange.Duplicate
        $taskStartRange.Collapse(1)
        $taskParagraphs += [ordered]@{
            text=$taskRange.Text.TrimEnd([char]13, [char]7)
            style=$taskStyle
            page=$taskStartRange.Information(1)
            physical_page=$taskStartRange.Information(3)
            physical_end_page=$taskRange.Information(3)
            label=$taskRange.ListFormat.ListString
            lines=$taskRange.ComputeStatistics(1)
            start=$taskRange.Start
            end=$taskRange.End
        }
    }
    $taskFields = @($taskDoc.Fields | ForEach-Object { [ordered]@{code=$_.Code.Text; result=$_.Result.Text} })
    $taskSections = @($taskDoc.Sections | ForEach-Object { $taskSectionStart=$_.Range.Duplicate; $taskSectionStart.Collapse(1); [ordered]@{start=$_.Range.Start; page=$taskSectionStart.Information(3); numbering=$_.Footers.Item(1).PageNumbers.NumberStyle; restart=$_.Footers.Item(1).PageNumbers.RestartNumberingAtSection; start_number=$_.Footers.Item(1).PageNumbers.StartingNumber} })
    $taskResult = [ordered]@{
        status='FIELDS_UPDATED_RENDERED_REVIEW_PENDING'
        document=$DocumentPath
        pages=$taskDoc.ComputeStatistics(2)
        words=$taskDoc.ComputeStatistics(0)
        tables=$taskDoc.Tables.Count
        inline_shapes=$taskDoc.InlineShapes.Count
        equations=$taskDoc.OMaths.Count
        toc=$taskDoc.TablesOfContents.Count
        paragraphs=$taskParagraphs
        fields=$taskFields
        sections=$taskSections
        pdf=$taskPdf
    }
    $taskResult | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'word-readback.json') -Encoding UTF8
    [ordered]@{pages=$taskResult.pages;tables=$taskResult.tables;equations=$taskResult.equations;toc=$taskResult.toc;pdf=$taskPdf} | ConvertTo-Json
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0) }
    if ($null -ne $taskWord -and $taskWord.Documents.Count -eq 0) { $taskWord.Quit() }
}
