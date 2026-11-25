$p = 'D:\Workspace\MainPage\imx6ull\rm\c36.html'
$s = [IO.File]::ReadAllText($p)
$i = $s.IndexOf('href="c35.html"')
$seg = $s.Substring($i - 60, 140)
$seg
$codes = ($seg.ToCharArray() | ForEach-Object { [int][char]$_ }) -join ','
$codes
