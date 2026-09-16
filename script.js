document.getElementById('year').textContent = new Date().getFullYear();

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

const canvas = document.getElementById('field');
const ctx = canvas.getContext('2d');
let w, h, mx = 0.68, my = 0.3, tx = mx, ty = my;
const blobs = [
  {x:.72,y:.28,r:.32,c:'89,123,255',a:.2,s:.00038},
  {x:.26,y:.62,r:.26,c:'201,255,74',a:.12,s:.00025},
  {x:.84,y:.78,r:.2,c:'255,112,72',a:.1,s:.0003}
];
function resize(){const d=Math.min(devicePixelRatio,2);w=innerWidth;h=innerHeight;canvas.width=w*d;canvas.height=h*d;canvas.style.width=w+'px';canvas.style.height=h+'px';ctx.setTransform(d,0,0,d,0,0)}
function draw(t){ctx.clearRect(0,0,w,h);mx+=(tx-mx)*.025;my+=(ty-my)*.025;blobs.forEach((b,i)=>{const x=(b.x+Math.sin(t*b.s+i)*.08+(mx-.5)*(i===0?.16:.05))*w;const y=(b.y+Math.cos(t*b.s*.8+i)*.07+(my-.5)*(i===0?.14:.04))*h;const r=b.r*Math.max(w,h);const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${b.c},${b.a})`);g.addColorStop(.52,`rgba(${b.c},${b.a*.45})`);g.addColorStop(1,`rgba(${b.c},0)`);ctx.fillStyle=g;ctx.fillRect(0,0,w,h)});requestAnimationFrame(draw)}
addEventListener('resize',resize);addEventListener('pointermove',e=>{tx=e.clientX/w;ty=e.clientY/h});resize();if(!matchMedia('(prefers-reduced-motion: reduce)').matches)requestAnimationFrame(draw);
