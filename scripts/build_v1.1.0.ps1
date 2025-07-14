# 飞机大战游戏 v1.1.0 Nuitka 编译脚本
Write-Host "🚀 飞机大战游戏 v1.1.0 Nuitka 编译" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

Write-Host "🧹 清理旧文件..." -ForegroundColor Yellow
if (Test-Path "PlaneWars_v1.1.0.exe") { Remove-Item "PlaneWars_v1.1.0.exe" }
if (Test-Path "main.build") { Remove-Item "main.build" -Recurse -Force }
if (Test-Path "main.dist") { Remove-Item "main.dist" -Recurse -Force }
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }

Write-Host "🔨 开始编译 v1.1.0 版本..." -ForegroundColor Cyan

$nuitkaArgs = @(
    "--onefile"
    "--windows-disable-console"
    "--output-filename=PlaneWars_v1.1.0"
    "--assume-yes-for-downloads"
    "--plugin-enable=numpy"
    "--include-package=pygame"
    "--include-package=numpy"
    "--include-module=sound_manager"
    "--include-module=config"
    "--include-module=player"
    "--include-module=enemy"
    "--include-module=bullet"
    "--include-module=item"
    "--include-module=game"
    "--windows-company-name=PlaneWars Game"
    "--windows-product-name=PlaneWars v1.1.0"
    "--windows-file-version=1.1.0.0"
    "--windows-product-version=1.1.0"
    "--windows-file-description=飞机大战游戏 v1.1.0"
    "main.py"
)

python -m nuitka @nuitkaArgs

if (Test-Path "PlaneWars_v1.1.0.exe") {
    Write-Host "✅ 编译成功！" -ForegroundColor Green
    Write-Host "📁 可执行文件: PlaneWars_v1.1.0.exe" -ForegroundColor Green
    
    $fileSize = (Get-Item "PlaneWars_v1.1.0.exe").Length / 1MB
    Write-Host "📊 文件大小: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Green
    
    Write-Host "📦 创建发布目录..." -ForegroundColor Yellow
    $releaseDir = "..\releases\release_clean_v1.1.0"
    if (!(Test-Path $releaseDir)) { 
        New-Item -ItemType Directory -Path $releaseDir -Force 
    }
    
    Copy-Item "PlaneWars_v1.1.0.exe" $releaseDir
    Copy-Item "..\README.md" $releaseDir
    Copy-Item "..\docs\CHANGELOG.md" $releaseDir
    Copy-Item "..\requirements.txt" $releaseDir
    
    Write-Host "✅ 发布包创建完成！" -ForegroundColor Green
    Write-Host "📂 发布目录: $releaseDir" -ForegroundColor Green
} else {
    Write-Host "❌ 编译失败！" -ForegroundColor Red
}

Write-Host "按任意键继续..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
