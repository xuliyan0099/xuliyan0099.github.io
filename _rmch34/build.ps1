$src  = 'D:\Workspace\MainPage\imx6ull\rm\c33.html'
$tail = 'D:\Workspace\MainPage\_rmch34\c34_tail.html'
$out  = 'D:\Workspace\MainPage\imx6ull\rm\c34.html'

$html = Get-Content $src -Raw
$cut  = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

$i = $new.IndexOf('<title>'); $j = $new.IndexOf('</title>')
$new = $new.Substring(0, $i) + '<title>RM 第 34 章 · RGB 屏接口 eLCDIF | i.MX6ULL 逐章解读</title>' + $new.Substring($j + 8)

$i = $new.IndexOf('<h1'); $j = $new.IndexOf('>', $i); $k = $new.IndexOf('</h1>')
$new = $new.Substring(0, $i) + '<h1>第 34 章 · RGB 屏接口（eLCDIF）</h1>' + $new.Substring($k + 5)

$newTexts = @('eLCDIF 基址', '0x021C_8000', '像素时钟', 'pix_clk 独立')
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

$new = [regex]::Replace($new, '<a class="bd-btn" href="c32\.html"[^>]*>← RM32</a>', '<a class="bd-btn" href="c33.html" style="text-decoration:none">← RM33</a>')
$new = [regex]::Replace($new, '<a class="bd-btn" href="c34\.html"[^>]*>RM34 →</a>', '')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length
[regex]::Match($new, '<title>[^<]*</title>').Value
[regex]::Match($new, '<h1>[^<]*</h1>').Value
[regex]::Matches($new, 'RM3[0-9]').Value
