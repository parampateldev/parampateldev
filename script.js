document.getElementById('year').textContent = new Date().getFullYear();

const root = document.documentElement;
const heroPortrait = document.querySelector('.hero-portrait');
let targetX = 0, targetY = 0, tiltX = 0, tiltY = 0;
addEventListener('pointermove', (e) => {
  targetX = (e.clientX / innerWidth - .5);
  targetY = (e.clientY / innerHeight - .5);
});
function trackPortrait(){
  tiltX += (targetX * 5 - tiltX) * .045;
  tiltY += (targetY * -4 - tiltY) * .045;
  if(heroPortrait){
    heroPortrait.style.setProperty('--tilt-x', tiltX + 'deg');
    heroPortrait.style.setProperty('--tilt-y', tiltY + 'deg');
    heroPortrait.style.setProperty('--look-x', tiltX * .45 + 'px');
    heroPortrait.style.setProperty('--look-y', -tiltY * .35 + 'px');
  }
  requestAnimationFrame(trackPortrait);
}
requestAnimationFrame(trackPortrait);
let mouseX=innerWidth*.5, mouseY=innerHeight*.5;
addEventListener('pointermove',e=>{mouseX=e.clientX;mouseY=e.clientY});

const canvas = document.getElementById('field');
const ctx = canvas.getContext('2d');
let w, h, dpr;
const blobs=[{x:.74,y:.25,r:.38,c:'89,123,255',a:.19},{x:.27,y:.63,r:.3,c:'201,255,74',a:.1},{x:.84,y:.78,r:.25,c:'255,112,72',a:.1}];
function resize(){dpr=Math.min(devicePixelRatio,2);w=innerWidth;h=innerHeight;canvas.width=w*dpr;canvas.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
function draw(t){ctx.clearRect(0,0,w,h);blobs.forEach((b,i)=>{const x=(b.x+Math.sin(t*.00025+i)*.1+(mouseX/w-.5)*.07)*w;const y=(b.y+Math.cos(t*.0002+i)*.09+(mouseY/h-.5)*.05)*h;const r=b.r*Math.max(w,h);const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${b.c},${b.a})`);g.addColorStop(.5,`rgba(${b.c},${b.a*.4})`);g.addColorStop(1,`rgba(${b.c},0)`);ctx.fillStyle=g;ctx.fillRect(0,0,w,h)});requestAnimationFrame(draw)}
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

// Fluid simulation used by the reference portfolio.
if (window.WebGLFluidEnhanced && document.getElementById('fluid')) {
  const fluid = new window.WebGLFluidEnhanced.default(document.getElementById('fluid'));
  fluid.setConfig({
    simResolution: 128, dyeResolution: 1440, captureResolution: 1512,
    densityDissipation: 0.5, velocityDissipation: 3, pressure: 0.1,
    pressureIterations: 20, curl: 3, splatRadius: 0.2, splatForce: 6000,
    shading: true, colorful: true, colorUpdateSpeed: 10, hover: true,
    backgroundColor: '#080a0e', transparent: true, brightness: 0.16,
    bloom: false, sunrays: false, colorPalette: ['#6478ff','#a9d95a','#806be6']
  });
  fluid.start();
  window.paramFluid = fluid;
}
