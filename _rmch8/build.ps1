$c7 = Get-Content 'D:\Workspace\MainPage\imx6ull\rm\c07.html' -Raw
$cut = $c7.IndexOf('var $ = function (id)')
$stag = $c7.LastIndexOf('<script>', $cut)
$prefix = $c7.Substring(0, $stag)
$tail = Get-Content 'D:\Workspace\MainPage\_rmch8\c08_tail.html' -Raw
$prefix = $prefix.Replace('<title>RM07 调试架构：JTAG、DAP、CTI 与 OnCE</title>', '<title>RM08 系统启动：从 ROM 到第一条指令</title>')
$prefix = $prefix.Replace('<h1 class="bd-title">第 7 章 · 调试架构</h1>', '<h1 class="bd-title">第 8 章 · 系统启动</h1>')
$prefix = $prefix.Replace('<span class="bd-reading-name">JTAG ID</span>', '<span class="bd-reading-name">启动模式</span>')
$prefix = $prefix.Replace('<span class="bd-reading-value">0x0891_E01D</span>', '<span class="bd-reading-value">010b</span>')
$prefix = $prefix.Replace('<span class="bd-reading-name">JTAG 引脚</span>', '<span class="bd-reading-name">IVT 偏移</span>')
$prefix = $prefix.Replace('<span class="bd-reading-value">5 根</span>', '<span class="bd-reading-value">0x400</span>')
$prefix = $prefix.Replace('href="c06.html"', 'href="c07.html"').Replace('← RM06', '← RM07')
$out = 'D:\Workspace\MainPage\imx6ull\rm\c08.html'
[IO.File]::WriteAllText($out, $prefix + $tail, (New-Object System.Text.UTF8Encoding($false)))
Write-Output ('built: ' + (Get-Item $out).Length)

$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$shotDir = 'C:\Users\xuliy\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38454808404882434\agents\m_0cwefOa3Zi7\shots_rm8'
New-Item -ItemType Directory -Force -Path $shotDir | Out-Null
New-Item -ItemType Directory -Force -Path "$env:TEMP\rm8test" | Out-Null
$base = Get-Content $out -Raw
foreach ($i in 0..4) {
  $html = $base.Replace('var INIT = { step: 0, dev: 2 };', "var INIT = { step: $i, dev: 2 };")
  $f = "$env:TEMP\rm8test\w$i.html"
  [IO.File]::WriteAllText($f, $html, (New-Object System.Text.UTF8Encoding($false)))
  & $edge --headless=new --disable-gpu --hide-scrollbars --window-size=1600,900 --user-data-dir="$env:TEMP\rm8w$i" --screenshot="$shotDir\w$i.png" ("file:///" + $f.Replace('\', '/')) 2>$null | Out-Null
}
Get-ChildItem $shotDir -Filter w*.png | Select-Object Name, Length | Format-Table -AutoSize
