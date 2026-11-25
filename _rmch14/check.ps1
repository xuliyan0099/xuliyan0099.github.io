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
     rects.forEach(function(r){
       var rx=+r.getAttribute('x'), ry=+r.getAttribute('y'), rw=+r.getAttribute('width'), rh=+r.getAttribute('height');
       if(rw<120||rh<24) return;
       var cx=b.x+b.width/2, cy=b.y+b.height/2;
       if(cx>rx-10 && cx<rx+rw+10 && cy>ry-6 && cy<ry+rh+6){
         var oR=(b.x+b.width)-(rx+rw), oB=(b.y+b.height)-(ry+rh), oL=rx-b.x, oT=ry-b.y;
         if(oR>2||oB>2||oL>2||oT>2) reps.push('S'+s+'|'+t.textContent.slice(0,16)+'|R'+Math.round(oR)+'|B'+Math.round(oB)+'|L'+Math.round(oL)+'|T'+Math.round(oT));
       }
     });
   });
 }
 document.title='OVF['+reps.length+'] : '+reps.join(' ;; ');
 } catch(e) { document.title = 'ERR ' + e.message; }
})();
</script>
</body>
'@
$html = $html.Replace('</body>', $probe)
[IO.File]::WriteAllText($out, $html, (New-Object System.Text.UTF8Encoding($false)))
$outF = Join-Path $env:TEMP 'dump14.txt'
$u = 'file:///' + $out.Replace('\','/')
cmd /c "`"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`" --headless=new --disable-gpu --no-sandbox --virtual-time-budget=3000 --user-data-dir=%TEMP%\dw14c --dump-dom `"$u`" > `"$outF`" 2>nul"
$all = Get-Content $outF -Raw
$m = [regex]::Match($all, '<title>(.*?)</title>')
$m.Groups[1].Value.Substring(0, [Math]::Min(1200, $m.Groups[1].Value.Length))
