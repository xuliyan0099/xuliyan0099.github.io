$src = 'D:\Workspace\MainPage\imx6ull\rm\c11.html'
$tail = 'D:\Workspace\MainPage\_rmch12\c12_tail.html'
$out = 'D:\Workspace\MainPage\imx6ull\rm\c12.html'

$html = Get-Content $src -Raw
$cut = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

$new = [regex]::Replace($new, '<title>[^<]*</title>', '<title>RM 第 12 章 · Cortex-A7 平台配置 | i.MX6ULL 逐章解读</title>')
$new = [regex]::Replace($new, '<h1[^>]*>[^<]*</h1>', '<h1>第 12 章 · A7 平台配置</h1>')
$new = [regex]::Replace($new, '<span class="bd-hint">[^<]*</span>', '<span class="bd-hint">核 / 缓存 / GIC / 总线</span>')

$newTexts = @('L2 缓存', '128 KB', '共享中断', '128 个')
$pattern = '<span class="bd-reading-(?:name|value)">[^<]*</span>'
$sb = New-Object System.Text.StringBuilder
$pos = 0
$n = 0
foreach ($m in [regex]::Matches($new, $pattern)) {
  [void]$sb.Append($new.Substring($pos, $m.Index - $pos))
  $cls = if ($m.Value -match 'bd-reading-name') { 'name' } else { 'value' }
  [void]$sb.Append('<span class="bd-reading-' + $cls + '">' + $newTexts[$n] + '</span>')
  $pos = $m.Index + $m.Length
  $n++
}
[void]$sb.Append($new.Substring($pos))
$new = $sb.ToString()

$new = $new.Replace('href="c10.html" style="text-decoration:none">← RM10', 'href="c11.html" style="text-decoration:none">← RM11')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length

$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$shots = 'C:\Users\xuliy\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38454808404882434\agents\m_0cwefOa3Zi7\shots_rm12'
New-Item -ItemType Directory -Force -Path $shots | Out-Null
New-Item -ItemType Directory -Force -Path "$env:TEMP\rm12test" | Out-Null
$base = Get-Content $out -Raw
foreach ($i in 0..4) {
  $html2 = $base.Replace('var INIT = { step: 0, lane: 0 };', "var INIT = { step: $i, lane: 0 };")
  $f = "$env:TEMP\rm12test\t$i.html"
  [IO.File]::WriteAllText($f, $html2, (New-Object System.Text.UTF8Encoding($false)))
  & $edge --headless=new --disable-gpu --hide-scrollbars --window-size=1600,900 --user-data-dir="$env:TEMP\rm12w$i" --screenshot="$shots\t$i.png" ("file:///" + $f.Replace('\', '/')) 2>$null | Out-Null
}
'shots done'
