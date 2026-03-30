/* ================================================================
   script.js — Nepaliकला | Shared JS v2
   ================================================================ */

/* ── CART STATE ── */
const CART_KEY = 'nk_cart';
function getCart(){try{return JSON.parse(localStorage.getItem(CART_KEY))||[]}catch{return[]}}
function saveCart(cart){localStorage.setItem(CART_KEY,JSON.stringify(cart))}
function addToCart(item){
  const cart=getCart();
  const existing=cart.find(c=>c.id===item.id&&c.type===item.type);
  if(existing){existing.qty=(existing.qty||1)+1}else{cart.push({...item,qty:1})}
  saveCart(cart);
  updateCartBadge();
  showToast('Added to Cart','✔','<strong>'+item.title+'</strong> added successfully.');
}
function updateCartBadge(){
  const total=getCart().reduce((s,c)=>s+(c.qty||1),0);
  document.querySelectorAll('.cart-count').forEach(el=>{
    el.textContent=total;
    el.style.display=total>0?'flex':'none';
  });
}

/* ── TOAST ── */
function showToast(title,icon,sub){
  let t=document.getElementById('global-toast');
  if(!t){
    t=document.createElement('div');
    t.id='global-toast';
    t.className='toast';
    t.innerHTML='<div class="toast-icon" id="t-icon"></div><div><div class="toast-title" id="t-title"></div><div class="toast-sub" id="t-sub"></div></div>';
    document.body.appendChild(t);
  }
  document.getElementById('t-icon').textContent=icon||'✔';
  document.getElementById('t-title').textContent=title;
  document.getElementById('t-sub').innerHTML=sub||'';
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer=setTimeout(()=>t.classList.remove('show'),3200);
}

document.addEventListener('DOMContentLoaded',()=>{

  /* ── NAV SCROLL ── */
  const navbar=document.getElementById('navbar');
  if(navbar){
    const onScroll=()=>navbar.classList.toggle('scrolled',window.scrollY>50);
    window.addEventListener('scroll',onScroll,{passive:true});
    onScroll();
  }

  /* ── ACTIVE NAV ── */
  const page=window.location.pathname.split('/').pop()||'';
  document.querySelectorAll('.nav-links a').forEach(a=>{
    if(a.getAttribute('href')===page)a.classList.add('active');
  });

  /* ── CART BADGE ── */
  updateCartBadge();

  /* ── SCROLL REVEAL ── */
  const revEls=document.querySelectorAll('.reveal');
  if(revEls.length){
    const obs=new IntersectionObserver(entries=>{
      entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target)}});
    },{threshold:.08});
    revEls.forEach(el=>obs.observe(el));
  }

  /* ── SMOOTH SCROLL ── */
  document.querySelectorAll('a[href^="#"]').forEach(a=>{
    a.addEventListener('click',e=>{
      const t=document.querySelector(a.getAttribute('href'));
      if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'})}
    });
  });

  /* ── ADD TO CART BUTTONS ── */
  document.querySelectorAll('.btn-cart').forEach(btn=>{
    btn.addEventListener('click',function(e){
      e.preventDefault();
      const card=this.closest('[data-product-id]');
      if(card){
        const item={
          id:card.dataset.productId,
          title:card.dataset.title||'Artwork',
          price:card.dataset.price||'0',
          artist:card.dataset.artist||'',
          type:card.dataset.type||'original',
          img:card.dataset.img||''
        };
        addToCart(item);
        const orig=this.textContent;
        this.textContent='Added ✔';
        this.classList.add('added');
        setTimeout(()=>{this.textContent=orig;this.classList.remove('added')},2000);
      }
    });
  });

  /* ── FILTER BUTTONS ── */
  document.querySelectorAll('.filter-group').forEach(group=>{
    group.querySelectorAll('.filter-btn').forEach(btn=>{
      btn.addEventListener('click',function(){
        group.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
        this.classList.add('active');
        const filter=this.dataset.filter;
        if(!filter)return;
        const grid=document.querySelector('.filterable-grid');
        if(!grid)return;
        grid.querySelectorAll('[data-category]').forEach(item=>{
          const show=filter==='all'||item.dataset.category===filter;
          item.style.display=show?'':'none';
        });
      });
    });
  });

  /* ── CONTACT/FORM SUBMIT ── */
  document.querySelectorAll('.js-form').forEach(form=>{
    form.addEventListener('submit',function(e){
      e.preventDefault();
      const btn=this.querySelector('[type="submit"],.submit-btn');
      if(!btn)return;
      const orig=btn.textContent;
      btn.textContent='Sending…';
      btn.disabled=true;
      setTimeout(()=>{
        btn.textContent='Sent ✔';
        btn.style.background='var(--success)';
        btn.style.borderColor='var(--success)';
        setTimeout(()=>{
          btn.textContent=orig;btn.disabled=false;
          btn.style.background='';btn.style.borderColor='';
          this.reset();
        },2500);
      },1000);
    });
  });

  /* ── NEWSLETTER ── */
  document.querySelectorAll('.js-newsletter').forEach(form=>{
    form.addEventListener('submit',function(e){
      e.preventDefault();
      const btn=this.querySelector('button');
      const orig=btn.textContent;
      btn.textContent='Subscribed ✔';
      btn.style.background='var(--gold)';btn.style.color='var(--navy)';
      this.reset();
      setTimeout(()=>{btn.textContent=orig;btn.style.background='';btn.style.color=''},3000);
    });
  });

  /* ── TAB SYSTEM ── */
  document.querySelectorAll('.tab-nav').forEach(nav=>{
    nav.querySelectorAll('.tab-btn').forEach(btn=>{
      btn.addEventListener('click',function(){
        const container=this.closest('.tabs-container');
        if(!container)return;
        container.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
        container.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
        this.classList.add('active');
        const target=container.querySelector('#'+this.dataset.tab);
        if(target)target.classList.add('active');
      });
    });
  });

  /* ── QUANTITY CONTROLS ── */
  document.querySelectorAll('.qty-control').forEach(ctrl=>{
    const minus=ctrl.querySelector('.qty-minus');
    const plus=ctrl.querySelector('.qty-plus');
    const inp=ctrl.querySelector('.qty-input');
    if(!minus||!plus||!inp)return;
    minus.addEventListener('click',()=>{const v=parseInt(inp.value)||1;if(v>1)inp.value=v-1});
    plus.addEventListener('click', ()=>{inp.value=(parseInt(inp.value)||1)+1});
  });

  /* ── ADMIN: SIDEBAR TOGGLE ── */
  const sideToggle=document.getElementById('sidebar-toggle');
  const adminSidebar=document.getElementById('admin-sidebar');
  if(sideToggle&&adminSidebar){
    sideToggle.addEventListener('click',()=>{adminSidebar.classList.toggle('collapsed')});
  }

  /* ── ADMIN: CHARTS (simple canvas sparklines) ── */
  function drawSparkline(id,data,color){
    const canvas=document.getElementById(id);
    if(!canvas||!canvas.getContext)return;
    const ctx=canvas.getContext('2d');
    const W=canvas.width,H=canvas.height;
    const max=Math.max(...data),min=Math.min(...data);
    const range=max-min||1;
    ctx.clearRect(0,0,W,H);
    ctx.strokeStyle=color||'#c8a84b';
    ctx.lineWidth=2;
    ctx.beginPath();
    data.forEach((v,i)=>{
      const x=(i/(data.length-1))*W;
      const y=H-((v-min)/range)*(H-8)-4;
      i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
    });
    ctx.stroke();
    ctx.lineTo(W,H);ctx.lineTo(0,H);
    ctx.fillStyle=color?.replace(')',',0.12)')||'rgba(200,168,75,0.12)';
    ctx.closePath();ctx.fill();
  }
  if(document.getElementById('chart-revenue')){
    drawSparkline('chart-revenue',[42,55,48,72,68,85,90,78,95,110,105,122],'#c8a84b');
    drawSparkline('chart-orders',[8,12,9,15,14,18,20,17,22,25,23,28],'#c93030');
    drawSparkline('chart-artists',[30,35,40,45,50,58,65,70,80,90,100,120],'#5b8dd9');
  }

});

/* ── EXPOSE GLOBALS ── */
window.NK={addToCart,getCart,showToast,updateCartBadge};
