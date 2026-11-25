$src  = 'D:\Workspace\MainPage\imx6ull\rm\c31.html'
$tail = 'D:\Workspace\MainPage\_rmch32\c32_tail.html'
$out  = 'D:\Workspace\MainPage\imx6ull\rm\c32.html'

$html = Get-Content $src -Raw
$cut  = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

$i = $new.IndexOf('<title>'); $j = $new.IndexOf('</title>')
$new = $new.Substring(0, $i) + '<title>RM 第 32 章 · IOMUX 控制器 (IOMUXC) | i.MX6ULL 逐章解读</title>' + $new.Substring($j + 8)

$i = $new.IndexOf('<h1'); $j = $new.IndexOf('>', $i); $k = $new.IndexOf('</h1>')
$new = $new.Substring(0, $i) + '<h1>第 32 章 · IOMUX 控制器（IOMUXC）</h1>' + $new.Substring($k + 5)

$newTexts = @('IOMUXC 基址', '0x020E_0000', '焊盘', '最多 8 个 ALT')
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

$new = [regex]::Replace($new, '<a class="bd-btn" href="c30\.html"[^>]*>← RM30</a>', '<a class="bd-btn" href="c31.html" style="text-decoration:none">← RM31</a>')
$new = [regex]::Replace($new, '<a class="bd-btn" href="c32\.html"[^>]*>RM32 →</a>', '')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length
[regex]::Match($new, '<title>[^<]*</title>').Value
[regex]::Match($new, '<h1>[^<]*</h1>').Value
[regex]::Matches($new, '← RM3[0-9]').Value
