$ErrorActionPreference = 'Stop'
$projectRoot = 'D:\Hoctap\bigdata\Detaituan8910'
$destination = Join-Path $projectRoot '.agent\qa\phase4-app-20261009\windows-runtime.json'
if (Test-Path -LiteralPath $destination) { throw 'Evidence exists; do not overwrite' }
$checks = @()
foreach ($item in @(@{ Name = 'dashboard'; Url = 'http://localhost:8501/_stcore/health' }, @{ Name = 'flink'; Url = 'http://localhost:8081/overview' })) {
    $response = Invoke-WebRequest -Uri $item.Url -UseBasicParsing -TimeoutSec 10
    $checks += @{ name = "Windows_localhost_$($item.Name)"; passed = ($response.StatusCode -eq 200); details = $response.Content }
}
$listeners = @(Get-NetTCPConnection -State Listen -LocalPort 8501,8081 | Select-Object LocalAddress,LocalPort)
$checks += @{ name = 'Windows_loopback_listeners'; passed = ($listeners.Count -ge 2 -and @($listeners | Where-Object LocalAddress -notin @('127.0.0.1','::1')).Count -eq 0); details = $listeners }
$wslState = (& wsl.exe --list --verbose | Out-String).Replace([string][char]0,'').Trim()
$checks += @{ name = 'WSL2_fresh_invocation'; passed = ($wslState -match 'Ubuntu-24.04\s+Running\s+2'); details = $wslState }
$volumes = @(Get-CimInstance Win32_LogicalDisk | Where-Object DeviceID -in @('C:','D:') | Select-Object DeviceID,FreeSpace,Size)
$report = @{ status = 'VERIFIED'; checks = $checks; passed = @($checks | Where-Object passed).Count; total_checks = $checks.Count; captured_at = (Get-Date).ToString('o'); physical_volumes = $volumes; cold_wsl_boot = 'NOT_TESTED; no shutdown or Windows restart'; autostart = 'NOT_IMPLEMENTED; foreground holders required' }
if (@($checks | Where-Object { -not $_.passed }).Count) { $report.status = 'FAIL' }
[System.IO.File]::WriteAllText($destination, ($report | ConvertTo-Json -Depth 8), [System.Text.UTF8Encoding]::new($false))
$report | ConvertTo-Json -Depth 8
if ($report.status -eq 'FAIL') { exit 1 }
