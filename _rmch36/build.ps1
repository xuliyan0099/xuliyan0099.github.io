param([int]$num,[string]$title,[string]$h1,[string]$r1n,[string]$r1v,[string]$r2n,[string]$r2v)
$root = 'D:\Workspace\MainPage'
$src  = Join-Path $root ('imx6ull\rm\c{0:d2}.html' -f ($num-1))
$tail = Join-Path $root ('_rmch{0}\c{0}_tail.html' -f $num)
$out  = Join-Path $root ('imx6ull\rm\c{0}.html' -f $num)
$html = Get-Content $src -Raw
$cut  = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)
$t = Get-Content $tail -Raw
$new = $prefix + $t
$i = $new.IndexOf('<title>'); $j = $new.IndexOf('</title>')
$new = $new.Substring(0, $i) + '<title>' + $title + '</title>' + $new.Substring($j + 8)
$i = $new.IndexOf('<h1'); $k = $new.IndexOf('</h1>')
$new = $new.Substring(0, $i) + '<h1>' + $h1 + '</h1>' + $new.Substring($k + 5)
$newTexts = @($r1n,$r1v,$r2n,$r2v)
$pattern = '<span class="bd-reading-(?:name|value)">[\s\S]*?</span>'
$sb = New-Object System.Text.StringBuilder
$pos = 0; $n = 0
foreach ($m in [regex]::Matches($new, $pattern)) {
  [void]$sb.Append($new.Substring($pos, $m.Index - $pos))
  $cls = if ($m.Value -match 'bd-reading-name') { 'name' } else { 'value' }
  $v = if ($n -lt 4) { $newTexts[$n] } else { '' }
  [void]$sb.Append('<span class="bd-reading-' + $cls + '">' + $v + '</span>')
  $pos = $m.Index + $m.Length; $n++
}
[void]$sb.Append($new.Substring($pos))
$new = $sb.ToString()
$prev = $num - 1
$prevLink = '<a class="bd-btn" href="c' + ('{0:d2}' -f $prev) + '.html" style="text-decoration:none">← RM' + ('{0:d2}' -f $prev) + '</a>'
$new = [regex]::Replace($new, '<a class="bd-btn" href="c\d+\.html" style="text-decoration:none">← RM\d+</a>', { param($m) $prevLink })
$new = [regex]::Replace($new, ' <a class="bd-btn" href="c\d+\.html" style="text-decoration:none">RM\d+ →</a>', '')
[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built ' + $out + ' ' + (Get-Item $out).Length
'title: ' + [regex]::Match($new, '<title>[^<]*</title>').Value
'h1: ' + [regex]::Match($new, '<h1>[^<]*</h1>').Value
'nav: ' + [regex]::Matches($new, 'RM\d\d').Value -join ','
'readings: ' + ([regex]::Matches($new, 'bd-reading-value">[^<]*').Value -join ' | ')