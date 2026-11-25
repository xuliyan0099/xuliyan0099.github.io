$root = 'D:\Workspace\MainPage'
$la = [string][char]8592   # left arrow
$ra = [string][char]8594   # right arrow
for ($n = 36; $n -le 41; $n++) {
  $p = Join-Path $root ("imx6ull\rm\c{0}.html" -f $n)
  $s = [IO.File]::ReadAllText($p)
  $anchor = '<a class="bd-btn" href="c{0}.html" style="text-decoration:none">' + $la + ' RM' + ($n - 1) + '</a>'
  $fwd = ' <a class="bd-btn" href="c{0}.html" style="text-decoration:none">RM{1} ' -f ($n + 1), ($n + 1) + $ra + '</a>'
  if (-not $s.Contains($anchor)) { "MISS $n" ; continue }
  $s = $s.Replace($anchor, $anchor + $fwd)
  [IO.File]::WriteAllText($p, $s, (New-Object System.Text.UTF8Encoding($false)))
  "link c$n -> c$($n + 1) ok"
}
