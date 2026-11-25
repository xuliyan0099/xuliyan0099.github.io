$p = 'D:\Workspace\MainPage\imx6ull\rm\c36.html'
$s = [IO.File]::ReadAllText($p)
$la = [string][char]8592
$anchor = '<a class="bd-btn" href="c35.html" style="text-decoration:none">' + $la + ' RM35</a>'
"anchorLen=" + $anchor.Length
"containsAnchor=" + $s.Contains($anchor)
"idxPlain=" + $s.IndexOf('<a class="bd-btn" href="c35.html"')
$i = $s.IndexOf('<a class="bd-btn" href="c35.html"')
$real = $s.Substring($i, $anchor.Length)
"sameLen=" + ($real.Length -eq $anchor.Length)
for ($k = 0; $k -lt $anchor.Length; $k++) {
  if ($real[$k] -ne $anchor[$k]) { "diffAt $k real=" + [int][char]$real[$k] + " want=" + [int][char]$anchor[$k] }
}
