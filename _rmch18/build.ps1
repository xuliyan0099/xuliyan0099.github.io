$src  = 'D:\Workspace\MainPage\imx6ull\rm\c17.html'
$tail = 'D:\Workspace\MainPage\_rmch18\c18_tail.html'
$out  = 'D:\Workspace\MainPage\imx6ull\rm\c18.html'

$html = Get-Content $src -Raw
$cut  = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

# 只替换文档头那一个 title（不要碰 SVG 里的 <title>）
$i = $new.IndexOf('<title>'); $j = $new.IndexOf('</title>')
$new = $new.Substring(0, $i) + '<title>RM 第 18 章 · 时钟控制器 CCM | i.MX6ULL 逐章解读</title>' + $new.Substring($j + 8)

# 只替换第一个 h1
$i = $new.IndexOf('<h1'); $j = $new.IndexOf('>', $i); $k = $new.IndexOf('</h1>')
$new = $new.Substring(0, $i) + '<h1>第 18 章 · 时钟控制器 CCM</h1>' + $new.Substring($k + 5)

# 标题栏那句副标题
$new = [regex]::Replace($new, '<span class="bd-hint">[^<]*</span>', '<span class="bd-hint">时钟树 / 分频 / 门控</span>')

# 四个读数：名称 / 值 交替
$newTexts = @('时钟源', '24 M + 32 k', '时钟根', '7 PLL · 18 根')
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

# 上一章链接
$new = $new.Replace('href="c16.html" style="text-decoration:none">← RM16', 'href="c17.html" style="text-decoration:none">← RM17')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length
[regex]::Match($new, '<title>[^<]*</title>').Value
[regex]::Matches($new, '← RM1[0-9]').Value
([regex]::Matches($new, 'bd-reading-(?:name|value)')).Count
