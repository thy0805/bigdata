param([string]$InputDoc, [string]$JsonPath)
$ErrorActionPreference = 'Stop'
$taskWord = $null
$taskDoc = $null
function Find-TaskParagraph([string]$Style, [string]$Needle) {
    foreach ($taskP in $taskDoc.Paragraphs) {
        if ($taskP.Style.NameLocal -eq $Style -and $taskP.Range.Text.Contains($Needle)) { return $taskP.Range.Duplicate }
    }
    throw 'Target not found'
}
try {
    $taskWord = New-Object -ComObject Word.Application
    $taskAlerts = $taskWord.DisplayAlerts
    $taskSecurity = $taskWord.AutomationSecurity
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskDoc = $taskWord.Documents.Open($InputDoc, $false, $true, $false)
    $taskResults = @()
    foreach ($taskCase in @(@('TableCaption','Một số câu hỏi phân tích','Table',3,'Table'), @('FigureCaption','Định hướng tiếp cận','Figure',2,'Figure'))) {
        $taskTarget = Find-TaskParagraph $taskCase[0] $taskCase[1]
        $taskInsert = $taskDoc.Range($taskTarget.Start, $taskTarget.Start)
        $taskLabel = if ($taskCase[2] -eq 'Table') { 'Bảng ' } else { 'Hình ' }
        $taskInsert.InsertBefore($taskLabel + '#.*. QA SEQ probe' + [char]13)
        $taskProbe = Find-TaskParagraph $taskCase[0] 'QA SEQ probe'
        $taskProbe.Style = $taskDoc.Styles.Item($taskCase[0])
        $taskRange = $taskProbe.Duplicate
        $taskRange.Find.ClearFormatting()
        $taskRange.Find.Execute('#') | Out-Null
        $taskDoc.Fields.Add($taskRange,-1,'STYLEREF "ChapterTitle" \n \t',$false) | Out-Null
        $taskProbe = Find-TaskParagraph $taskCase[0] 'QA SEQ probe'
        $taskRange = $taskProbe.Duplicate
        $taskRange.Find.ClearFormatting()
        $taskRange.Find.MatchWildcards = $false
        $taskRange.Find.Execute('*') | Out-Null
        $taskDoc.Fields.Add($taskRange,-1,('SEQ ' + $taskCase[2] + ' \s 1'),$false) | Out-Null
        $taskDoc.Fields.Update() | Out-Null
        $taskDoc.TablesOfContents.Item([int]$taskCase[3]).Update()
        $taskShifted = (Find-TaskParagraph $taskCase[0] $taskCase[1]).Text.TrimEnd([char]13,[char]7)
        $taskListFound = $taskDoc.TablesOfContents.Item([int]$taskCase[3]).Range.Text.Contains('QA SEQ probe')
        (Find-TaskParagraph $taskCase[0] 'QA SEQ probe').Delete() | Out-Null
        $taskDoc.Fields.Update() | Out-Null
        $taskDoc.TablesOfContents.Item([int]$taskCase[3]).Update()
        $taskRestored = (Find-TaskParagraph $taskCase[0] $taskCase[1]).Text.TrimEnd([char]13,[char]7)
        $taskResults += [ordered]@{type=$taskCase[2];shifted=$taskShifted;restored=$taskRestored;list_detects_added_caption=$taskListFound;list_removes_deleted_caption=(!$taskDoc.TablesOfContents.Item([int]$taskCase[3]).Range.Text.Contains('QA SEQ probe'))}
    }
    $taskChecks = [ordered]@{table_seq_increments=($taskResults[0].shifted -match '^Bảng 1\.3\.');table_seq_restores=($taskResults[0].restored -match '^Bảng 1\.2\.');figure_seq_increments=($taskResults[1].shifted -match '^Hình 1\.2\.');figure_seq_restores=($taskResults[1].restored -match '^Hình 1\.1\.');both_lists_detect_added=($taskResults[0].list_detects_added_caption -and $taskResults[1].list_detects_added_caption);both_lists_remove_deleted=($taskResults[0].list_removes_deleted_caption -and $taskResults[1].list_removes_deleted_caption)}
    [ordered]@{changes_saved=$false;results=$taskResults;checks=$taskChecks} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $JsonPath -Encoding utf8
    $taskChecks | ConvertTo-Json
    if ($taskChecks.Values -contains $false) { throw 'Caption probe failed' }
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0) }
    if ($null -ne $taskWord) {
        $taskWord.DisplayAlerts = $taskAlerts
        $taskWord.AutomationSecurity = $taskSecurity
        if ($taskWord.Documents.Count -eq 0) { $taskWord.Quit() }
    }
}
