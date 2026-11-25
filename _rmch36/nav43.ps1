$root = 'D:\Workspace\MainPage'
$la = [string][char]8592
$ra = [string][char]8594
$dirAnchor = '<a class="bd-btn" href="index.html" style="display:inline-flex;align-items:center;justify-content:center;text-decoration:none">' + [string][char]9776 + ' 目录</a>'
for ($n = 43; $n -le 60; $n++) {
  $p = Join-Path $root ("imx6ull\rm\c{0}.html" -f $n)
  $s = [IO.File]::ReadAllText($p)
  if ($s.Contains('href="c' + ($n - 1) + '.html"')) { "SKIP $n (already has nav)"; continue }
  if (-not $s.Contains($dirAnchor)) { "MISS $n no dir anchor"; continue }
  $prev = $n - 1
  $nav = ('<a class="bd-btn" href="c{0}.html" style="text-decoration:none">' -f $prev) + $la + (' RM{0}</a>' -f $prev)
  if ($n -lt 60) {
    $next = $n + 1
    $nav = $nav + (' <a class="bd-btn" href="c{0}.html" style="text-decoration:none">' -f $next) + ('RM{0} ' -f $next) + $ra + '</a>'
  }
  $s = $s.Replace($dirAnchor, $nav + "`n        " + $dirAnchor)
  [IO.File]::WriteAllText($p, $s, (New-Object System.Text.UTF8Encoding($false)))
  "nav c$n ok"
}
