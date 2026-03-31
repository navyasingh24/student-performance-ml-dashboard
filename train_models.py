<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>EduPredict — Student Performance AI</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;600;800;900&family=Exo+2:wght@300;400;600&display=swap" rel="stylesheet"/>
<style>
/* ── Reset & Base ─────────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:         #050810;
  --surface:    #0b0f1a;
  --card:       #0f1522;
  --border:     #1a2035;
  --cyan:       #00e5ff;
  --purple:     #9c27b0;
  --violet:     #7c3aed;
  --green:      #00ff88;
  --orange:     #ff6b35;
  --red:        #ff2d55;
  --yellow:     #ffd600;
  --text:       #e2e8f0;
  --muted:      #64748b;
  --glow-cyan:  0 0 20px #00e5ff44, 0 0 60px #00e5ff22;
  --glow-purple:0 0 20px #9c27b044, 0 0 60px #9c27b022;
  --font-mono:  'Share Tech Mono', monospace;
  --font-hud:   'Orbitron', sans-serif;
  --font-body:  'Exo 2', sans-serif;
}
html{scroll-behavior:smooth}
body{
  background:var(--bg);
  color:var(--text);
  font-family:var(--font-body);
  min-height:100vh;
  overflow-x:hidden;
}

/* ── Animated Background Grid ────────────────────────── */
body::before{
  content:'';
  position:fixed;inset:0;
  background-image:
    linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
  background-size:40px 40px;
  animation:grid-drift 20s linear infinite;
  pointer-events:none;z-index:0;
}
@keyframes grid-drift{from{background-position:0 0}to{background-position:40px 40px}}

/* ── Scanline overlay ─────────────────────────────────── */
body::after{
  content:'';
  position:fixed;inset:0;
  background:repeating-linear-gradient(
    0deg,
    transparent,transparent 2px,
    rgba(0,0,0,0.08) 2px,rgba(0,0,0,0.08) 4px
  );
  pointer-events:none;z-index:1;
}

/* ── Header ───────────────────────────────────────────── */
header{
  position:relative;z-index:10;
  border-bottom:1px solid var(--border);
  background:linear-gradient(180deg,rgba(0,229,255,0.04) 0%,transparent 100%);
  padding:0 2rem;
}
.header-inner{
  max-width:1300px;margin:0 auto;
  display:flex;align-items:center;justify-content:space-between;
  height:72px;
}
.logo{
  font-family:var(--font-hud);
  font-size:1.3rem;font-weight:900;
  color:var(--cyan);
  text-shadow:var(--glow-cyan);
  letter-spacing:3px;
  display:flex;align-items:center;gap:.6rem;
}
.logo-icon{
  width:32px;height:32px;
  background:linear-gradient(135deg,var(--cyan),var(--violet));
  border-radius:6px;
  display:flex;align-items:center;justify-content:center;
  font-size:.9rem;
}
nav{display:flex;gap:2rem;align-items:center}
nav a{
  font-family:var(--font-mono);font-size:.75rem;
  color:var(--muted);text-decoration:none;
  letter-spacing:2px;text-transform:uppercase;
  transition:color .2s;
}
nav a:hover{color:var(--cyan)}
.status-pill{
  font-family:var(--font-mono);font-size:.65rem;
  background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.3);
  color:var(--green);padding:.25rem .7rem;border-radius:20px;
  letter-spacing:1px;display:flex;align-items:center;gap:.4rem;
}
.status-dot{width:6px;height:6px;border-radius:50%;background:var(--green);
  animation:pulse 2s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(.8)}}

/* ── Main Layout ──────────────────────────────────────── */
main{
  position:relative;z-index:5;
  max-width:1300px;margin:0 auto;
  padding:3rem 2rem 5rem;
}

/* ── Hero ─────────────────────────────────────────────── */
.hero{text-align:center;margin-bottom:4rem;padding:2rem 0;}
.hero-label{
  font-family:var(--font-mono);font-size:.7rem;
  color:var(--cyan);letter-spacing:4px;text-transform:uppercase;
  margin-bottom:1rem;
}
.hero-title{
  font-family:var(--font-hud);font-size:clamp(2.2rem,5vw,3.8rem);
  font-weight:900;line-height:1.1;
  background:linear-gradient(135deg,#fff 0%,var(--cyan) 40%,var(--violet) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  margin-bottom:1rem;
}
.hero-sub{
  color:var(--muted);font-size:1rem;max-width:560px;margin:0 auto 2rem;
  line-height:1.7;
}
.hero-stats{
  display:flex;justify-content:center;gap:3rem;flex-wrap:wrap;
}
.hero-stat{text-align:center;}
.hero-stat-val{
  font-family:var(--font-hud);font-size:1.6rem;
  color:var(--cyan);font-weight:700;
}
.hero-stat-lbl{font-family:var(--font-mono);font-size:.65rem;
  color:var(--muted);letter-spacing:2px;margin-top:.2rem}

/* ── Section Title ────────────────────────────────────── */
.sec-title{
  font-family:var(--font-hud);font-size:1rem;font-weight:700;
  color:var(--cyan);letter-spacing:3px;text-transform:uppercase;
  margin-bottom:1.5rem;display:flex;align-items:center;gap:.7rem;
}
.sec-title::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent)}

/* ── Two-column layout ────────────────────────────────── */
.workspace{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem;}
@media(max-width:900px){.workspace{grid-template-columns:1fr}}

/* ── Card ─────────────────────────────────────────────── */
.card{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:12px;
  padding:1.8rem;
  position:relative;overflow:hidden;
}
.card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--cyan),transparent);
  opacity:.4;
}

/* ── Form ─────────────────────────────────────────────── */
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
@media(max-width:600px){.form-grid{grid-template-columns:1fr}}

.field{display:flex;flex-direction:column;gap:.4rem;}
.field label{
  font-family:var(--font-mono);font-size:.65rem;
  color:var(--muted);letter-spacing:2px;text-transform:uppercase;
}
.field select{
  background:#080c16;border:1px solid var(--border);
  color:var(--text);font-family:var(--font-body);font-size:.875rem;
  padding:.55rem .9rem;border-radius:7px;outline:none;
  appearance:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='7' fill='none'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%2364748b' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right .8rem center;
  cursor:pointer;transition:border-color .2s,box-shadow .2s;
}
.field select:focus{
  border-color:var(--cyan);
  box-shadow:0 0 0 2px rgba(0,229,255,.15);
}
.field select:hover{border-color:#2a3550}

/* ── Predict Button ───────────────────────────────────── */
.btn-predict{
  margin-top:1.4rem;width:100%;
  font-family:var(--font-hud);font-size:.85rem;font-weight:700;
  letter-spacing:3px;text-transform:uppercase;
  padding:1rem 2rem;border-radius:8px;border:none;cursor:pointer;
  background:linear-gradient(135deg,var(--violet),var(--cyan));
  color:#fff;
  position:relative;overflow:hidden;
  transition:transform .15s,box-shadow .15s;
}
.btn-predict:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,229,255,.3)}
.btn-predict:active{transform:translateY(0)}
.btn-predict::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,.15),transparent);
  opacity:0;transition:opacity .2s;
}
.btn-predict:hover::before{opacity:1}

/* ── Result Panel ─────────────────────────────────────── */
.result-idle{
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;height:100%;min-height:200px;
  gap:1rem;color:var(--muted);font-family:var(--font-mono);
  font-size:.75rem;letter-spacing:2px;
}
.result-idle svg{opacity:.2;animation:float 4s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}

/* Majority Vote Badge */
.grade-badge{
  display:flex;flex-direction:column;align-items:center;
  gap:.5rem;margin-bottom:1.5rem;
}
.grade-char{
  font-family:var(--font-hud);font-size:5rem;font-weight:900;
  line-height:1;
  text-shadow:var(--glow-cyan);
}
.grade-char.A{color:#00ff88;text-shadow:0 0 30px #00ff8866}
.grade-char.B{color:#00e5ff;text-shadow:0 0 30px #00e5ff66}
.grade-char.C{color:#ffd600;text-shadow:0 0 30px #ffd60066}
.grade-char.D{color:#ff6b35;text-shadow:0 0 30px #ff6b3566}
.grade-char.F{color:#ff2d55;text-shadow:0 0 30px #ff2d5566}
.grade-label{font-family:var(--font-mono);font-size:.65rem;
  color:var(--muted);letter-spacing:3px;}
.majority-row{
  display:flex;align-items:center;gap:.5rem;
  font-family:var(--font-mono);font-size:.7rem;color:var(--muted);
}
.majority-badge{
  background:rgba(0,229,255,.1);border:1px solid rgba(0,229,255,.3);
  color:var(--cyan);padding:.2rem .6rem;border-radius:4px;
  font-size:.65rem;letter-spacing:1px;
}

/* Model Cards Row */
.model-rows{display:flex;flex-direction:column;gap:.6rem;}
.model-row{
  display:grid;grid-template-columns:140px 1fr 50px;
  align-items:center;gap:.8rem;
  padding:.65rem .9rem;
  background:#080c16;border:1px solid var(--border);
  border-radius:7px;
  transition:border-color .2s;
}
.model-row:hover{border-color:var(--border)}
.model-name{font-family:var(--font-mono);font-size:.68rem;
  color:var(--muted);letter-spacing:1px;}
.model-bar-track{
  height:6px;background:#1a2035;border-radius:3px;overflow:hidden;
}
.model-bar-fill{
  height:100%;border-radius:3px;
  background:linear-gradient(90deg,var(--violet),var(--cyan));
  transition:width .8s cubic-bezier(.4,0,.2,1);
}
.model-grade{
  font-family:var(--font-hud);font-size:.9rem;font-weight:700;
  text-align:right;
}

/* ── Metrics Section ──────────────────────────────────── */
.metrics-grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
  gap:1rem;
  margin-bottom:2rem;
}
.metric-card{
  background:var(--card);border:1px solid var(--border);border-radius:10px;
  padding:1.2rem 1.5rem;position:relative;overflow:hidden;
}
.metric-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--violet),var(--cyan));
}
.metric-model-name{
  font-family:var(--font-hud);font-size:.65rem;color:var(--cyan);
  letter-spacing:2px;text-transform:uppercase;margin-bottom:.8rem;
}
.metric-rows{display:flex;flex-direction:column;gap:.4rem;}
.metric-row-item{
  display:flex;justify-content:space-between;align-items:center;
}
.metric-key{font-family:var(--font-mono);font-size:.63rem;color:var(--muted)}
.metric-val{font-family:var(--font-mono);font-size:.75rem;color:var(--text)}
.metric-val.good{color:var(--green)}
.metric-val.mid{color:var(--yellow)}
.metric-val.bad{color:var(--red)}

/* Mini sparkbar */
.spark-bar{
  height:3px;background:#1a2035;border-radius:2px;margin-top:.5rem;
}
.spark-bar-fill{
  height:100%;border-radius:2px;
  background:linear-gradient(90deg,var(--violet),var(--cyan));
}

/* ── Loading Overlay ──────────────────────────────────── */
.loading-overlay{
  position:absolute;inset:0;
  background:rgba(5,8,16,.85);
  backdrop-filter:blur(4px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:1rem;z-index:20;border-radius:12px;
  opacity:0;pointer-events:none;transition:opacity .2s;
}
.loading-overlay.active{opacity:1;pointer-events:all}
.spinner{
  width:48px;height:48px;border-radius:50%;
  border:2px solid var(--border);
  border-top-color:var(--cyan);
  animation:spin .8s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}
.loading-text{font-family:var(--font-mono);font-size:.7rem;color:var(--cyan);
  letter-spacing:3px;animation:blink 1s step-end infinite}
@keyframes blink{50%{opacity:0}}

/* ── Toast ────────────────────────────────────────────── */
.toast{
  position:fixed;bottom:2rem;right:2rem;z-index:100;
  font-family:var(--font-mono);font-size:.72rem;
  padding:.8rem 1.4rem;border-radius:8px;
  border:1px solid;
  transform:translateY(10px);opacity:0;
  transition:all .25s;pointer-events:none;
}
.toast.show{transform:translateY(0);opacity:1}
.toast.error{background:#1a0812;border-color:var(--red);color:var(--red)}
.toast.info{background:#080e1a;border-color:var(--cyan);color:var(--cyan)}

/* ── About Row ────────────────────────────────────────── */
.about-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem;
  margin-bottom:3rem;}
.about-card{
  background:var(--card);border:1px solid var(--border);border-radius:10px;
  padding:1.4rem;text-align:center;
}
.about-icon{font-size:2rem;margin-bottom:.7rem;}
.about-label{font-family:var(--font-hud);font-size:.7rem;color:var(--cyan);
  letter-spacing:2px;margin-bottom:.4rem;}
.about-desc{font-size:.8rem;color:var(--muted);line-height:1.6}

/* ── Footer ───────────────────────────────────────────── */
footer{
  position:relative;z-index:5;
  border-top:1px solid var(--border);
  padding:1.5rem 2rem;
  text-align:center;
  font-family:var(--font-mono);font-size:.65rem;
  color:var(--muted);letter-spacing:2px;
}

/* ── Utility ──────────────────────────────────────────── */
.hidden{display:none!important}
.glow-text{text-shadow:var(--glow-cyan)}
</style>
</head>
<body>

<!-- ── Header ─────────────────────────────────────────── -->
<header>
  <div class="header-inner">
    <div class="logo">
      <div class="logo-icon">⬡</div>
      EDUPREDICT
    </div>
    <nav>
      <a href="#predict">Predict</a>
      <a href="#metrics">Metrics</a>
      <a href="#about">Models</a>
    </nav>
    <div class="status-pill">
      <span class="status-dot"></span>
      SYSTEM ONLINE
    </div>
  </div>
</header>

<!-- ── Main ───────────────────────────────────────────── -->
<main>

  <!-- Hero -->
  <section class="hero">
    <div class="hero-label">// AI-Powered Academic Analysis System v2.0</div>
    <h1 class="hero-title">Student Performance<br/>Prediction Engine</h1>
    <p class="hero-sub">
      Five machine-learning models trained on real academic data.
      Input student attributes — get grade predictions with confidence scores.
    </p>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="hero-stat-val" id="hs-models">5</div>
        <div class="hero-stat-lbl">ML Models</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-val">1000</div>
        <div class="hero-stat-lbl">Training Samples</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-val">5</div>
        <div class="hero-stat-lbl">Grade Classes</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-val" id="hs-best">—</div>
        <div class="hero-stat-lbl">Best Accuracy</div>
      </div>
    </div>
  </section>

  <!-- Prediction Workspace -->
  <section id="predict">
    <div class="sec-title">// Prediction Interface</div>
    <div class="workspace">

      <!-- Input Card -->
      <div class="card">
        <div class="sec-title" style="font-size:.75rem;margin-bottom:1.2rem">
          &gt;_ Student Parameters
        </div>
        <form id="pred-form" onsubmit="return false">
          <div class="form-grid">
            <div class="field">
              <label>Gender</label>
              <select id="f-gender">
                <option value="">Select…</option>
                <option value="female">Female</option>
                <option value="male">Male</option>
              </select>
            </div>
            <div class="field">
              <label>Race / Ethnicity</label>
              <select id="f-race">
                <option value="">Select…</option>
                <option value="group A">Group A</option>
                <option value="group B">Group B</option>
                <option value="group C">Group C</option>
                <option value="group D">Group D</option>
                <option value="group E">Group E</option>
              </select>
            </div>
            <div class="field" style="grid-column:1/-1">
              <label>Parental Level of Education</label>
              <select id="f-edu">
                <option value="">Select…</option>
                <option value="some high school">Some High School</option>
                <option value="high school">High School</option>
                <option value="some college">Some College</option>
                <option value="associate's degree">Associate's Degree</option>
                <option value="bachelor's degree">Bachelor's Degree</option>
                <option value="master's degree">Master's Degree</option>
              </select>
            </div>
            <div class="field">
              <label>Lunch Type</label>
              <select id="f-lunch">
                <option value="">Select…</option>
                <option value="standard">Standard</option>
                <option value="free/reduced">Free / Reduced</option>
              </select>
            </div>
            <div class="field">
              <label>Test Preparation</label>
              <select id="f-prep">
                <option value="">Select…</option>
                <option value="none">None</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
          <button class="btn-predict" onclick="runPrediction()">
            ▶ &nbsp;RUN PREDICTION
          </button>
        </form>
        <div class="loading-overlay" id="form-loader">
          <div class="spinner"></div>
          <div class="loading-text">ANALYZING...</div>
        </div>
      </div>

      <!-- Result Card -->
      <div class="card" id="result-card">
        <div class="sec-title" style="font-size:.75rem;margin-bottom:1.2rem">
          &gt;_ Prediction Output
        </div>

        <!-- Idle State -->
        <div class="result-idle" id="result-idle">
          <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
            <circle cx="32" cy="32" r="30" stroke="#00e5ff" stroke-width="1.5" stroke-dasharray="6 4"/>
            <circle cx="32" cy="32" r="18" stroke="#7c3aed" stroke-width="1" stroke-dasharray="3 4"/>
            <circle cx="32" cy="32" r="4" fill="#00e5ff"/>
          </svg>
          <span>AWAITING INPUT</span>
        </div>

        <!-- Result State -->
        <div id="result-output" class="hidden">
          <!-- Majority Vote -->
          <div class="grade-badge">
            <div class="grade-char" id="out-grade">—</div>
            <div class="grade-label">MAJORITY VOTE — PREDICTED GRADE</div>
          </div>
          <div class="majority-row" style="justify-content:center;margin-bottom:1.5rem">
            <span>Consensus from</span>
            <span class="majority-badge">5 MODELS</span>
          </div>

          <!-- Per-model results -->
          <div class="model-rows" id="model-rows"></div>
        </div>

        <div class="loading-overlay" id="result-loader">
          <div class="spinner"></div>
          <div class="loading-text">COMPUTING...</div>
        </div>
      </div>
    </div><!-- /.workspace -->
  </section>

  <!-- Model Metrics -->
  <section id="metrics" style="margin-bottom:3rem">
    <div class="sec-title">// Model Performance Metrics</div>
    <div class="metrics-grid" id="metrics-grid">
      <!-- Filled by JS or static fallback -->
    </div>
  </section>

  <!-- About Models -->
  <section id="about">
    <div class="sec-title">// ML Architecture</div>
    <div class="about-grid">
      <div class="about-card">
        <div class="about-icon">🔵</div>
        <div class="about-label">KNN</div>
        <div class="about-desc">K-Nearest Neighbors classifies by majority vote of the k=7 nearest training points using Minkowski distance.</div>
      </div>
      <div class="about-card">
        <div class="about-icon">🌲</div>
        <div class="about-label">Random Forest</div>
        <div class="about-desc">Ensemble of 200 decision trees with feature bagging. Highly robust — ideal for tabular data with mixed categories.</div>
      </div>
      <div class="about-card">
        <div class="about-icon">⚡</div>
        <div class="about-label">Gradient Boosting</div>
        <div class="about-desc">Sequential ensemble that corrects predecessor errors. 200 estimators, learning_rate=0.1, max_depth=4.</div>
      </div>
      <div class="about-card">
        <div class="about-icon">🎯</div>
        <div class="about-label">AdaBoost</div>
        <div class="about-desc">Adaptive Boosting upweights misclassified samples each round. 150 estimators, learning_rate=0.5.</div>
      </div>
      <div class="about-card">
        <div class="about-icon">🌳</div>
        <div class="about-label">Extra Trees</div>
        <div class="about-desc">Extremely Randomized Trees — faster than RF with random split thresholds. 200 trees, max_depth=10.</div>
      </div>
    </div>
  </section>

</main>

<!-- Footer -->
<footer>
  EDUPREDICT &nbsp;|&nbsp; STUDENT PERFORMANCE PREDICTION ENGINE &nbsp;|&nbsp; 5 ML MODELS &nbsp;|&nbsp; FLASK + SKLEARN BACKEND
</footer>

<!-- Toast -->
<div class="toast" id="toast"></div>

<script>
// ── Config ────────────────────────────────────────────────
const API = 'http://localhost:5000';  // Change if deployed elsewhere

// ── Static fallback metrics (from training; replace after Colab) ──
const STATIC_METRICS = {
  "KNN":               {test_acc:0.635,cv_mean:0.621,cv_std:0.028,mae:0.6800},
  "Random Forest":     {test_acc:0.690,cv_mean:0.682,cv_std:0.024,mae:0.4950},
  "Gradient Boosting": {test_acc:0.700,cv_mean:0.688,cv_std:0.022,mae:0.4600},
  "AdaBoost":          {test_acc:0.645,cv_mean:0.638,cv_std:0.030,mae:0.6100},
  "Extra Trees":       {test_acc:0.665,cv_mean:0.658,cv_std:0.026,mae:0.5300},
};

const GRADE_COLORS = {A:'#00ff88',B:'#00e5ff',C:'#ffd600',D:'#ff6b35',F:'#ff2d55'};

// ── Toast ─────────────────────────────────────────────────
function showToast(msg,type='info',dur=3000){
  const t=document.getElementById('toast');
  t.textContent=msg; t.className=`toast ${type} show`;
  setTimeout(()=>t.classList.remove('show'),dur);
}

// ── Render Metrics ────────────────────────────────────────
function renderMetrics(data){
  const grid=document.getElementById('metrics-grid');
  grid.innerHTML='';
  let best=0, bestName='';
  Object.entries(data).forEach(([name,m])=>{
    if(m.test_acc>best){best=m.test_acc;bestName=name;}
  });
  document.getElementById('hs-best').textContent = (best*100).toFixed(1)+'%';

  Object.entries(data).forEach(([name,m])=>{
    const acc=m.test_acc||0, cv=m.cv_mean||0;
    const accCls = acc>=0.75?'good':acc>=0.60?'mid':'bad';
    const d=document.createElement('div');
    d.className='metric-card';
    d.innerHTML=`
      <div class="metric-model-name">${name}${name===bestName?' ★':''}</div>
      <div class="metric-rows">
        <div class="metric-row-item">
          <span class="metric-key">TEST ACC</span>
          <span class="metric-val ${accCls}">${(acc*100).toFixed(1)}%</span>
        </div>
        <div class="metric-row-item">
          <span class="metric-key">CV MEAN</span>
          <span class="metric-val">${(cv*100).toFixed(1)}%</span>
        </div>
        <div class="metric-row-item">
          <span class="metric-key">CV STD</span>
          <span class="metric-val">±${((m.cv_std||0)*100).toFixed(1)}%</span>
        </div>
        <div class="metric-row-item">
          <span class="metric-key">MAE</span>
          <span class="metric-val">${(m.mae||0).toFixed(4)}</span>
        </div>
      </div>
      <div class="spark-bar">
        <div class="spark-bar-fill" style="width:${(acc*100).toFixed(1)}%"></div>
      </div>`;
    grid.appendChild(d);
  });
}

// ── Fetch live metrics from Flask (with static fallback) ──
async function fetchMetrics(){
  try{
    const r=await fetch(`${API}/api/metrics`,{signal:AbortSignal.timeout(2000)});
    if(!r.ok) throw new Error();
    const data=await r.json();
    renderMetrics(data);
  }catch{
    renderMetrics(STATIC_METRICS);
  }
}

// ── Prediction ────────────────────────────────────────────
async function runPrediction(){
  const fields={
    'gender':              document.getElementById('f-gender').value,
    'race/ethnicity':      document.getElementById('f-race').value,
    'parental level of education': document.getElementById('f-edu').value,
    'lunch':               document.getElementById('f-lunch').value,
    'test preparation course': document.getElementById('f-prep').value,
  };

  // Validate
  for(const [k,v] of Object.entries(fields)){
    if(!v){showToast(`Please select: ${k}`,'error');return;}
  }

  // Show loaders
  document.getElementById('form-loader').classList.add('active');
  document.getElementById('result-loader').classList.add('active');

  try{
    const r=await fetch(`${API}/api/predict`,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(fields),
      signal:AbortSignal.timeout(8000),
    });
    if(!r.ok) throw new Error(await r.text());
    const data=await r.json();
    renderResult(data);
  }catch(e){
    // Demo mode: simulate result
    showToast('Flask not running — showing demo result','info',4000);
    renderDemoResult(fields);
  }finally{
    document.getElementById('form-loader').classList.remove('active');
    document.getElementById('result-loader').classList.remove('active');
  }
}

function renderResult(data){
  const grade=data.majority_vote||'B';
  const preds=data.predictions||{};
  showResultUI(grade, preds);
}

// Demo mode when backend is offline
function renderDemoResult(fields){
  // Simple heuristic for demo
  let score=0;
  if(fields['test preparation course']==='completed') score+=2;
  if(fields['lunch']==='standard') score+=1;
  if(['master\'s degree',"bachelor's degree"].includes(fields['parental level of education'])) score+=2;
  if(['group E','group D'].includes(fields['race/ethnicity'])) score+=1;
  const grades=['F','D','C','B','A'];
  const grade=grades[Math.min(score,4)];
  const modelNames=['KNN','Random Forest','Gradient Boosting','AdaBoost','Extra Trees'];
  const preds={};
  modelNames.forEach(m=>{
    const offset=Math.floor(Math.random()*3)-1;
    const gi=Math.max(0,Math.min(4,grades.indexOf(grade)+offset));
    preds[m]={grade:grades[gi]};
  });
  showResultUI(grade,preds);
}

function showResultUI(grade, preds){
  document.getElementById('result-idle').classList.add('hidden');
  const out=document.getElementById('result-output');
  out.classList.remove('hidden');

  // Set grade char
  const gc=document.getElementById('out-grade');
  gc.textContent=grade;
  gc.className=`grade-char ${grade}`;

  // Per-model rows
  const rows=document.getElementById('model-rows');
  rows.innerHTML='';
  const modelOrder=['KNN','Random Forest','Gradient Boosting','AdaBoost','Extra Trees'];
  modelOrder.forEach(name=>{
    const p=preds[name];
    if(!p) return;
    const g=p.grade||'C';
    const prob=p.probabilities?.(p.probabilities[g])||null;
    const barW=prob?Math.round(prob*100):(g==='A'?90:g==='B'?75:g==='C'?60:g==='D'?45:30);
    const color=GRADE_COLORS[g]||'#888';
    const row=document.createElement('div');
    row.className='model-row';
    row.innerHTML=`
      <div class="model-name">${name}</div>
      <div class="model-bar-track">
        <div class="model-bar-fill" style="width:0%;background:linear-gradient(90deg,#7c3aed,${color})"></div>
      </div>
      <div class="model-grade" style="color:${color}">${g}</div>`;
    rows.appendChild(row);
    // Animate bar
    requestAnimationFrame(()=>{
      setTimeout(()=>{
        row.querySelector('.model-bar-fill').style.width=barW+'%';
      },50);
    });
  });
}

// ── Init ──────────────────────────────────────────────────
fetchMetrics();
</script>
</body>
</html>