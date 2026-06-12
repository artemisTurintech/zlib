param(
    [int]$Runs = 10
)
$ErrorActionPreference = 'Stop'

python "$(Split-Path $PSScriptRoot -Parent)\run_benchmark.py" --runs $Runs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
