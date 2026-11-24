param([string]$file = 'c15.html', [int]$steps = 5, [string]$dir = 'shots_rm15')
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$base = Get-Content "D:\Workspace\MainPage\imx6ull\rm\$file" -Raw
$shots = 'C:\Users\xuliy\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.sessions\38454808404882434\agents\m_0cwefOa3Zi7\' + $dir
New-Item -ItemType Directory -Force -Path $shots | Out-Null
$tmp = Join-Path $env:TEMP ('shots_' + $file)
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
foreach ($i in 0..($steps - 1)) {
  $html2 = $base.Replace('var INIT = { step: 0, lane: 0 };', "var INIT = { step: $i, lane: 0 };")
  $f = Join-Path $tmp ("t$i.html")
  [IO.File]::WriteAllText($f, $html2, (New-Object System.Text.UTF8Encoding($false)))
  $u = 'file:///' + $f.Replace('\', '/')
  & $edge --headless=new --disable-gpu --hide-scrollbars --window-size=1600,900 --user-data-dir="$tmp\w$i" --screenshot="$shots\t$i.png" $u 2>$null | Out-Null
}
Get-ChildItem $shots -Filter *.png | Select-Object Name, Length
