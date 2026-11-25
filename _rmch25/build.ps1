$src  = 'D:\Workspace\MainPage\imx6ull\rm\c24.html'
$tail = 'D:\Workspace\MainPage\_rmch25\c25_tail.html'
$out  = 'D:\Workspace\MainPage\imx6ull\rm\c25.html'

$html = Get-Content $src -Raw
$cut  = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

$i = $new.IndexOf('<title>'); $j = $new.IndexOf('</title>')
$new = $new.Substring(0, $i) + '<title>RM 第 25 章 · 增强型串行音频接口 (ESAI) | i.MX6ULL 逐章解读</title>' + $new.Substring($j + 8)

$i = $new.IndexOf('<h1'); $j = $new.IndexOf('>', $i); $k = $new.IndexOf('</h1>')
$new = $new.Substring(0, $i) + '<h1>第 25 章 · 增强型串行音频接口（ESAI）</h1>' + $new.Substring($k + 5)

$newTexts = @('寄存器基址', '0x0202_4000', '收发通道', '6 发 / 4 收')
$pattern = '<span class="bd-reading-(?:name|value)">[^<]*</span>'
$sb = New-Object System.Text.StringBuilder
$pos = 0; $n = 0
foreach ($m in [regex]::Matches($new, $pattern)) {
  [void]$sb.Append($new.Substring($pos, $m.Index - $pos))
  $cls = if ($m.Value -match 'bd-reading-name') { 'name' } else { 'value' }
  [void]$sb.Append('<span class="bd-reading-' + $cls + '">' + $newTexts[$n] + '</span>')
  $pos = $m.Index + $m.Length; $n++
}
[void]$sb.Append($new.Substring($pos))
$new = $sb.ToString()

$new = [regex]::Replace($new, '<a class="bd-btn" href="c23\.html"[^>]*>← RM23</a>', '<a class="bd-btn" href="c24.html" style="text-decoration:none">← RM24</a>')
$new = [regex]::Replace($new, '<a class="bd-btn" href="c25\.html"[^>]*>RM25 →</a>', '')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length
[regex]::Match($new, '<title>[^<]*</title>').Value
[regex]::Match($new, '<h1>[^<]*</h1>').Value
[regex]::Matches($new, '← RM2[0-9]').Value
[regex]::Matches($new, 'RM2[0-9] →').Value
