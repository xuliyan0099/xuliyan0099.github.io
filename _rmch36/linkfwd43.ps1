$root = 'D:\Workspace\MainPage'
$la = [string][char]8592
$ra = [string][char]8594
foreach ($n in 42..44) {
  $p = Join-Path $root ("imx6ull\rm\c{0}.html" -f $n)
  $s = [IO.File]::ReadAllText($p)
  $prev = $n - 1
  $next = $n + 1
  $anchor = ('<a class="bd-btn" href="c{0}.html" style="text-decoration:none">' -f $prev) + $la + (' RM{0}</a>' -f $prev)
  $fwd = (' <a class="bd-btn" href="c{0}.html" style="text-decoration:none">' -f $next) + ('RM{0} ' -f $next) + $ra + '</a>'
  if ($s.Contains($fwd)) { "SKIP $n" ; continue }
  if (-not $s.Contains($anchor)) { "MISS $n" ; continue }
  $s = $s.Replace($anchor, $anchor + $fwd)
  [IO.File]::WriteAllText($p, $s, (New-Object System.Text.UTF8Encoding($false)))
  "link c$n -> c$next ok"
}
