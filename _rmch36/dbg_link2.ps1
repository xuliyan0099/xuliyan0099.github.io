$p = 'D:\Workspace\MainPage\imx6ull\rm\c36.html'
$s = [IO.File]::ReadAllText($p)
$n = 36
$la = [string][char]8592
$ra = [string][char]8594
$anchor = '<a class="bd-btn" href="c{0}.html" style="text-decoration:none">' -f $n + $la + ' RM' + ($n - 1) + '</a>'
"anchor=" + $anchor
"contains=" + $s.Contains($anchor)
$fwd = ' <a class="bd-btn" href="c{0}.html" style="text-decoration:none">RM{1} ' -f ($n + 1), ($n + 1) + $ra + '</a>'
"fwd=" + $fwd
