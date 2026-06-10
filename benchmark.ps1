$ErrorActionPreference = 'Stop'

python "$PSScriptRoot\run_benchmark.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
