$src = 'D:\Workspace\MainPage\imx6ull\rm\c10.html'
$tail = 'D:\Workspace\MainPage\_rmch11\c11_tail.html'
$out = 'D:\Workspace\MainPage\imx6ull\rm\c11.html'

$html = Get-Content $src -Raw
$cut = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

$new = [regex]::Replace($new, '<title>[^<]*</title>', '<title>RM 第 11 章 · 系统安全总览与信任链 | i.MX6ULL 逐章解读</title>')
$new = [regex]::Replace($new, '<h1[^>]*>[^<]*</h1>', '<h1>第 11 章 · 系统安全</h1>')
$new = [regex]::Replace($new, '<span class="bd-hint">[^<]*</span>', '<span class="bd-hint">信任链 / CSU / 防拆 / 熔丝</span>')

$txts = @('验签算法', 'RSA-4096', '权限档位', '8 级')
$pattern = '<span class="bd-reading-(?:name|value)">[^<]*</span>'
$sb = New-Object System.Text.StringBuilder
$idx = 0
foreach ($m in [regex]::Matches($new, $pattern)) {
  [void]$sb.Append($new.Substring($idx, $m.Index - $idx))
  $val = $txts[$script:k++]
  $cls = if (($m.Value) -match 'bd-reading-name') { 'name' } else { 'value' }
  [void]$sb.Append('<span class="bd-reading-' + $cls + '">' + $val + '</span>')
  $idx = $m.Index + $m.Length
}
[void]$sb.Append($new.Substring($idx))
$new = $sb.ToString()

$new = $new.Replace('href="c09.html" style="text-decoration:none">← RM09', 'href="c10.html" style="text-decoration:none">← RM10')
$new = [regex]::Replace($new, '<a[^>]*>\s*RM\s*11\s*→?\s*</a>', '')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length

$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$shots = 'C:\Users\xuliy\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38454808404882434\agents\m_0cwefOa3Zi7\shots_rm11'
New-Item -ItemType Directory -Force -Path $shots | Out-Null
New-Item -ItemType Directory -Force -Path "$env:TEMP\rm11test" | Out-Null
$base = Get-Content $out -Raw
foreach ($i in 0..4) {
  $html = $base.Replace('var INIT = { step: 0, lane: 0 };', "var INIT = { step: $i, lane: 0 };")
  $f = "$env:TEMP\rm11test\t$i.html"
  [IO.File]::WriteAllText($f, $html, (New-Object System.Text.UTF8Encoding($false)))
  & $edge --headless=new --disable-gpu --hide-scrollbars --window-size=1600,900 --user-data-dir="$env:TEMP\rm11w$i" --screenshot="$shots\t$i.png" ("file:///" + $f.Replace('\', '/')) 2>$null | Out-Null
}
'shots done'
