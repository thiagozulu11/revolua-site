(()=>{'use strict';
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const isMobile=()=>innerWidth<768,canvas=()=>$(isMobile()?'.canvas.mobile':'.canvas.desktop');
const menu=$('.fixed-menu'),drawer=$('.mobile-drawer');
const sections={'desafios':['12:6','12:71'],'atuacao':['3:30','3:134'],'resultados':['3:55','3:159'],'metodo':['3:75','3:179'],'diferenciais':['12:36','12:101'],'quem-somos':['3:94','3:198'],'perguntas':['12:51','12:116'],'contato':['3:100','3:204']};
function target(name){return $('[data-node-id="'+sections[name][isMobile()?1:0]+'"]',canvas())}
function scrollToSection(name){const n=target(name);if(!n)return;const top=n.getBoundingClientRect().top+scrollY-menu.getBoundingClientRect().height;window.scrollTo({top,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});drawer.hidden=true;history.replaceState(null,'','#'+name)}
const links={'Atuação':'atuacao','Resultados':'resultados','Quem somos':'quem-somos','Perguntas frequentes':'perguntas','Vamos conversar ↗':'contato'};
$$('button').forEach(b=>{const label=b.textContent.replace(/\s+/g,' ').trim();if(links[label]){b.classList.add('nav-link');b.addEventListener('click',()=>scrollToSection(links[label]));}else if(label.startsWith('Menu')){b.classList.add('mobile-menu-trigger');b.setAttribute('aria-expanded','false');b.addEventListener('click',()=>{drawer.hidden=!drawer.hidden;b.setAttribute('aria-expanded',String(!drawer.hidden));});}});
$$('.menu-canvas.mobile [data-node-id="3:114"]').forEach(n=>{n.tabIndex=0;n.setAttribute('role','button');n.setAttribute('aria-label','Abrir menu');n.addEventListener('click',()=>drawer.hidden=!drawer.hidden);n.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();drawer.hidden=!drawer.hidden}})});
$$('.mobile-drawer a,.skip').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();scrollToSection(a.hash.slice(1))}));
$$('a[href*="wa.me"]').filter(a=>a.className.includes('rounded-')).forEach(a=>a.classList.add('btn'));
$$('[data-name]').forEach(n=>{const name=n.dataset.name;if(name.startsWith('FAQ / ')&&!name.includes('Identificação')||['A conta não fecha.','As áreas não se conectam.','A urgência virou rotina.','na folha docente','nas horas docentes pagas','Resultados / Centro universitário no Centro-Oeste'].includes(name)){n.classList.add('hover-card');const c=getComputedStyle(n).backgroundColor.match(/\d+/g);if(c&&Number(c[0])+Number(c[1])+Number(c[2])<400)n.classList.add('dark');}});
$$('p').forEach(p=>p.classList.add('no-widow'));
$$('img').forEach(img=>{if((/logo(?:-desktop)?\.png/.test(img.src)))img.alt='Revolua — Pense. Reorganize. Execute.';else if(img.src.includes('office.jpg'))img.alt='Elisa Faria, fundadora da Revolua, em seu ambiente de trabalho';else if(img.src.includes('portrait.jpg'))img.alt='Retrato de Elisa Faria, fundadora da Revolua';});
function menuState(){const el=target('desafios');menu.classList.toggle('shown',el.getBoundingClientRect().top<innerHeight);if(!menu.classList.contains('shown'))drawer.hidden=true;}
function resize(){const width=isMobile()?390:1440,viewport=document.documentElement.clientWidth;document.documentElement.style.setProperty('--scale',viewport/width);$('#page-height').style.height=canvas().scrollHeight*(viewport/width)+'px';menuState();}
let queued=false;addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(()=>{menuState();queued=false})}},{passive:true});addEventListener('resize',resize);addEventListener('keydown',e=>{if(e.key==='Escape')drawer.hidden=true});new ResizeObserver(resize).observe(canvas());document.fonts.ready.then(resize);$$('img').forEach(i=>i.addEventListener('load',resize));resize();
})();
