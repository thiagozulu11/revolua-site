from pathlib import Path
import re,html,json
root=Path(__file__).parent
classes=set()
def convert(file,prefix):
 s=(root/file).read_text()
 images={}
 for name,url in re.findall(r'const (\w+) = "(https:[^"]+)";',s):
  images[name]='assets/'+('office.jpg' if 'FotoNaOperacao' in name else 'portrait.jpg' if 'RetratoInstitucional' in name else ('logo-desktop.png' if prefix=='d' else 'logo.png') if 'Logotipo' in name else prefix+'-'+name+'.svg')
 components=dict(re.findall(r'function (\w+)\([^\n]*\) \{\s*return \((.*?)\n  \);\n\}',s,re.S))
 main=re.search(r'export default function \w+\(\) \{\s*return \((.*?)\n  \);\n\}',s,re.S).group(1)
 def expand(m):
  name,attrs=m.group(1),m.group(2)
  out=components[name]
  override=re.search(r'className="([^"]*)"',attrs)
  out=re.sub(r'className=\{className \|\| "([^"]*)"\}',lambda m:'className="'+(override.group(1) if override else m.group(1))+'"',out)
  return out
 while re.search(r'<(Revolua\w+)\b([^>]*)/>',main):main=re.sub(r'<(Revolua\w+)\b([^>]*)/>',expand,main)
 main=re.sub(r'\{`([^`]*)`\}',lambda m:html.escape(m.group(1)),main)
 main=re.sub(r'src=\{(\w+)\}',lambda m:'src="'+images[m.group(1)]+'"',main)
 main=re.sub(r'style=\{\{ backgroundImage: "([^"]*)" \}\}',lambda m:'style="background-image:'+m.group(1)+'"',main)
 main=main.replace('className=','class=').replace('alt=""','alt="" loading="lazy"').replace('target="_blank"','target="_blank" rel="noopener noreferrer"')
 main=main.replace('word-break:break-word','word-break:normal')
 main=re.sub(r'<(div|p|span)\b([^>]*?)/>',r'<\1\2></\1>',main)
 for a in re.findall(r'class="([^"]*)"',main):classes.update(a.split())
 # Separate the fixed navigation from the document flow.
 node='3:8' if prefix=='d' else '3:112'
 found=re.search(r'<div\b[^>]*data-node-id="'+node+r'"[^>]*>',main)
 start=found.start();depth=1;end=found.end()
 for m in re.finditer(r'<(/?)div\b[^>]*>',main[found.end():]):
  depth+=-1 if m.group(1) else 1
  if depth==0:end=found.end()+m.end();break
 nav=main[start:end];main=main[:start]+main[end:]
 return main,nav
desktop,desktopnav=convert('figma-reference.tsx','d')
mobile,mobilenav=convert('figma-mobile-reference.tsx','m')
def rule(c):
 fixed={'relative':'position:relative','absolute':'position:absolute','flex':'display:flex','block':'display:block','flex-col':'flex-direction:column','items-start':'align-items:flex-start','items-center':'align-items:center','justify-between':'justify-content:space-between','justify-center':'justify-content:center','justify-end':'justify-content:flex-end','shrink-0':'flex-shrink:0','content-stretch':'align-content:stretch','overflow-clip':'overflow:hidden','pointer-events-none':'pointer-events:none','max-w-none':'max-width:none','min-w-px':'min-width:1px','w-px':'width:1px','h-px':'height:1px','w-full':'width:100%','size-full':'width:100%;height:100%','inset-0':'inset:0','left-0':'left:0','right-0':'right:0','top-0':'top:0','mb-0':'margin-bottom:0','opacity-0':'opacity:0','text-center':'text-align:center','text-left':'text-align:left','text-white':'color:#fff','bg-white':'background-color:#fff','font-bold':'font-weight:700','font-medium':'font-weight:500','font-normal':'font-weight:400','border':'border-width:1px','border-solid':'border-style:solid','object-cover':'object-fit:cover','object-contain':'object-fit:contain','whitespace-pre-wrap':'white-space:pre-wrap','cursor-pointer':'cursor:pointer','flex-[1_0_0]':'flex:1 0 0'}
 fixed['text-right']='text-align:right'
 fixed.update({'col-1':'grid-column:1','row-1':'grid-row:1','inline-grid':'display:inline-grid','place-items-start':'place-items:start','ml-0':'margin-left:0','mt-0':'margin-top:0','overflow-hidden':'overflow:hidden'})
 if c in fixed:return fixed[c]
 if c.startswith("font-['Montserrat"):return "font-family:Montserrat,Arial,sans-serif"
 m=re.fullmatch(r'\[([^:]+):([^]]+)\]',c)
 if m:return m[1]+':'+m[2]
 m=re.fullmatch(r'([a-z-]+)-\[(.*)\]',c)
 if not m:raise ValueError('Unsupported class '+c)
 p,v=m.groups();v=v.replace('_',' ')
 props={'w':'width','h':'height','size':'width','gap':'gap','leading':'line-height','tracking':'letter-spacing','left':'left','right':'right','top':'top','bottom':'bottom','bg':'background-color','border':'border-color','rounded':'border-radius','rounded-tl':'border-top-left-radius','rounded-tr':'border-top-right-radius','rounded-bl':'border-bottom-left-radius','rounded-br':'border-bottom-right-radius','p':'padding','pt':'padding-top','pb':'padding-bottom','pl':'padding-left','pr':'padding-right','backdrop-blur':'backdrop-filter','drop-shadow':'filter'}
 if p=='px':return f'padding-left:{v};padding-right:{v}'
 if p=='py':return f'padding-top:{v};padding-bottom:{v}'
 if p=='mt':return 'margin-top:'+v
 if p=='grid-cols':return 'grid-template-columns:'+v
 if p=='grid-rows':return 'grid-template-rows:'+v
 if p=='text':return ('color:' if v.startswith(('#','rgb','var')) else 'font-size:')+v
 if p=='size':return f'width:{v};height:{v}'
 if p=='backdrop-blur':v='blur('+v+')'
 if p=='drop-shadow':v='drop-shadow('+v+')'
 if p=='shadow':return 'box-shadow:'+v
 return props[p]+':'+v
css='\n'.join('[class~='+json.dumps(c)+']{'+rule(c)+'}' for c in sorted(classes))
(root/'dist/layout.css').write_text(css)
page='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Revolua — Gestão educacional</title><meta name="description" content="Gestão educacional com presença na operação. Conheça a Revolua e marque uma conversa."><link rel="icon" href="assets/logo.png"><link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="layout.css"><link rel="stylesheet" href="site.css"></head><body><a class="skip" href="#desafios">Ir para o conteúdo</a><div id="page-height"><main class="canvas desktop">DESKTOP</main><main class="canvas mobile">MOBILE</main></div><header class="fixed-menu" aria-label="Navegação principal"><div class="menu-canvas desktop">DESKTOPNAV</div><div class="menu-canvas mobile">MOBILENAV</div></header><nav class="mobile-drawer" aria-label="Menu móvel" hidden><a href="#atuacao">Atuação</a><a href="#resultados">Resultados</a><a href="#quem-somos">Quem somos</a><a href="#contato">Vamos conversar ↗</a></nav><script src="site.js"></script></body></html>'''
page=page.replace('DESKTOPNAV',desktopnav).replace('MOBILENAV',mobilenav).replace('DESKTOP',desktop).replace('MOBILE',mobile)
(root/'dist/index.html').write_text(page)
print('Built index.html and local layout.css; classes:',len(classes))
