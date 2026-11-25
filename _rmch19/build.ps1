$src  = 'D:\Workspace\MainPage\imx6ull\rm\c18.html'
$tail = 'D:\Workspace\MainPage\_rmch19\c19_tail.html'
$out  = 'D:\Workspace\MainPage\imx6ull\rm\c19.html'

$html = Get-Content $src -Raw
$cut  = $html.IndexOf('var $ = function (id)')
$stag = $html.LastIndexOf('<script>', $cut)
$prefix = $html.Substring(0, $stag)

$t = Get-Content $tail -Raw
$new = $prefix + $t

# 只替换文档头那一个 title（不要碰 SVG 里的 <title>）
$i = $new.IndexOf('<title>'); $j = $new.IndexOf('</title>')
$new = $new.Substring(0, $i) + '<title>RM 第 19 章 · 摄像头接口 CSI | i.MX6ULL 逐章解读</title>' + $new.Substring($j + 8)

# 只替换第一个 h1
$i = $new.IndexOf('<h1'); $j = $new.IndexOf('>', $i); $k = $new.IndexOf('</h1>')
$new = $new.Substring(0, $i) + '<h1>第 19 章 · 摄像头接口 CSI</h1>' + $new.Substring($k + 5)

# 标题栏那句副标题
$new = [regex]::Replace($new, '<span class="bd-hint">[^<]*</span>', '<span class="bd-hint">并行接口 / 打包 / DMA</span>')

# 四个读数：名称 / 值 交替
$newTexts = @('寄存器基址', '0x021C_4000', 'RX FIFO', '128 字')
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
$new = $new.Replace('href="c17.html" style="text-decoration:none">← RM17', 'href="c18.html" style="text-decoration:none">← RM18')

[IO.File]::WriteAllText($out, $new, (New-Object System.Text.UTF8Encoding($false)))
'built: ' + (Get-Item $out).Length
[regex]::Match($new, '<title>[^<]*</title>').Value
[regex]::Matches($new, '← RM1[0-9]').Value
([regex]::Matches($new, 'bd-reading-(?:name|value)')).Count
