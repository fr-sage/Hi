// app.js
// External resources used (CDNs):
// - Chart.js (https://cdn.jsdelivr.net/npm/chart.js)
// - Google Fonts (Inter) loaded in index.html

// ========== Theme Toggle (prefers-color-scheme default, persists to localStorage) ==========
const THEME_KEY = 'portfolio-theme';
const body = document.body;
const btnTheme = document.getElementById('theme-toggle');

function applyTheme(theme){
  if(theme === 'light'){
    body.classList.remove('dark');
    body.classList.add('light');
  } else if(theme === 'dark'){
    body.classList.remove('light');
    body.classList.add('dark');
  }
}

function initTheme(){
  const stored = localStorage.getItem(THEME_KEY);
  if(stored){ applyTheme(stored); }
  else{
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(prefersDark ? 'dark' : 'light');
  }
}
initTheme();

if(btnTheme){
  btnTheme.addEventListener('click', ()=>{
    const isLight = body.classList.contains('light');
    const next = isLight ? 'dark' : 'light';
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
  });
}

// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(a=>{
  a.addEventListener('click', (e)=>{
    const href = a.getAttribute('href');
    if(href.length>1){
      e.preventDefault();
      document.querySelector(href).scrollIntoView({behavior:'smooth',block:'start'});
    }
  });
});

// ========== Projects data (derived from README.md content) ==========
const PROJECTS = {
  p1:{
    id:'p1',
    title:'이커머스 고객 세그먼트 분석 및 마케팅 전략 제안',
    goal:'매출 하락 원인 규명 및 RFM 기반 고객 맞춤 프로모션 제안',
    data:'거래 내역(주문,고객,상품) 원시 데이터 — SQL로 다차원 테이블 생성',
    method:'SQL로 ETL 후 Python(Pandas)으로 RFM 지표 산출 및 K-Means로 클러스터링, Tableau로 대시보드 제작',
    results:'잠재 이탈 고객 타겟 프로모션으로 예상 매출 8% 증가 시나리오 도출',
    recommendation:'고가치 잠재 이탈군에 대해 맞춤형 프로모션 적용 및 재참여 캠페인 실행',
    tech:['SQL','Python','Tableau']
  },
  p2:{
    id:'p2',
    title:'프로젝트 2 — [두 번째 프로젝트 제목]',
    goal:'[프로젝트 목표 요약]',
    data:'[사용한 데이터 설명]',
    method:'[사용한 방법/분석 도구]',
    results:'[수치화된 성과]',
    recommendation:'[제안 사항]',
    tech:['SQL','Excel']
  }
};

// Modal handling
const modal = document.getElementById('modal');
const modalBody = document.getElementById('modal-body');
const modalTitle = document.getElementById('modal-title');
const modalClose = document.getElementById('modal-close');

function openModal(id){
  const proj = PROJECTS[id];
  if(!proj) return;
  modalTitle.textContent = proj.title;
  modalBody.innerHTML = `
    <p><strong>Goal:</strong> ${proj.goal}</p>
    <p><strong>Data:</strong> ${proj.data}</p>
    <p><strong>Method:</strong> ${proj.method}</p>
    <p><strong>Results:</strong> ${proj.results}</p>
    <p><strong>Recommendation:</strong> ${proj.recommendation}</p>
    <p><strong>Tech:</strong> ${proj.tech.join(', ')}</p>
    <hr />
    <div class="accordion">
      <button class="acc-toggle">분석 과정 (클릭하여 확장)</button>
      <div class="acc-panel">
        <p>분석 과정, 인사이트, 추가 제안 등을 여기에 상세히 기술합니다. (예: RFM 계산법, 클러스터 설명, KPI 변화 등)</p>
      </div>
    </div>
  `;
  modal.setAttribute('aria-hidden','false');
}

function closeModal(){
  modal.setAttribute('aria-hidden','true');
}

document.querySelectorAll('.detail-btn').forEach(b=>{
  b.addEventListener('click', ()=> openModal(b.dataset.id));
});
modalClose.addEventListener('click', closeModal);
modal.addEventListener('click', (e)=>{ if(e.target.classList.contains('modal-backdrop')) closeModal(); });
document.addEventListener('keydown', (e)=>{ if(e.key==='Escape') closeModal(); });

// Accordion inside modal (event delegation)
document.addEventListener('click', (e)=>{
  if(e.target.classList.contains('acc-toggle')){
    const btn = e.target; const panel = btn.nextElementSibling;
    const open = panel.style.maxHeight;
    if(open){ panel.style.maxHeight = null; btn.setAttribute('aria-expanded','false'); }
    else{ panel.style.maxHeight = panel.scrollHeight + 'px'; btn.setAttribute('aria-expanded','true'); }
  }
});

// Filters
document.querySelectorAll('.filter-btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.filter;
    document.querySelectorAll('.project-card').forEach(card=>{
      if(f==='all') card.style.display = '';
      else{
        const techs = card.dataset.tech.split(' ');
        card.style.display = techs.includes(f) ? '' : 'none';
      }
    });
  });
});

// IntersectionObserver reveal for sections
const io = new IntersectionObserver((entries)=>{
  entries.forEach(ent=>{
    if(ent.isIntersecting){ ent.target.classList.add('visible'); io.unobserve(ent.target); }
  });
},{threshold:0.12});
document.querySelectorAll('.section, .project-card, .card, .hero-card').forEach(el=>{ el.classList.add('reveal'); io.observe(el); });

// Back to top button
const backTop = document.getElementById('backTop');
window.addEventListener('scroll', ()=>{
  if(window.scrollY > 400) backTop.style.display = 'block'; else backTop.style.display = 'none';
});
backTop.addEventListener('click', ()=> window.scrollTo({top:0,behavior:'smooth'}));

// Chart.js visualization (demo data based on README project: e-commerce revenue & churn)
function renderChart(){
  try{
    const ctx = document.getElementById('kpiChart');
    if(!ctx) return;
    if(typeof Chart === 'undefined'){
      // Chart.js failed to load (network/offline). Skip chart render to avoid runtime error.
      console.warn('Chart.js not available — skipping chart render.');
      return;
    }
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const revenue = [120,130,115,140,150,160,155,170,165,180,190,210]; // demo
    const churn = [4.5,4.2,4.8,4.0,3.9,3.7,3.8,3.5,3.6,3.4,3.2,3.0]; // %

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: months,
        datasets: [
          { type:'line', label:'Revenue (k)', data: revenue, borderColor:'rgba(124,92,255,0.95)', backgroundColor:'rgba(124,92,255,0.18)', yAxisID:'y'},
          { type:'bar', label:'Churn Rate (%)', data: churn, backgroundColor:'rgba(0,255,209,0.38)', yAxisID:'y1'}
        ]
      },
      options: {
        plugins:{tooltip:{mode:'index',intersect:false}},
        responsive:true, maintainAspectRatio:false,
        scales:{
          y:{type:'linear',position:'left',title:{display:true,text:'Revenue (k)'}},
          y1:{type:'linear',position:'right',grid:{display:false},title:{display:true,text:'Churn (%)'},ticks:{callback: v=>v+"%"}}
        }
      }
    });
  }catch(err){
    console.error('Error rendering chart:', err);
  }
}
renderChart();

// Small accessibility: ensure modal gets focus when opened
const obs = new MutationObserver(muts=>{
  muts.forEach(m=>{
    if(m.attributeName==='aria-hidden' && modal.getAttribute('aria-hidden')==='false'){
      modal.querySelector('.modal-panel').focus();
    }
  });
});
obs.observe(modal,{attributes:true});
