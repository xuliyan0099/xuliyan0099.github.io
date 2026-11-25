$src = 'D:\Workspace\MainPage\imx6ull\rm\c08.html'
$raw = Get-Content $src -Raw
$cut = $raw.IndexOf('var $ = function (id)')
$stag = $raw.LastIndexOf('<script>', $cut)
$prefix = $raw.Substring(0, $stag)
$tail = Get-Content 'D:\Workspace\MainPage\_rmch10\c10_tail.html' -Raw

$prefix = [regex]::Replace($prefix, '<title>[^<]*</title>', '<title>RM10 时钟与电源：七个 PLL 与六个稳压器</title>')
$prefix = [regex]::Replace($prefix, '<h1 class="bd-title">[^<]*</h1>', '<h1 class="bd-title">第 10 章 · 时钟与电源管理</h1>')

# 依次替换 4 个 reading span（名称1、值1、名称2、值2）
$newTexts = @('核心频率', '528 MHz', 'PLL 数量', '7 个')
$pattern = '<span class="bd-reading-(?:name|value)">[^<]*</span>'
$sb = New-Object System.Text.StringBuilder
$pos = 0
$n = 0
foreach ($m in [regex]::Matches($prefix, $pattern)) {
  [void]$sb.Append($prefix.Substring($pos, $m.Index - $pos))
  $cls = if ($m.Value -match 'bd-reading-name') { 'name' } else { 'value' }
  [void]$sb.Append('<span class="bd-reading-' + $cls + '">' + $newTexts[$n] + '</span>')
  $pos = $m.Index + $m.Length
  $n++
}
[void]$sb.Append($prefix.Substring($pos))
$prefix = $sb.ToString()

# 首章按钮：只留"← RM09"，删掉前进按钮
$prefix = [regex]::Replace($prefix, '<a class="bd-btn" href="c07\.html" style="text-decoration:none">← RM07</a>', '<a class="bd-btn" href="c09.html" style="text-decoration:none">← RM09</a>')
$prefix = [regex]::Replace($prefix, '\s*<a class="bd-btn" href="c09\.html" style="display:inline-flex;align-items:center;justify-content:center;text-decoration:none">RM09 →</a>', '')

$out = 'D:\Workspace\MainPage\imx6ull\rm\c10.html'
[IO.File]::WriteAllText($out, $prefix + $tail, (New-Object System.Text.UTF8Encoding($false)))
Write-Output ('built: ' + (Get-Item $out).Length)

$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$shotDir = 'C:\Users\xuliy\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38454808404882434\agents\m_0cwefOa3Zi7\shots_rm10'
New-Item -ItemType Directory -Force -Path "$env:TEMP\rm10test" | Out-Null
$base = Get-Content $out -Raw
foreach ($i in 0..4) {
  $html = $base.Replace('var INIT = { step: 0, lane: 0 };', "var INIT = { step: $i, lane: 0 };")
  $f = "$env:TEMP\rm10test\t$i.html"
  [IO.File]::WriteAllText($f, $html, (New-Object System.Text.UTF8Encoding($false)))
  & $edge --headless=new --disable-gpu --hide-scrollbars --window-size=1600,900 --user-data-dir="$env:TEMP\rm10w$i" --screenshot="$shotDir\t$i.png" ("file:///" + $f.Replace('\', '/')) 2>$null | Out-Null
}
Write-Output 'shots done'
