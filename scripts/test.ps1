$ErrorActionPreference = 'Stop'

$VCVARS = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
$CTEST  = "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\ctest.exe"
$BUILD  = "$(Split-Path $PSScriptRoot -Parent)\build"

cmd /c "call `"$VCVARS`" x64 && cd /d `"$BUILD`" && `"$CTEST`" --output-on-failure -C Release"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
