$src = 'D:\Workspace\MainPage\imx6ull\rm\c13.html'
$tail = 'D:\Workspace\MainPage\_rmch17\c17_tail.html'
$out = 'D:\Workspace\MainPage\imx6ull\rm\c17.html'

$html = Get-Content $src -Raw
$cut = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

$new = [regex]::Replace($new, '<title>[^<]*</title>', '<title>RM 第 17 章 · NAND 纠错加速器 BCH | i.MX6ULL 逐章解读</title>')
$new = [regex]::Replace($new, '<h1[^>]*>[^<]*</h1>', '<h1>第 17 章 · NAND 纠错加速器 BCH</h1>')
$new = [regex]::Replace($new, '<span class="bd-hint">[^<]*</span>', '<span class="bd-hint">纠错 / 布局 / 环路</span>')

$newTexts = @('纠错能力', '2–40 位', '页布局', '4 套')
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

$new = [regex]::Replace($new, 'href="c1[0-9].html" style="text-decoration:none">← RM1[0-9]', 'href="c16.html" style="text-decoration:none">← RM16')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length
[regex]::Match($new, '<title>.*?</title>').Value
[regex]::Matches($new, '← RM1[0-9]').Value
