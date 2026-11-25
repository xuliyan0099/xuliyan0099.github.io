$src = 'D:\Workspace\MainPage\imx6ull\rm\c14.html'
$out = Join-Path $env:TEMP 'chk14.html'
$html = Get-Content $src -Raw
$probe = @'
<script>
window.onerror = function(m, u, l){ document.title = 'JSERR ' + m + ' @' + l; };
(function(){
try {
var reps=[];
for (var s=0;s<5;s++){
  state.step=s; draw();
  var rects=[].slice.call(scene.querySelectorAll('rect'));
  var texts=[].slice.call(scene.querySelectorAll('text'));
  texts.forEach(function(t){
    var b=t.getBBox();
    if(b.x<20||b.x+b.width>1900||b.y<88||b.y+b.height>974) reps.push('OUT|'+t.textContent.slice(0,14));
    rects.forEach(function(r){
      var rx=+r.getAttribute('x'), ry=+r.getAttribute('y'), rw=+r.getAttribute('width'), rh=+r.getAttribute('height');
      if(rw<120||rh<24) return;
      var ix = Math.min(b.x+b.width, rx+rw) - Math.max(b.x, rx);
      var iy = Math.min(b.y+b.height, ry+rh) - Math.max(b.y, ry);
      if(ix<=0||iy<=0) return;
      var fully = (b.x>=rx-2 && b.x+b.width<=rx+rw+3 && b.y>=ry-12 && b.y+b.height<=ry+rh+3);
      if(!fully) reps.push('CROSS S'+s+'|'+t.textContent.slice(0,14)+'|dx'+Math.round(ix)+'|dy'+Math.round(iy));
    });
  });
  for(var i=0;i<texts.length;i++) for(var j=i+1;j<texts.length;j++){
    var a=texts[i].getBBox(), c=texts[j].getBBox();
    var ox=Math.min(a.x+a.width,c.x+c.width)-Math.max(a.x,c.x);
    var oy=Math.min(a.y+a.height,c.y+c.height)-Math.max(a.y,c.y);
    if(ox>3&&oy>3){ var ar=Math.min(a.width*a.height,c.width*c.height); if(ox*oy>0.25*ar) reps.push('TXT2 S'+s+'|'+texts[i].textContent.slice(0,10)+'×'+texts[j].textContent.slice(0,10)); }
  }
}
document.title='CHK['+reps.length+'] : '+reps.slice(0,30).join(' ;; ');
} catch(e){ document.title='ERR '+e.message; }
})();
</script>
</body>
'@
$html = $html.Replace('</body>', $probe)
[IO.File]::WriteAllText($out, $html, (New-Object System.Text.UTF8Encoding($false)))
$outF = Join-Path $env:TEMP 'dump14.txt'
$u = 'file:///' + $out.Replace('\','/')
cmd /c "`"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`" --headless=new --disable-gpu --no-sandbox --virtual-time-budget=4000 --user-data-dir=%TEMP%\dw14f --dump-dom `"$u`" > `"$outF`" 2>nul"
$all = Get-Content $outF -Raw
[regex]::Match($all,'<title>.*?</title>').Value
