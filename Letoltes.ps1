# Andersen – Windows telepítő letöltő
# A legfrissebb GitHub-kiadásból letölti a Windows telepítőt, ellenőrzi, majd elindítja.
# Nem igényel Node.js-t, Pythont vagy Gitet – csak a beépített Windows PowerShellt.

[CmdletBinding()]
param(
    [switch]$Quiet
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$repo = 'diablomike20/Andersen'
$api = "https://api.github.com/repos/$repo/releases/latest"
$headers = @{
    'User-Agent' = 'Andersen-Downloader'
    'Accept'     = 'application/vnd.github+json'
}

function Write-Step([string]$Message) {
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Fail([string]$Message) {
    Write-Host ''
    Write-Host "HIBA: $Message" -ForegroundColor Red
    exit 1
}

try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
} catch {
    # Régebbi .NET-verzión a TLS 1.2 beállítása nem kötelező.
}

Write-Step 'A legfrissebb Andersen-kiadás keresése...'
try {
    $release = Invoke-RestMethod -Uri $api -Headers $headers -UseBasicParsing
} catch {
    Fail "Nem sikerült elérni a GitHubot. Ellenőrizd az internetkapcsolatot. ($($_.Exception.Message))"
}

$assets = @($release.assets)
$installer = $assets | Where-Object { $_.name -match '_x64-setup\.exe$' } | Select-Object -First 1
if (-not $installer) {
    $installer = $assets | Where-Object { $_.name -match '\.msi$' } | Select-Object -First 1
}
if (-not $installer) {
    Fail "A legfrissebb kiadásban nincs Windows-telepítő. Nézd meg: https://github.com/$repo/releases"
}

Write-Host "   Verzió: $($release.tag_name)"
Write-Host "   Fájl:   $($installer.name)"

$downloadDir = Join-Path $env:TEMP 'Andersen-Setup'
New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null
$target = Join-Path $downloadDir $installer.name

Write-Step 'Letöltés...'
try {
    Invoke-WebRequest -Uri $installer.browser_download_url -OutFile $target -UseBasicParsing
} catch {
    Fail "A letöltés nem sikerült: $($_.Exception.Message)"
}

# Ha a GitHub megadja a SHA-256 lenyomatot, ellenőrizzük a letöltött fájlt.
$expected = $null
if ($installer.digest -and $installer.digest -match '^sha256:([0-9a-fA-F]{64})$') {
    $expected = $Matches[1].ToLowerInvariant()
}
if ($expected) {
    Write-Step 'A letöltött fájl ellenőrzése...'
    $actual = (Get-FileHash -Path $target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $expected) {
        Remove-Item -Force $target
        Fail 'A letöltött fájl sérült (ellenőrzőösszeg-eltérés).'
    }
    Write-Host '   Ellenőrzőösszeg rendben.'
}

Write-Step 'Telepítő indítása...'
Write-Host '   A telepítőablakban válaszd ki a telepítés helyét, majd kattints a Telepítés gombra.'
Start-Process -FilePath $target -Wait

Write-Host ''
Write-Host 'Kész! Az Andersen a Start menüből vagy az asztali parancsikonról indítható.' -ForegroundColor Green
