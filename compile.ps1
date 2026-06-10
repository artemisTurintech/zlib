$ErrorActionPreference = 'Stop'

$VCVARS = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
$CMAKE  = "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
$NINJA  = "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe"
$ROOT   = $PSScriptRoot

cmd /c "call `"$VCVARS`" x64 && `"$CMAKE`" -S `"$ROOT`" -B `"$ROOT\build`" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_MAKE_PROGRAM=`"$NINJA`" && `"$CMAKE`" --build `"$ROOT\build`""
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
