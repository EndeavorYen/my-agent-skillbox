#Requires -Version 5.1
param(
    [Parameter(Position = 0)]
    [ValidateSet('grok', 'claude', 'cursor', 'all')]
    [string]$Platform = 'all'
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillSrc = Join-Path $RepoRoot 'SKILL.md'
$ReadmeSrc = Join-Path $RepoRoot 'README.md'
$HelperSrc = Join-Path $RepoRoot 'scripts\grill-log.py'
if (-not (Test-Path -LiteralPath $SkillSrc)) {
    throw "SKILL.md not found at $SkillSrc"
}
if (-not (Test-Path -LiteralPath $HelperSrc)) {
    throw "scripts/grill-log.py not found at $HelperSrc"
}

function Get-UserHome {
    if ($env:USERPROFILE) { return $env:USERPROFILE }
    return $HOME
}

function Get-Dest([string]$Name) {
    $homeDir = Get-UserHome
    switch ($Name) {
        'grok' {
            $root = if ($env:GROK_HOME) { $env:GROK_HOME } else { Join-Path $homeDir '.grok' }
            return (Join-Path $root 'skills\gentle-grill-me')
        }
        'claude' { return (Join-Path $homeDir '.claude\skills\gentle-grill-me') }
        'cursor' { return (Join-Path $homeDir '.cursor\skills\gentle-grill-me') }
        default { throw "Unknown platform $Name" }
    }
}

function Install-To([string]$Name) {
    $dest = Get-Dest $Name
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -Force -LiteralPath $SkillSrc -Destination (Join-Path $dest 'SKILL.md')
    if (Test-Path -LiteralPath $ReadmeSrc) {
        Copy-Item -Force -LiteralPath $ReadmeSrc -Destination (Join-Path $dest 'README.md')
    }
    if (Test-Path -LiteralPath $HelperSrc) {
        $scriptsDest = Join-Path $dest 'scripts'
        New-Item -ItemType Directory -Force -Path $scriptsDest | Out-Null
        Copy-Item -Force -LiteralPath $HelperSrc -Destination (Join-Path $scriptsDest 'grill-log.py')
    }
    Write-Output "Installed $Name -> $dest"
}

$targets = if ($Platform -eq 'all') { @('grok', 'claude', 'cursor') } else { @($Platform) }
foreach ($t in $targets) { Install-To $t }
