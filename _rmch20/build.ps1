$src  = 'D:\Workspace\MainPage\imx6ull\rm\c19.html'
$tail = 'D:\Workspace\MainPage\_rmch20\c20_tail.html'
$out  = 'D:\Workspace\MainPage\imx6ull\rm\c20.html'

$html = Get-Content $src -Raw
$cut  = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

$i = $new.IndexOf('<title>'); $j = $new.IndexOf('</title>')
$new = $new.Substring(0, $i) + '<title>RM 第 20 章 · 增强可配置 SPI (ECSPI) | i.MX6ULL 逐章解读</title>' + $new.Substring($j + 8)

$i = $new.IndexOf('<h1'); $j = $new.IndexOf('>', $i); $k = $new.IndexOf('</h1>')
$new = $new.Substring(0, $i) + '<h1>第 20 章 · 增强可配置 SPI（ECSPI）</h1>' + $new.Substring($k + 5)

$new = [regex]::Replace($new, '<span class="bd-hint">[^<]*</span>', '<span class="bd-hint">四线全双工 / 分频 / 片选</span>')

$newTexts = @('寄存器基址', '0x0200_8000', 'FIFO 深度', '64×32')
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

$new = $new.Replace('href="c18.html" style="text-decoration:none">← RM18', 'href="c19.html" style="text-decoration:none">← RM19')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length
[regex]::Match($new, '<title>[^<]*</title>').Value
[regex]::Matches($new, '← RM1[0-9]').Value
[regex]::Matches($new, '<span class="bd-reading-(?:name|value)">[^<]*</span>').Count
