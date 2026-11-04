from pathlib import Path
import re, subprocess
root=Path(__file__).parent
assets=root/'dist/assets'
for prefix,ref in [('d','figma-reference.tsx'),('m','figma-mobile-reference.tsx')]:
    source=(root/ref).read_text()
    for name,url in re.findall(r'const (\w+) = "(https:[^"]+)";',source):
        if 'FotoNaOperacao' in name and (assets/'office.jpg').is_file():
            continue
        if 'RetratoInstitucional' in name and (assets/'portrait.jpg').is_file():
            continue
        filename=('office.jpg' if 'FotoNaOperacao' in name else 'portrait.jpg' if 'RetratoInstitucional' in name else ('logo-desktop.png' if prefix=='d' else 'logo.png') if 'Logotipo' in name else prefix+'-'+name+'.svg')
        subprocess.run(['curl','-f','-sS','-L','--max-time','30',url,'-o',str(assets/filename)],check=True)
css=subprocess.check_output(['curl','-f','-sS','-L','https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800&display=swap']).decode()
for i,url in enumerate(dict.fromkeys(re.findall(r'url\(([^)]+)\)',css))):
    ext='woff2' if 'woff2' in url else 'ttf'
    name=f'montserrat-{i}.{ext}'
    subprocess.run(['curl','-f','-sS','-L',url,'-o',str(assets/name)],check=True)
    css=css.replace(url,'assets/'+name)
(root/'dist/fonts.css').write_text(css)
print('Assets and Montserrat downloaded.')
