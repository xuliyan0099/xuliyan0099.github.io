$root = 'D:\Workspace\MainPage'
for ($n = 36; $n -le 41; $n++) {
  $p = Join-Path $root ("imx6ull\rm\c{0}.html" -f $n)
  $s = [IO.File]::ReadAllText($p)
  $anchor = '<a class="bd-btn" href="c{0}.html" style="text-decoration:none">← RM{1}</a>' -f $n, ($n - 1)
  $fwd = ' <a class="bd-btn" href="c{0}.html" style="text-decoration:none">RM{1} →</a>' -f ($n + 1), ($n + 1)
  if (-not $s.Contains($anchor)) { "MISS $n" ; continue }
  $s = $s.Replace($anchor, $anchor + $fwd)
  [IO.File]::WriteAllText($p, $s, (New-Object System.Text.UTF8Encoding($false)))
  "link c$n -> c$($n + 1) ok"
}
