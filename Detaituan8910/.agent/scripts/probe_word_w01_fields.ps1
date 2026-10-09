param([string]$DocumentPath, [string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$taskHashBefore = (Get-FileHash -LiteralPath $DocumentPath -Algorithm SHA256).Hash
$taskProbePath = Join-Path $OutputDirectory 'W01-field-probe.docx'
Copy-Item -LiteralPath $DocumentPath -Destination $taskProbePath
$taskWord = $null
$taskDoc = $null
$taskChecks = @()
function Add-TaskCheck([string]$Id, [bool]$Pass, $Evidence) {
    $script:taskChecks += [ordered]@{id=$Id;status=$(if ($Pass) {'PASS'} else {'FAIL'});evidence=$Evidence}
}
function Update-TaskFields {
    $script:taskDoc.Fields.Update() | Out-Null
    foreach ($taskToc in $script:taskDoc.TablesOfContents) { $taskToc.Update() }
    $script:taskDoc.Repaginate()
}
try {
    $taskWord = New-Object -ComObject Word.Application
    $taskWord.Visible = $false
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskDoc = $taskWord.Documents.Open($taskProbePath, $false, $false, $false)
    $taskCaptionBefore = @($taskDoc.Paragraphs | Where-Object {$_.Style.NameLocal -in @('TableCaption','FigureCaption')} | ForEach-Object {$_.Range.Text.Trim()})
    foreach ($taskKind in @('Table','Figure')) {
        $taskKey = $(if ($taskKind -eq 'Table') {'T31'} else {'F31'})
        $taskNext = $(if ($taskKind -eq 'Table') {'T32'} else {'F32'})
        $taskLocation = $(if ($taskKind -eq 'Table') {$taskDoc.Tables.Item(8).Range.End} else {$taskDoc.Bookmarks.Item("W01_$taskKey").Range.Paragraphs.Item(1).Range.End})
        $taskRange = $taskDoc.Range($taskLocation,$taskLocation)
        $taskRange.Text = "PROBE_$taskKind`r"
        $taskParagraph = $taskDoc.Range($taskLocation,$taskLocation+1).Paragraphs.Item(1)
        $taskParagraph.Style = $(if ($taskKind -eq 'Table') {'TableCaption'} else {'FigureCaption'})
        $taskInsert = $taskDoc.Range($taskParagraph.Range.End-1,$taskParagraph.Range.End-1)
        $taskDoc.Fields.Add($taskInsert,-1,('SEQ '+$taskKind+' \s 1'),$false) | Out-Null
        Update-TaskFields
        $taskResult = $taskDoc.Bookmarks.Item("W01_$taskNext").Range.Text.Trim()
        Add-TaskCheck "$taskKind-insert-increments-next-caption" ($taskResult -match '3\.3$') $taskResult
        $taskParagraph.Range.Delete() | Out-Null
        Update-TaskFields
        $taskRestored = $taskDoc.Bookmarks.Item("W01_$taskNext").Range.Text.Trim()
        Add-TaskCheck "$taskKind-delete-restores-caption" ($taskRestored -match '3\.2$') $taskRestored
    }
    $taskChapterFirst = @($taskDoc.Paragraphs | Where-Object {$_.Style.NameLocal -eq 'Heading 21' -and $_.Range.ListFormat.ListString -eq '3.1.'})[0]
    $taskLocation = $taskChapterFirst.Range.Start
    $taskRange = $taskDoc.Range($taskLocation,$taskLocation)
    $taskRange.Text = "PROBE_HEADING`r"
    $taskParagraph = $taskDoc.Range($taskLocation,$taskLocation+1).Paragraphs.Item(1)
    $taskParagraph.Style = 'Heading 21'
    Update-TaskFields
    $taskHeadingLabel = $taskParagraph.Range.ListFormat.ListString
    $taskExisting = @($taskDoc.Paragraphs | Where-Object {$_.Style.NameLocal -eq 'Heading 21' -and $_.Range.Text.StartsWith('GIỚI THIỆU BỘ DỮ LIỆU UCI')})[0]
    if ($null -eq $taskExisting) {
        $taskExisting = @($taskDoc.Paragraphs | Where-Object {$_.Style.NameLocal -eq 'Heading 21' -and $_.Range.Text.ToUpper().StartsWith('GIỚI THIỆU BỘ DỮ LIỆU UCI')})[0]
    }
    Add-TaskCheck 'heading-insert-stable-numbering' ($taskHeadingLabel -eq '3.1.' -and $taskExisting.Range.ListFormat.ListString -eq '3.2.') @{inserted=$taskHeadingLabel;existing=$taskExisting.Range.ListFormat.ListString}
    $taskParagraph.Range.Delete() | Out-Null
    Update-TaskFields
    Add-TaskCheck 'heading-delete-restores-numbering' ($taskExisting.Range.ListFormat.ListString -eq '3.1.') $taskExisting.Range.ListFormat.ListString
    $taskCaptionAfter = @($taskDoc.Paragraphs | Where-Object {$_.Style.NameLocal -in @('TableCaption','FigureCaption')} | ForEach-Object {$_.Range.Text.Trim()})
    Add-TaskCheck 'all-caption-results-restored' (($taskCaptionBefore -join "`n") -eq ($taskCaptionAfter -join "`n")) @{count=$taskCaptionAfter.Count}
    $taskErrors = @($taskDoc.Fields | Where-Object {$_.Result.Text -match 'Error!|Lỗi!'})
    Add-TaskCheck 'toc-lists-and-refs-no-errors-after-probe' ($taskErrors.Count -eq 0 -and $taskDoc.TablesOfContents.Count -eq 3) @{errors=$taskErrors.Count;toc=$taskDoc.TablesOfContents.Count}
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0) }
    if ($null -ne $taskWord -and $taskWord.Documents.Count -eq 0) { $taskWord.Quit() }
    $taskHashAfter = (Get-FileHash -LiteralPath $DocumentPath -Algorithm SHA256).Hash
    Add-TaskCheck 'final-artifact-unchanged-by-probe' ($taskHashBefore -eq $taskHashAfter) @{before=$taskHashBefore;after=$taskHashAfter}
    $taskResult = [ordered]@{status=$(if (@($taskChecks | Where-Object {$_.status -eq 'FAIL'}).Count -eq 0 -and $taskChecks.Count -eq 9) {'PASS'} else {'FAIL_OR_INCOMPLETE'});scope='Only QA copy opened and edited; final artifact byte hash unchanged';checks=$taskChecks}
    $taskResult | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'field-probe.json') -Encoding UTF8
    $taskResult | ConvertTo-Json -Depth 8
}
