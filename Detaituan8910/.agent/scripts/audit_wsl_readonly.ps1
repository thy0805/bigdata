param([Parameter(Mandatory=$true)][string]$OutputPath)

$ErrorActionPreference = 'Stop'
$phaseOut = [IO.Path]::GetFullPath($OutputPath)
$phaseQaRoot = 'D:\Hoctap\bigdata\Detaituan8910\.agent\qa\phase0-20261008\'
if (-not $phaseOut.StartsWith($phaseQaRoot, [StringComparison]::OrdinalIgnoreCase)) { throw 'Output must stay in the phase 0 QA directory.' }
if (Test-Path -LiteralPath $phaseOut) { throw 'Output already exists; use a new filename.' }

function Get-PhaseNativeVersion([string]$Path, [string]$Arguments) {
    if (-not (Test-Path -LiteralPath $Path)) { return [ordered]@{path=$Path;exists=$false} }
    $phaseInfo = [Diagnostics.ProcessStartInfo]::new()
    $phaseInfo.FileName = $Path
    $phaseInfo.Arguments = $Arguments
    $phaseInfo.UseShellExecute = $false
    $phaseInfo.CreateNoWindow = $true
    $phaseInfo.RedirectStandardOutput = $true
    $phaseInfo.RedirectStandardError = $true
    $phaseProcess = [Diagnostics.Process]::new()
    $phaseProcess.StartInfo = $phaseInfo
    try {
        [void]$phaseProcess.Start()
        $phaseStdout = $phaseProcess.StandardOutput.ReadToEndAsync()
        $phaseStderr = $phaseProcess.StandardError.ReadToEndAsync()
        $phaseExited = $phaseProcess.WaitForExit(10000)
        if (-not $phaseExited) {
            $phaseProcess.Kill()
            $phaseProcess.WaitForExit()
        }
        return [ordered]@{path=$Path;exists=$true;timed_out=(-not $phaseExited);exit_code=$phaseProcess.ExitCode;stdout=$phaseStdout.Result.Trim();stderr=$phaseStderr.Result.Trim()}
    } finally { $phaseProcess.Dispose() }
}

$phaseOs = Get-CimInstance Win32_OperatingSystem
$phaseComputer = Get-CimInstance Win32_ComputerSystem
$phaseCpu = Get-CimInstance Win32_Processor
$phaseWindows = Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
$phaseFeatureNames = @('VirtualMachinePlatform','HypervisorPlatform','Microsoft-Windows-Subsystem-Linux')
$phaseFeatures = @(Get-CimInstance Win32_OptionalFeature | Where-Object { $_.Name -in $phaseFeatureNames } | Select-Object Name,InstallState)
$phaseServiceNames = @('WslService','WslInstaller','LxssManager','vmcompute','msiserver')
$phaseServices = @(Get-CimInstance Win32_Service | Where-Object { $_.Name -in $phaseServiceNames } | Select-Object Name,State,StartMode,PathName)
$phasePackages = @(Get-AppxPackage | Where-Object { $_.Name -match 'WindowsSubsystemForLinux|Ubuntu|Debian' })
$phasePackageResults = foreach ($phasePkg in $phasePackages) {
    $phaseManifestPath = Join-Path $phasePkg.InstallLocation 'AppxManifest.xml'
    $phaseManifest = Get-Content -LiteralPath $phaseManifestPath -Raw
    [ordered]@{name=$phasePkg.Name;version=[string]$phasePkg.Version;full_name=$phasePkg.PackageFullName;location=$phasePkg.InstallLocation;status=[string]$phasePkg.Status;manifest_sha256=(Get-FileHash -LiteralPath $phaseManifestPath -Algorithm SHA256).Hash;has_installer_service=($phaseManifest -match 'Service Name="WslInstaller"');has_installer_class=($phaseManifest -match 'B5AEB4C3-9541-492F-AD4D-505951F6ADA4');files=@(Get-ChildItem -LiteralPath $phasePkg.InstallLocation | Select-Object Name,Length)}
}

$phaseRegistryPaths = @(
    'Registry::HKEY_CLASSES_ROOT\CLSID\{B5AEB4C3-9541-492F-AD4D-505951F6ADA4}',
    'HKLM:\SOFTWARE\Classes\PackagedCom\ClassIndex\{B5AEB4C3-9541-492F-AD4D-505951F6ADA4}',
    'HKCU:\SOFTWARE\Classes\PackagedCom\ClassIndex\{B5AEB4C3-9541-492F-AD4D-505951F6ADA4}',
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss\MSI',
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss'
)
$phaseRegistry = foreach ($phaseReg in $phaseRegistryPaths) { [ordered]@{path=$phaseReg;exists=(Test-Path -LiteralPath $phaseReg)} }
$phaseUninstallRoots = @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall','HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
$phaseUninstall = @(foreach ($phaseReg in $phaseUninstallRoots) { Get-ChildItem -LiteralPath $phaseReg -ErrorAction SilentlyContinue | Get-ItemProperty | Where-Object { $_.DisplayName -match 'Windows Subsystem for Linux|WSL' } | Select-Object DisplayName,DisplayVersion,InstallLocation,Publisher })
$phaseInstaller = $null
try {
    $phaseInstaller = New-Object -ComObject WindowsInstaller.Installer
    $phaseComResult = [ordered]@{success=$true;install_method_called=$false}
} catch { $phaseComResult = [ordered]@{success=$false;hresult=$_.Exception.HResult;message=$_.Exception.Message;install_method_called=$false} }
finally { if ($phaseInstaller) { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($phaseInstaller) } }

try { $phaseDeviceGuard = @(Get-CimInstance -Namespace 'root\Microsoft\Windows\DeviceGuard' -ClassName Win32_DeviceGuard | Select-Object VirtualizationBasedSecurityStatus,SecurityServicesRunning,AvailableSecurityProperties) }
catch { $phaseDeviceGuard = [ordered]@{query_error=$_.Exception.Message} }
$phaseRuntime = @(
    (Get-PhaseNativeVersion 'C:\Users\thy\miniconda3\python.exe' '-V'),
    (Get-PhaseNativeVersion 'C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe' '-version'),
    (Get-PhaseNativeVersion 'C:\Program Files\Android\Android Studio\jbr\bin\java.exe' '-version')
)
$phaseFiles = foreach ($phasePath in @('C:\Windows\System32\wsl.exe','C:\Windows\System32\msiexec.exe')) { $phaseItem = Get-Item -LiteralPath $phasePath; [ordered]@{path=$phasePath;file_version=$phaseItem.VersionInfo.FileVersion;sha256=(Get-FileHash -LiteralPath $phasePath -Algorithm SHA256).Hash} }
$phaseSourcePaths = @('C:\Users\thy\Downloads\individual+household+electric+power+consumption.zip','D:\Hoctap\bigdata\Detaituan8910\BaoCao_PhanTich_DuDoan_DienNang_UCI_QA_v3_20261008.docx')
$phaseSourceHashes = foreach ($phasePath in $phaseSourcePaths) { [ordered]@{path=$phasePath;sha256=(Get-FileHash -LiteralPath $phasePath -Algorithm SHA256).Hash} }

$phaseResult = [ordered]@{
    captured_at=(Get-Date).ToString('o')
    powershell_version=$PSVersionTable.PSVersion.ToString()
    process_64bit=[Environment]::Is64BitProcess
    is_admin=([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    os=($phaseOs | Select-Object Caption,Version,BuildNumber,OSArchitecture,TotalVisibleMemorySize,FreePhysicalMemory)
    windows=($phaseWindows | Select-Object DisplayVersion,UBR,EditionID)
    host=($phaseComputer | Select-Object HypervisorPresent,Manufacturer,Model,TotalPhysicalMemory)
    cpu=($phaseCpu | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,VirtualizationFirmwareEnabled,VMMonitorModeExtensions,SecondLevelAddressTranslationExtensions)
    optional_features=$phaseFeatures
    services=$phaseServices
    service_names_not_found=@($phaseServiceNames | Where-Object { $_ -notin $phaseServices.Name })
    appx_packages=@($phasePackageResults)
    registry=$phaseRegistry
    wsl_msi_folder_exists=(Test-Path -LiteralPath 'C:\Program Files\WSL')
    wsl_uninstall_entries=$phaseUninstall
    windows_installer_com=$phaseComResult
    device_guard=$phaseDeviceGuard
    versions=$phaseRuntime
    system_files=@($phaseFiles)
    commands=@(Get-Command python,java,wsl,docker,flink -ErrorAction SilentlyContinue | Select-Object Name,Source,CommandType)
    disks=@(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | Select-Object DeviceID,Size,FreeSpace)
    source_hashes=@($phaseSourceHashes)
    safety=[ordered]@{wsl_executed=$false;installed_anything=$false;changed_registry=$false;changed_features=$false;rebooted=$false}
}
$phaseJson = $phaseResult | ConvertTo-Json -Depth 9
[IO.File]::WriteAllText($phaseOut, $phaseJson, [Text.UTF8Encoding]::new($false))
Write-Output $phaseJson
