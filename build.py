#!/usr/bin/env python3
"""Builds index.html (bilingual loader + PWA) from src/app-es.html and src/app-en.html.

Usage: python3 build.py
Also bumps the service-worker cache version so installed apps pick up the update.
"""
import base64, re, pathlib

ROOT = pathlib.Path(__file__).parent
PWAHEAD = '''<meta name="theme-color" content="#0f3d2e">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Hi-Lo">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
'''
PWAJS = '''<script>
(function(){
  if('serviceWorker' in navigator){ navigator.serviceWorker.register('sw.js').catch(function(){}); }
  var deferred=null, b=document.getElementById('install');
  window.addEventListener('beforeinstallprompt',function(e){ e.preventDefault(); deferred=e; b.style.display=''; });
  b.addEventListener('click',function(){ if(!deferred) return; deferred.prompt(); deferred.userChoice.finally(function(){ deferred=null; b.style.display='none'; }); });
  window.addEventListener('appinstalled',function(){ b.style.display='none'; });
})();
</script>
</body>'''
LOADER = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="Andres Guanipa">
<meta name="copyright" content="© 2026 Andres Guanipa">
<meta name="description" content="Hi-Lo card counting trainer for blackjack (English / Español).">
%(head)s<title>Hi-Lo Trainer · Entrenador Hi-Lo</title>
<style>html,body{margin:0;background:#0f3d2e}</style>
</head>
<body>
<script>
(function(){
  var DOCS={es:"%(es)s",en:"%(en)s"};
  function dec(b){ var bin=atob(b), u=new Uint8Array(bin.length); for(var i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return new TextDecoder('utf-8').decode(u); }
  function pick(){
    try{ var l=localStorage.getItem('hilo-lang'); if(l==='es'||l==='en') return l; }catch(e){}
    return ((navigator.language||'')+'').toLowerCase().indexOf('es')===0?'es':'en';
  }
  function render(l){ var h=dec(DOCS[l]); document.open(); document.write(h); document.close(); }
  window.__hiloSetLang=function(l){
    try{ localStorage.setItem('hilo-lang',l); }catch(e){}
    try{ location.reload(); }catch(e){}
    setTimeout(function(){ render(l); },500);
  };
  render(pick());
})();
</script>
</body>
</html>
'''

def pwaify(s, label):
    v = '<meta name="viewport" content="width=device-width, initial-scale=1">'
    s = s.replace(v, v + '\n' + PWAHEAD.rstrip('\n'), 1)
    s = s.replace('  </header>', '    <button class="btn primary" id="install" style="display:none;margin-top:10px;width:100%">' + label + '</button>\n  </header>', 1)
    i = s.rindex('</body>')
    return s[:i] + PWAJS + s[i + len('</body>'):]

def b64(x):
    return base64.b64encode(x.encode('utf-8')).decode()

es = pwaify((ROOT / 'src/app-es.html').read_text(encoding='utf-8'), 'Instalar app')
en = pwaify((ROOT / 'src/app-en.html').read_text(encoding='utf-8'), 'Install app')
(ROOT / 'index.html').write_text(LOADER % {'head': PWAHEAD, 'es': b64(es), 'en': b64(en)}, encoding='utf-8')

sw = (ROOT / 'sw.js').read_text(encoding='utf-8')
n = int(re.search(r"hilo-v(\d+)", sw).group(1)) + 1
(ROOT / 'sw.js').write_text(re.sub(r"hilo-v\d+", "hilo-v%d" % n, sw), encoding='utf-8')
print('index.html built · cache hilo-v%d' % n)
