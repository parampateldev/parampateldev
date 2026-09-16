document.getElementById('year').textContent = new Date().getFullYear();

const root = document.documentElement;
const metas = [...document.querySelectorAll('.meta')];
let mouseX = innerWidth * .7, mouseY = innerHeight * .32;
let lastMouseX = mouseX, lastMouseY = mouseY;
const fluidPoints = metas.map((_, i) => ({ x: mouseX - i * 18, y: mouseY, vx: 0, vy: 0 }));
addEventListener('pointermove', (e) => { mouseX = e.clientX; mouseY = e.clientY; });
function moveFluid(t){
  const scaleX = 1000 / innerWidth, scaleY = 1000 / innerHeight;
  const speed = Math.hypot(mouseX-lastMouseX, mouseY-lastMouseY);
  fluidPoints.forEach((p,i) => {
    const leader = i === 0 ? {x:mouseX,y:mouseY} : fluidPoints[i-1];
    const spring = i === 0 ? .065 : .105;
    p.vx += (leader.x-p.x)*spring;
    p.vy += (leader.y-p.y)*spring;
    p.vx *= i === 0 ? .77 : .72;
    p.vy *= i === 0 ? .77 : .72;
    p.x += p.vx; p.y += p.vy;
    const wave = Math.sin(t*.002+i*1.15)*(8+i*1.6);
    const x = p.x*scaleX + Math.cos(t*.0014+i)*wave;
    const y = p.y*scaleY + Math.sin(t*.0017+i)*wave;
    const stretch = Math.min(1.65,1+speed*.006*(1-i/metas.length));
    metas[i].setAttribute('transform',`translate(${x} ${y}) rotate(${Math.atan2(p.vy,p.vx)*57.3}) scale(${stretch} ${2-stretch*.55})`);
  });
  lastMouseX += (mouseX-lastMouseX)*.18; lastMouseY += (mouseY-lastMouseY)*.18;
  requestAnimationFrame(moveFluid);
}
requestAnimationFrame(moveFluid);

const canvas = document.getElementById('field');
const ctx = canvas.getContext('2d');
let w, h, dpr;
const blobs=[{x:.74,y:.25,r:.38,c:'89,123,255',a:.19},{x:.27,y:.63,r:.3,c:'201,255,74',a:.1},{x:.84,y:.78,r:.25,c:'255,112,72',a:.1}];
function resize(){dpr=Math.min(devicePixelRatio,2);w=innerWidth;h=innerHeight;canvas.width=w*dpr;canvas.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
function draw(t){ctx.clearRect(0,0,w,h);blobs.forEach((b,i)=>{const x=(b.x+Math.sin(t*.00025+i)*.1+(cursorX/w-.5)*.07)*w;const y=(b.y+Math.cos(t*.0002+i)*.09+(cursorY/h-.5)*.05)*h;const r=b.r*Math.max(w,h);const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${b.c},${b.a})`);g.addColorStop(.5,`rgba(${b.c},${b.a*.4})`);g.addColorStop(1,`rgba(${b.c},0)`);ctx.fillStyle=g;ctx.fillRect(0,0,w,h)});requestAnimationFrame(draw)}
addEventListener('resize',resize);resize();requestAnimationFrame(draw);

const heroTitle=document.querySelector('h1');
const story=document.querySelector('.motion-story');
const sculpture=document.querySelector('.glass-sculpture');
const build=document.querySelector('.word-build');
const teach=document.querySelector('.word-teach');
const ship=document.querySelector('.word-ship');
const portrait=document.querySelector('.portrait img');
function clamp(v,a=0,b=1){return Math.max(a,Math.min(b,v))}
function onScroll(){
  const y=scrollY;
  const heroP=clamp(y/innerHeight);
  heroTitle.style.transform=`translate3d(0,${heroP*70}px,0) scale(${1-heroP*.06})`;
  heroTitle.style.opacity=1-heroP*.72;
  const rect=story.getBoundingClientRect();
  const p=clamp(-rect.top/(story.offsetHeight-innerHeight));
  sculpture.style.transform=`translate3d(${(p-.5)*150}px,${Math.sin(p*Math.PI)*-35}px,0) rotate(${p*130-35}deg) scale(${.74+p*.35})`;
  sculpture.style.borderRadius=`${43+p*14}% ${57-p*14}% ${37+p*18}% ${63-p*18}% / ${48-p*9}% ${36+p*16}% ${64-p*16}% ${52+p*9}%`;
  build.style.transform=`translate3d(${p*48}vw,${p*8}vh,0)`;
  teach.style.transform=`translate3d(${-p*55}vw,${(p-.5)*8}vh,0)`;
  ship.style.transform=`translate3d(${p*36}vw,${-p*12}vh,0)`;
  const pr=document.querySelector('.portrait').getBoundingClientRect();
  const pp=clamp((innerHeight-pr.top)/(innerHeight+pr.height));
  root.style.setProperty('--portrait-y',`${-14+pp*13}%`);
}
addEventListener('scroll',onScroll,{passive:true});onScroll();
