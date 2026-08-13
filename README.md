# energy-calculator
Electrical energy calculation tools
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ENERGOTIZIM — Dispetcherlik Markazi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#05070a; --panel:#0b0f14; --panel2:#0e131a;
    --line-hi:#39ff88; --line-lo:#3aa8ff; --line-fault:#ff4d4d; --amber:#ffb020;
    --text:#c9d4dc; --dim:#5b6b78; --grid:#101820; --border:#1c2530;
    --forecast:#b98bff; --gen-col:#ffb020;
  }
  body.theme-light{
    --bg:#eef2f5; --panel:#ffffff; --panel2:#f3f6f8;
    --line-hi:#0a9d4c; --line-lo:#1470c4; --line-fault:#d33; --amber:#b5760a;
    --text:#1b2530; --dim:#7c8b98; --grid:#e2e8ee; --border:#d6dee5;
    --forecast:#7a3fd6; --gen-col:#b5760a;
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html,body{ background:var(--bg); color:var(--text); font-family:'JetBrains Mono', monospace; min-height:100%; }
  body{ background-image: radial-gradient(circle at 20% 10%, rgba(57,255,136,0.04), transparent 40%), radial-gradient(circle at 80% 80%, rgba(58,168,255,0.05), transparent 40%); padding:14px; }

  #alertBanner{ position:fixed; top:10px; left:50%; transform:translateX(-50%) translateY(-140%); background:#2a0e0e; border:1px solid var(--line-fault); color:#ffdada; padding:10px 16px; border-radius:6px; font-size:12px; z-index:100; display:flex; align-items:center; gap:12px; box-shadow:0 4px 24px rgba(0,0,0,.5); transition:transform .35s ease; }
  #alertBanner.show{ transform:translateX(-50%) translateY(0); }
  #alertBanner button{ background:none; border:1px solid var(--line-fault); color:#ffdada; border-radius:4px; padding:2px 8px; cursor:pointer; font-family:inherit; }

  .headbar{ display:flex; align-items:center; justify-content:space-between; padding:10px 18px; border:1px solid var(--border); background:linear-gradient(180deg,var(--panel2),var(--bg)); border-radius:6px; margin-bottom:12px; flex-wrap:wrap; gap:10px;}
  .brand{ display:flex; align-items:center; gap:12px; }
  .brand-mark{ width:34px; height:34px; border:2px solid var(--line-hi); border-radius:50%; display:flex; align-items:center; justify-content:center; color:var(--line-hi); font-family:'Chakra Petch',sans-serif; font-weight:700; font-size:15px; box-shadow:0 0 12px rgba(57,255,136,.5); flex-shrink:0; }
  .brand h1{ font-family:'Chakra Petch',sans-serif; font-weight:700; font-size:19px; letter-spacing:1.5px; }
  .brand small{ display:block; font-size:10px; letter-spacing:2px; color:var(--dim); font-family:'Chakra Petch',sans-serif; margin-top:2px; }
  .headright{ display:flex; align-items:center; gap:16px; }
  .clockwrap{ text-align:right; }
  #clock{ font-size:26px; font-weight:700; color:var(--line-hi); text-shadow:0 0 10px rgba(57,255,136,.6); letter-spacing:2px; }
  #datestr{ font-size:10.5px; color:var(--dim); letter-spacing:1px; text-transform:uppercase; }
  .iconbtn{ background:var(--panel2); border:1px solid var(--border); color:var(--text); border-radius:5px; padding:7px 10px; cursor:pointer; font-family:'Chakra Petch',sans-serif; font-size:11px; letter-spacing:.5px; }
  .iconbtn:hover{ border-color:var(--line-lo); }

  .board{ border:1px solid var(--border); background: linear-gradient(var(--grid) 1px, transparent 1px) 0 0/32px 32px, linear-gradient(90deg, var(--grid) 1px, transparent 1px) 0 0/32px 32px, var(--panel); border-radius:6px; padding:10px 6px; margin-bottom:12px; position:relative; overflow:hidden; }
  .board-label{ position:absolute; top:8px; left:16px; font-family:'Chakra Petch',sans-serif; font-size:10px; letter-spacing:2px; color:var(--dim); z-index:2; }
  .board-controls{ position:absolute; top:6px; right:10px; display:flex; gap:6px; z-index:2; }
  .board-controls button{ width:26px; height:26px; background:var(--panel2); border:1px solid var(--border); color:var(--text); border-radius:4px; cursor:pointer; font-size:14px; line-height:1; }
  .legend{ position:absolute; bottom:8px; left:16px; display:flex; gap:14px; z-index:2; font-size:9px; color:var(--dim); font-family:'Chakra Petch',sans-serif; letter-spacing:.5px; }
  .legend span{ display:inline-flex; align-items:center; gap:5px; }
  .legend i{ width:9px; height:9px; border-radius:50%; display:inline-block; }
  svg{ display:block; width:100%; height:400px; cursor:grab; }
  svg.dragging{ cursor:grabbing; }

  .node-box{ fill:var(--panel2); stroke:#2a3644; stroke-width:1; cursor:pointer; }
  .node-box.gen{ stroke:var(--gen-col); }
  .node-label{ fill:var(--text); font-family:'Chakra Petch',sans-serif; font-size:9.5px; font-weight:600; pointer-events:none;}
  .node-sub{ fill:var(--dim); font-size:7.5px; pointer-events:none;}
  .line-hi{ stroke:var(--line-hi); stroke-width:1.8; fill:none; filter:drop-shadow(0 0 3px rgba(57,255,136,.6)); cursor:pointer; }
  .line-lo{ stroke:var(--line-lo); stroke-width:1.5; fill:none; filter:drop-shadow(0 0 2px rgba(58,168,255,.5)); cursor:pointer; }
  .line-fault{ stroke:var(--line-fault); stroke-width:1.8; fill:none; filter:drop-shadow(0 0 4px rgba(255,77,77,.7)); cursor:pointer; }
  .line-gen{ stroke:var(--gen-col); stroke-width:1.3; fill:none; opacity:.75; }
  .line-hit{ stroke:transparent; stroke-width:12; fill:none; cursor:pointer; }
  .flow{ stroke-dasharray:2 6; animation:flow 1.1s linear infinite; }
  .flow-slow{ stroke-dasharray:1.5 5; animation:flow 1.8s linear infinite; }
  @keyframes flow{ to{ stroke-dashoffset:-40; } }
  .breaker-on{ fill:var(--line-hi); } .breaker-off{ fill:var(--line-fault); }
  .pulse{ animation:pulse 1.6s ease-in-out infinite; } @keyframes pulse{ 0%,100%{opacity:1;} 50%{opacity:.35;} }
  .territory{ fill:rgba(255,255,255,0.02); stroke:var(--border); stroke-width:1; stroke-dasharray:3 4; }
  .region-label{ fill:var(--dim); font-size:8px; opacity:.55; font-style:italic; pointer-events:none; }

  .kpi-row{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-bottom:12px; }
  @media (max-width:700px){ .kpi-row{ grid-template-columns:repeat(2,1fr);} }
  .kpi{ background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:10px 14px; }
  .kpi .lbl{ font-size:9px; letter-spacing:1.5px; color:var(--dim); text-transform:uppercase; font-family:'Chakra Petch',sans-serif;}
  .kpi .val{ font-size:22px; font-weight:700; margin-top:2px; font-family:'Chakra Petch',sans-serif; }
  .kpi .val span{ font-size:12px; color:var(--dim); font-weight:500; margin-left:4px;}
  .kpi.warn .val{ color:var(--amber); }
  .kpi svg{ height:26px; width:100%; margin-top:4px; }

  .grid-cols{ display:grid; grid-template-columns:repeat(4, 1fr); gap:10px; }
  @media (max-width:900px){ .grid-cols{ grid-template-columns:repeat(2,1fr); } }
  @media (max-width:560px){ .grid-cols{ grid-template-columns:1fr; } }
  .panel{ background:var(--panel); border:1px solid var(--border); border-radius:6px; overflow:hidden; display:flex; flex-direction:column; }
  .panel-head{ background:var(--panel2); padding:7px 10px; font-family:'Chakra Petch',sans-serif; font-size:11px; font-weight:600; letter-spacing:1px; color:#9fd9ff; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap; }
  .theme-light .panel-head{ color:#0a6fa8; }
  .panel-tools{ display:flex; gap:6px; align-items:center; }
  .searchbox{ background:var(--bg); border:1px solid var(--border); color:var(--text); font-family:inherit; font-size:10px; padding:3px 6px; border-radius:4px; width:110px; }
  .minibtn{ background:var(--bg); border:1px solid var(--border); color:var(--dim); font-size:9px; padding:3px 6px; border-radius:4px; cursor:pointer; font-family:'Chakra Petch',sans-serif; }
  .minibtn:hover{ color:var(--text); border-color:var(--line-lo); }
  .dot{ width:6px; height:6px; border-radius:50%; background:var(--line-hi); box-shadow:0 0 6px var(--line-hi); flex-shrink:0;}
  table{ width:100%; border-collapse:collapse; font-size:10.5px; }
  th{ text-align:left; padding:5px 8px; color:var(--dim); font-weight:500; font-size:9px; letter-spacing:.5px; text-transform:uppercase; border-bottom:1px solid var(--border); background:var(--panel2); position:sticky; top:0; }
  td{ padding:5px 8px; border-bottom:1px solid var(--border); white-space:nowrap; }
  tr:hover td{ background:var(--panel2); }
  .num{ font-variant-numeric:tabular-nums; text-align:right; }
  .status-ok{ color:var(--line-hi); } .status-warn{ color:var(--amber); } .status-fault{ color:var(--line-fault); font-weight:700; }
  .tablewrap{ max-height:230px; overflow:auto; }
  .spark{ width:46px; height:16px; vertical-align:middle; }

  .alarms{ max-height:230px; overflow-y:auto; }
  .alarm-row{ padding:6px 10px; font-size:10px; border-bottom:1px solid var(--border); cursor:pointer; }
  .alarm-row .top{ display:flex; gap:8px; }
  .alarm-row .t{ color:var(--dim); flex-shrink:0; }
  .alarm-row.sev-crit{ color:var(--line-fault); } .alarm-row.sev-warn{ color:var(--amber); } .alarm-row.sev-info{ color:var(--line-lo); }
  .alarm-comment{ margin-top:4px; display:none; gap:6px; }
  .alarm-comment.open{ display:flex; }
  .alarm-comment input{ flex:1; background:var(--bg); border:1px solid var(--border); color:var(--text); font-family:inherit; font-size:10px; padding:3px 6px; border-radius:4px; }
  .comment-tag{ color:var(--dim); font-style:italic; display:block; margin-top:3px; }

  .detail-overlay{ position:fixed; inset:0; background:rgba(0,0,0,.55); display:none; align-items:center; justify-content:center; z-index:200; }
  .detail-overlay.show{ display:flex; }
  .detail-card{ background:var(--panel); border:1px solid var(--border); border-radius:8px; width:min(480px,90vw); padding:16px; }
  .detail-card h2{ font-family:'Chakra Petch',sans-serif; font-size:15px; margin-bottom:4px; }
  .detail-card .sub{ color:var(--dim); font-size:10.5px; margin-bottom:12px; }
  .detail-card svg{ width:100%; height:100px; }
  .detail-close{ float:right; background:none; border:1px solid var(--border); color:var(--text); border-radius:4px; padding:3px 9px; cursor:pointer; }
  .detail-grid{ display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:12px; font-size:10.5px; }
  .detail-grid div span{ display:block; color:var(--dim); font-size:9px; text-transform:uppercase; letter-spacing:1px; }

  ::-webkit-scrollbar{ width:7px; height:7px; }
  ::-webkit-scrollbar-track{ background:var(--panel2); }
  ::-webkit-scrollbar-thumb{ background:#243040; border-radius:4px; }
  footer{ text-align:center; padding:10px; color:var(--dim); font-size:9.5px; letter-spacing:1px; }
</style>
</head>
<body>

<div id="alertBanner"><span id="alertText"></span><button id="alertClose">YOPISH</button></div>

<div class="headbar">
  <div class="brand">
    <div class="brand-mark">⚡</div>
    <div>
      <h1>ENERGOTIZIM NAZORAT MARKAZI</h1>
      <small>O'ZBEKISTON MILLIY ELEKTR TARMOG'I — REAL VAQT MONITORINGI</small>
    </div>
  </div>
  <div class="headright">
    <button class="iconbtn" id="themeToggle">☾ MAVZU</button>
    <div class="clockwrap">
      <div id="clock">00:00:00</div>
      <div id="datestr">—</div>
    </div>
  </div>
</div>

<div class="kpi-row">
  <div class="kpi">
    <div class="lbl">Umumiy Yuklama (prognoz bilan)</div>
    <div class="val" id="kpiLoad">— <span>MVt</span></div>
    <svg id="loadForecastSpark"></svg>
  </div>
  <div class="kpi">
    <div class="lbl">Tarmoq Chastotasi</div>
    <div class="val" id="kpiFreq">— <span>Hz</span></div>
  </div>
  <div class="kpi">
    <div class="lbl">Faol Liniyalar</div>
    <div class="val" id="kpiLines">— <span>/ 8</span></div>
  </div>
  <div class="kpi warn">
    <div class="lbl">Faol Signallar</div>
    <div class="val" id="kpiAlarms">— <span>ta</span></div>
  </div>
</div>

<div class="board">
  <div class="board-label">MNEMOSXEMA — O'ZBEKISTON GENERATSIYA VA UZATISH TARMOG'I</div>
  <div class="board-controls">
    <button id="zoomIn">+</button>
    <button id="zoomOut">−</button>
    <button id="zoomReset">⤾</button>
  </div>
  <svg viewBox="0 0 700 380" id="mimic"></svg>
  <div class="legend">
    <span><i style="background:var(--gen-col)"></i>Generatsiya manbai</span>
    <span><i style="background:var(--line-lo)"></i>Podstansiya / Yuklama markazi</span>
    <span><i style="background:var(--line-fault)"></i>Avariya</span>
  </div>
</div>

<div class="grid-cols">

  <div class="panel" style="grid-column: span 2;">
    <div class="panel-head">
      <span style="display:flex;align-items:center;gap:6px;"><span class="dot"></span>PODSTANSIYALAR / YUKLAMA MARKAZLARI</span>
      <div class="panel-tools">
        <input class="searchbox" id="subSearch" placeholder="qidirish...">
        <button class="minibtn" id="subSort">SARALASH</button>
        <button class="minibtn" id="subExport">CSV</button>
      </div>
    </div>
    <div class="tablewrap"><table>
      <thead><tr><th>Obyekt</th><th class="num">kV</th><th class="num">MVt</th><th>Tendensiya</th><th class="num">A</th><th>Holat</th></tr></thead>
      <tbody id="subTable"></tbody>
    </table></div>
  </div>

  <div class="panel" style="grid-column: span 2;">
    <div class="panel-head">
      <span style="display:flex;align-items:center;gap:6px;"><span class="dot"></span>UZATISH LINIYALARI (MAGISTRAL)</span>
      <div class="panel-tools">
        <input class="searchbox" id="lineSearch" placeholder="qidirish...">
        <button class="minibtn" id="lineSort">SARALASH</button>
        <button class="minibtn" id="lineExport">CSV</button>
      </div>
    </div>
    <div class="tablewrap"><table>
      <thead><tr><th>Liniya</th><th class="num">kV</th><th>Yuklama</th><th class="num">%</th><th>Holat</th></tr></thead>
      <tbody id="lineTable"></tbody>
    </table></div>
  </div>

  <div class="panel" style="grid-column: span 2;">
    <div class="panel-head">
      <span style="display:flex;align-items:center;gap:6px;"><span class="dot"></span>SIGNALIZATSIYA JURNALI</span>
      <div class="panel-tools">
        <button class="minibtn" id="alarmExport">CSV</button>
        <button class="minibtn" id="alarmClear">TOZALASH</button>
      </div>
    </div>
    <div class="alarms" id="alarmLog"></div>
  </div>

  <div class="panel" style="grid-column: span 2;">
    <div class="panel-head">
      <span style="display:flex;align-items:center;gap:6px;"><span class="dot"></span>GENERATSIYA MANBALARI</span>
      <div class="panel-tools">
        <input class="searchbox" id="genSearch" placeholder="qidirish...">
        <button class="minibtn" id="genExport">CSV</button>
      </div>
    </div>
    <div class="tablewrap"><table>
      <thead><tr><th>Stansiya</th><th class="num">MVt</th><th>Tendensiya</th><th class="num">%</th><th>Holat</th></tr></thead>
      <tbody id="genTable"></tbody>
    </table></div>
  </div>

</div>

<div class="panel" style="margin-top:10px;">
  <div class="panel-head">
    <span style="display:flex;align-items:center;gap:6px;"><span class="dot"></span>REAL JOYLASHUVLAR — GOOGLE XARITASI</span>
    <div class="panel-tools"><input class="searchbox" id="mapsSearch" placeholder="qidirish..." style="width:140px;"></div>
  </div>
  <div style="padding:4px 4px 10px;">
    <div style="font-size:9.5px;color:var(--dim);padding:8px 10px 4px;letter-spacing:1px;text-transform:uppercase;font-family:'Chakra Petch',sans-serif;">Generatsiya manbalari</div>
    <div id="mapsLinksGen" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(190px,1fr)); gap:6px; padding:0 10px;"></div>
    <div style="font-size:9.5px;color:var(--dim);padding:12px 10px 4px;letter-spacing:1px;text-transform:uppercase;font-family:'Chakra Petch',sans-serif;">Podstansiyalar / Yuklama markazlari</div>
    <div id="mapsLinksGrid" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(190px,1fr)); gap:6px; padding:0 10px 4px;"></div>
  </div>
</div>

<footer>ENERGOTIZIM SCADA/EMS — SIMULYATSIYA REJIMI · JOYLASHUV TAXMINIY KOORDINATALARGA ASOSLANGAN SXEMATIK KO'RSATKICH · Jurnal brauzeringizda saqlanadi</footer>

<div class="detail-overlay" id="detailOverlay">
  <div class="detail-card">
    <button class="detail-close" id="detailClose">✕</button>
    <h2 id="detailTitle">—</h2>
    <div class="sub" id="detailSub">—</div>
    <svg id="detailChart" viewBox="0 0 300 100" preserveAspectRatio="none"></svg>
    <div class="detail-grid" id="detailGrid"></div>
    <a id="detailMapLink" href="#" target="_blank" rel="noopener" class="minibtn" style="display:inline-block;margin-top:12px;text-decoration:none;">📍 GOOGLE XARITASIDA OCHISH</a>
  </div>
</div>

<script>
const svgns = "http://www.w3.org/2000/svg";

const themeBtn = document.getElementById('themeToggle');
themeBtn.addEventListener('click', ()=>{
  document.body.classList.toggle('theme-light');
  themeBtn.textContent = document.body.classList.contains('theme-light') ? '☀ MAVZU' : '☾ MAVZU';
});

function tick(){
  const now = new Date();
  document.getElementById('clock').textContent = now.toLocaleTimeString('uz-UZ', {hour12:false});
  const days=['Yakshanba','Dushanba','Seshanba','Chorshanba','Payshanba','Juma','Shanba'];
  const months=['yanvar','fevral','mart','aprel','may','iyun','iyul','avgust','sentabr','oktabr','noyabr','dekabr'];
  document.getElementById('datestr').textContent = `${days[now.getDay()]}, ${now.getDate()} ${months[now.getMonth()]} ${now.getFullYear()}`;
}
tick(); setInterval(tick,1000);

/* ---------- Real-geography node data (approx coordinates) ---------- */
// Grid / load-center substations
const gridNodes = [
  {id:'tsk', name:"Toshkent", lon:69.28, lat:41.30, kv:500, base:480, hist:[], mapsUrl:"https://maps.google.com/?cid=11937127517559049112"},
  {id:'jzk', name:"Jizzax", lon:67.83, lat:40.12, kv:220, base:90, hist:[], mapsUrl:"https://maps.google.com/?cid=10554401295052640482"},
  {id:'smk', name:"Samarqand", lon:66.96, lat:39.65, kv:220, base:200, hist:[], mapsUrl:"https://maps.google.com/?cid=5221421127129050967"},
  {id:'bxr', name:"Buxoro", lon:64.42, lat:39.77, kv:220, base:160, hist:[], mapsUrl:"https://maps.google.com/?cid=14446398563653576551"},
  {id:'qrs', name:"Qarshi", lon:65.79, lat:38.86, kv:220, base:140, hist:[], mapsUrl:"https://maps.google.com/?cid=7585022385417834653"},
  {id:'nuk', name:"Nukus", lon:59.61, lat:42.46, kv:220, base:110, hist:[], mapsUrl:"https://maps.google.com/?cid=9535464614235519286"},
  {id:'frg', name:"Farg'ona", lon:71.78, lat:40.39, kv:220, base:180, hist:[], mapsUrl:"https://maps.google.com/?cid=14962321866357636028"},
  {id:'and', name:"Andijon", lon:72.34, lat:40.78, kv:110, base:120, hist:[], mapsUrl:"https://maps.google.com/?cid=18178142911318974380"},
  {id:'nmn', name:"Namangan", lon:71.67, lat:40.99, kv:110, base:100, hist:[], mapsUrl:"https://maps.google.com/?cid=3958508297295831302"},
];
// Generation sources
const genNodes = [
  {id:'sdt', name:"Sirdaryo TES", lon:68.78, lat:40.49, cap:3000, hist:[], mapsUrl:"https://maps.google.com/?cid=17429590686570124231"},
  {id:'tsi', name:"Toshkent IES", lon:69.35, lat:41.20, cap:1870, hist:[], mapsUrl:"https://maps.google.com/?cid=6127197953028920599"},
  {id:'chg', name:"Charvak GES", lon:70.02, lat:41.62, cap:620, hist:[], mapsUrl:"https://maps.google.com/?cid=10173227217530929614"},
  {id:'fhg', name:"Farhod GES", lon:69.27, lat:40.22, cap:126, hist:[], mapsUrl:"https://maps.google.com/?cid=17424167629597049085"},
  {id:'agt', name:"Angren TES", lon:70.14, lat:41.02, cap:484, hist:[], mapsUrl:"https://maps.google.com/?cid=17603881763463471735"},
  {id:'nvt', name:"Navoiy TES", lon:65.38, lat:40.10, cap:1230, hist:[], mapsUrl:"https://maps.google.com/?cid=8858439347007437998"},
  {id:'zfw', name:"Zarafshon Shamol ES", lon:64.20, lat:41.57, cap:500, hist:[], mapsUrl:"https://maps.google.com/?cid=4241850867011603979"},
  {id:'kks', name:"Karakul Quyosh SES", lon:63.85, lat:39.15, cap:200, hist:[], mapsUrl:"https://maps.google.com/?cid=9251788477188992462"},
  {id:'mbt', name:"Mubarek TES", lon:65.15, lat:39.27, cap:960, hist:[], mapsUrl:"https://maps.google.com/?cid=8725562161346930039"},
  {id:'tmt', name:"Talimarjon TES", lon:65.49, lat:38.28, cap:1600, hist:[], mapsUrl:"https://maps.google.com/?cid=4846254994207317001"},
  {id:'tht', name:"Taxiatosh TES", lon:60.10, lat:41.80, cap:730, hist:[], mapsUrl:"https://maps.google.com/?cid=6504227686620483399"},
];
const allNodes = [...gridNodes, ...genNodes];
const nodeById = id => allNodes.find(n=>n.id===id);

// Faultable backbone transmission lines (grid-to-grid)
const lines = [
  {name:"Toshkent — Jizzax", kv:220, a:'tsk', b:'jzk', hist:[]},
  {name:"Jizzax — Samarqand", kv:220, a:'jzk', b:'smk', hist:[]},
  {name:"Samarqand — Buxoro", kv:220, a:'smk', b:'bxr', hist:[]},
  {name:"Buxoro — Qarshi", kv:220, a:'bxr', b:'qrs', hist:[]},
  {name:"Buxoro — Nukus", kv:220, a:'bxr', b:'nuk', hist:[]},
  {name:"Toshkent — Farg'ona", kv:220, a:'tsk', b:'frg', hist:[]},
  {name:"Farg'ona — Andijon", kv:110, a:'frg', b:'and', hist:[]},
  {name:"Farg'ona — Namangan", kv:110, a:'frg', b:'nmn', hist:[]},
];
// Generation feed connectors (always-on, non-faultable)
const genEdges = [
  ['tsk','sdt'], ['tsk','tsi'], ['tsk','chg'], ['tsk','fhg'], ['tsk','agt'],
  ['smk','nvt'], ['nvt','zfw'], ['bxr','kks'], ['qrs','mbt'], ['qrs','tmt'], ['nuk','tht'],
];

let faultLine = -1;
let alarms = [];
let loadHistory = [];
let subSortStress = false, lineSortStress = false;
let subFilter = '', lineFilter = '', genFilter='';

function rnd(min,max){ return Math.random()*(max-min)+min; }
function fmtTime(){ return new Date().toLocaleTimeString('uz-UZ',{hour12:false}); }
function pushHist(arr, v, max=24){ arr.push(v); if(arr.length>max) arr.shift(); }

async function loadAlarmsFromStorage(){
  try{
    const res = await window.storage.get('energotizim-alarms-uz-v3', false);
    if(res && res.value){ alarms = JSON.parse(res.value); }
  }catch(e){}
  renderAlarms();
}
async function saveAlarmsToStorage(){
  try{ await window.storage.set('energotizim-alarms-uz-v3', JSON.stringify(alarms.slice(0,60)), false); }catch(e){}
}

let alarmSeq = 0;
function pushAlarm(text, sev){
  const item = {id:'a'+(++alarmSeq)+'-'+Date.now(), t:fmtTime(), text, sev, comment:''};
  alarms.unshift(item);
  if(alarms.length>60) alarms.pop();
  renderAlarms();
  saveAlarmsToStorage();
  if(sev==='crit') showBanner(text);
}
function showBanner(text){
  document.getElementById('alertText').textContent = '⚠ '+text;
  const b = document.getElementById('alertBanner');
  b.classList.add('show');
  clearTimeout(showBanner._t);
  showBanner._t = setTimeout(()=> b.classList.remove('show'), 6000);
}
document.getElementById('alertClose').addEventListener('click', ()=> document.getElementById('alertBanner').classList.remove('show'));

function renderAlarms(){
  const el=document.getElementById('alarmLog');
  el.innerHTML = alarms.map(a=>`
    <div class="alarm-row sev-${a.sev}" data-id="${a.id}">
      <div class="top"><span class="t">${a.t}</span><span>${a.text}</span></div>
      ${a.comment ? `<span class="comment-tag">💬 ${escapeHtml(a.comment)}</span>` : ''}
      <div class="alarm-comment"><input type="text" placeholder="Operator izohi..." value="${escapeHtml(a.comment)}"></div>
    </div>`).join('') || '<div style="padding:12px;color:var(--dim);font-size:10.5px;">Signal yo\'q</div>';

  el.querySelectorAll('.alarm-row').forEach(row=>{
    row.addEventListener('click', (e)=>{
      if(e.target.tagName==='INPUT') return;
      row.querySelector('.alarm-comment').classList.toggle('open');
    });
    const input = row.querySelector('.alarm-comment input');
    input.addEventListener('click', e=>e.stopPropagation());
    input.addEventListener('change', ()=>{
      const a = alarms.find(x=>x.id===row.dataset.id);
      if(a){ a.comment = input.value; renderAlarms(); saveAlarmsToStorage(); }
    });
  });
}
function escapeHtml(s){ return (s||'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

document.getElementById('alarmClear').addEventListener('click', ()=>{ alarms = []; renderAlarms(); saveAlarmsToStorage(); });

function toCSV(rows){ return rows.map(r=>r.map(c=>`"${String(c).replace(/"/g,'""')}"`).join(',')).join('\n'); }
function downloadCSV(filename, rows){
  const blob = new Blob([toCSV(rows)], {type:'text/csv;charset=utf-8;'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href=url; a.download=filename; a.click(); URL.revokeObjectURL(url);
}
document.getElementById('subExport').addEventListener('click', ()=>{
  const rows=[['Obyekt','kV','MVt','A','Holat']];
  gridNodes.forEach(s=>{ const last=s.hist[s.hist.length-1]||s.base; rows.push([s.name,s.kv,last.toFixed(1),Math.round(last*1000/(s.kv*1.73)), last>s.base*1.12?'YUQORI YUKLAMA':'NORMA']); });
  downloadCSV('podstansiyalar.csv', rows);
});
document.getElementById('lineExport').addEventListener('click', ()=>{
  const rows=[['Liniya','kV','Yuklama %','Holat']];
  lines.forEach((l,i)=>{ const last=l.hist[l.hist.length-1]||0; rows.push([l.name,l.kv,last, i===faultLine?'AVARIYA':'ISHLAMOQDA']); });
  downloadCSV('liniyalar.csv', rows);
});
document.getElementById('genExport').addEventListener('click', ()=>{
  const rows=[['Stansiya','MVt','%','Holat']];
  genNodes.forEach(g=>{ const last=g.hist[g.hist.length-1]||0; rows.push([g.name,last.toFixed(0),Math.round(last/g.cap*100),'ISHDA']); });
  downloadCSV('generatsiya.csv', rows);
});
document.getElementById('alarmExport').addEventListener('click', ()=>{
  const rows=[['Vaqt','Daraja','Xabar','Izoh']];
  alarms.forEach(a=> rows.push([a.t,a.sev,a.text,a.comment||'']));
  downloadCSV('signalizatsiya-jurnali.csv', rows);
});

document.getElementById('subSearch').addEventListener('input', e=>{ subFilter=e.target.value.toLowerCase(); renderTables(); });
document.getElementById('lineSearch').addEventListener('input', e=>{ lineFilter=e.target.value.toLowerCase(); renderTables(); });
document.getElementById('genSearch').addEventListener('input', e=>{ genFilter=e.target.value.toLowerCase(); renderTables(); });
document.getElementById('subSort').addEventListener('click', ()=>{ subSortStress=!subSortStress; renderTables(); });
document.getElementById('lineSort').addEventListener('click', ()=>{ lineSortStress=!lineSortStress; renderTables(); });

function sparkPath(hist, w=46, h=16){
  if(hist.length<2) return '';
  const min=Math.min(...hist), max=Math.max(...hist);
  const range = (max-min)||1;
  return hist.map((v,i)=>{ const x=(i/(hist.length-1))*w; const y=h-((v-min)/range)*h; return `${i===0?'M':'L'}${x.toFixed(1)},${y.toFixed(1)}`; }).join(' ');
}
function sparkSVG(hist, colorVar='--line-hi'){
  return `<svg class="spark" viewBox="0 0 46 16"><path d="${sparkPath(hist)}" fill="none" stroke="var(${colorVar})" stroke-width="1.4"/></svg>`;
}

function renderTables(){
  let totalLoad=0;
  let subList = gridNodes.map(s=>{ totalLoad += (s.hist[s.hist.length-1]||s.base); return s; }).filter(s=> s.name.toLowerCase().includes(subFilter));
  if(subSortStress){ subList = subList.slice().sort((a,b)=>{ const la=a.hist[a.hist.length-1]||a.base, lb=b.hist[b.hist.length-1]||b.base; return (lb-b.base)-(la-a.base); }); }
  document.getElementById('subTable').innerHTML = subList.map(s=>{
    const load = s.hist[s.hist.length-1]||s.base;
    const amps = Math.round(load*1000/(s.kv*1.73));
    const stressed = load > s.base*1.12;
    const status = stressed ? '<span class="status-warn">YUQORI YUKLAMA</span>' : '<span class="status-ok">NORMA</span>';
    return `<tr><td>${s.name}</td><td class="num">${s.kv}</td><td class="num">${load.toFixed(1)}</td><td>${sparkSVG(s.hist, stressed?'--amber':'--line-hi')}</td><td class="num">${amps}</td><td>${status}</td></tr>`;
  }).join('') || '<tr><td colspan="6" style="color:var(--dim);text-align:center;">Topilmadi</td></tr>';

  let lineList = lines.map((l,i)=>({...l, idx:i})).filter(l=> l.name.toLowerCase().includes(lineFilter));
  if(lineSortStress){ lineList = lineList.slice().sort((a,b)=> (b.idx===faultLine?1000:(b.hist[b.hist.length-1]||0)) - (a.idx===faultLine?1000:(a.hist[a.hist.length-1]||0))); }
  document.getElementById('lineTable').innerHTML = lineList.map(l=>{
    const pct = l.hist[l.hist.length-1]||0;
    let status;
    if(l.idx===faultLine) status='<span class="status-fault">AVARIYA</span>';
    else if(pct>88) status='<span class="status-warn">CHEGARAGA YAQIN</span>';
    else status='<span class="status-ok">ISHLAMOQDA</span>';
    return `<tr><td>${l.name}</td><td class="num">${l.kv}</td><td>${sparkSVG(l.hist, l.idx===faultLine?'--line-fault':(pct>88?'--amber':'--line-lo'))}</td><td class="num">${pct}%</td><td>${status}</td></tr>`;
  }).join('') || '<tr><td colspan="5" style="color:var(--dim);text-align:center;">Topilmadi</td></tr>';

  document.getElementById('genTable').innerHTML = genNodes.filter(g=>g.name.toLowerCase().includes(genFilter)).map(g=>{
    const out = g.hist[g.hist.length-1]||0;
    const pct = Math.round(out/g.cap*100);
    return `<tr><td>${g.name}</td><td class="num">${out.toFixed(0)}</td><td>${sparkSVG(g.hist,'--gen-col')}</td><td class="num">${pct}%</td><td><span class="status-ok">ISHDA</span></td></tr>`;
  }).join('') || '<tr><td colspan="5" style="color:var(--dim);text-align:center;">Topilmadi</td></tr>';

  document.getElementById('kpiLoad').innerHTML = totalLoad.toFixed(0)+' <span>MVt</span>';
  document.getElementById('kpiFreq').innerHTML = (49.94+rnd(-0.06,0.08)).toFixed(2)+' <span>Hz</span>';
  document.getElementById('kpiLines').innerHTML = (faultLine>=0? lines.length-1 : lines.length) +' <span>/ '+lines.length+'</span>';
  document.getElementById('kpiAlarms').innerHTML = (faultLine>=0? 1:0) +' <span>ta</span>';

  renderForecast();
}

function renderForecast(){
  const svg = document.getElementById('loadForecastSpark');
  const w=200,h=26;
  if(loadHistory.length<2){ svg.innerHTML=''; return; }
  const n = loadHistory.length;
  const xs = loadHistory.map((_,i)=>i);
  const meanX = xs.reduce((a,b)=>a+b,0)/n;
  const meanY = loadHistory.reduce((a,b)=>a+b,0)/n;
  let num=0, den=0;
  xs.forEach((x,i)=>{ num += (x-meanX)*(loadHistory[i]-meanY); den += (x-meanX)**2; });
  const slope = den? num/den : 0;
  const intercept = meanY - slope*meanX;
  const forecastPts = [n, n+1, n+2, n+3].map(x=> slope*x+intercept);
  const all = loadHistory.concat(forecastPts);
  const min=Math.min(...all), max=Math.max(...all), range=(max-min)||1;
  const toXY = (i,v)=> [ (i/(all.length-1))*w, h-((v-min)/range)*h ];
  const histPath = loadHistory.map((v,i)=>{ const [x,y]=toXY(i,v); return `${i===0?'M':'L'}${x.toFixed(1)},${y.toFixed(1)}`; }).join(' ');
  const fcPts = forecastPts.map((v,i)=>{ const [x,y]=toXY(n+i,v); return `${x.toFixed(1)},${y.toFixed(1)}`; });
  const lastHistPt = toXY(n-1, loadHistory[n-1]);
  const fcPath = `M${lastHistPt[0].toFixed(1)},${lastHistPt[1].toFixed(1)} L${fcPts.join(' L')}`;
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.innerHTML = `<path d="${histPath}" fill="none" stroke="var(--line-hi)" stroke-width="1.6"/><path d="${fcPath}" fill="none" stroke="var(--forecast)" stroke-width="1.4" stroke-dasharray="3 3"/>`;
}

/* ---------- Geographic projection ---------- */
const LON_MIN=55.8, LON_MAX=73.3, LAT_MIN=37.1, LAT_MAX=45.7;
const MAP_W=680, MAP_H=360, MAP_PAD=24;
function project(lon,lat){
  const x = MAP_PAD + (lon-LON_MIN)/(LON_MAX-LON_MIN) * (MAP_W-2*MAP_PAD);
  const y = MAP_PAD + (LAT_MAX-lat)/(LAT_MAX-LAT_MIN) * (MAP_H-2*MAP_PAD);
  return [x,y];
}
allNodes.forEach(n=>{ const [x,y]=project(n.lon,n.lat); n.x=x; n.y=y; });

/* ---------- Mimic diagram with zoom/pan ---------- */
const mimic = document.getElementById('mimic');
let viewState = {x:0,y:0,scale:1};
function applyView(){
  const g = document.getElementById('zoomGroup');
  if(g) g.setAttribute('transform', `translate(${viewState.x},${viewState.y}) scale(${viewState.scale})`);
}
document.getElementById('zoomIn').addEventListener('click', ()=>{ viewState.scale=Math.min(3,viewState.scale*1.2); applyView(); });
document.getElementById('zoomOut').addEventListener('click', ()=>{ viewState.scale=Math.max(0.5,viewState.scale/1.2); applyView(); });
document.getElementById('zoomReset').addEventListener('click', ()=>{ viewState={x:0,y:0,scale:1}; applyView(); });
mimic.addEventListener('wheel', e=>{
  e.preventDefault();
  const dir = e.deltaY<0 ? 1.1 : 0.9;
  viewState.scale = Math.min(3, Math.max(0.5, viewState.scale*dir));
  applyView();
}, {passive:false});
let dragging=false, dragStart={x:0,y:0};
mimic.addEventListener('pointerdown', e=>{ dragging=true; mimic.classList.add('dragging'); dragStart={x:e.clientX-viewState.x, y:e.clientY-viewState.y}; });
window.addEventListener('pointerup', ()=>{ dragging=false; mimic.classList.remove('dragging'); });
window.addEventListener('pointermove', e=>{ if(!dragging) return; viewState.x=e.clientX-dragStart.x; viewState.y=e.clientY-dragStart.y; applyView(); });

function buildMimic(){
  mimic.innerHTML = '';
  const zg = document.createElementNS(svgns,'g');
  zg.setAttribute('id','zoomGroup');
  mimic.appendChild(zg);

  // loose territory backdrop (schematic, not a precise border)
  const hull = document.createElementNS(svgns,'rect');
  const xs = allNodes.map(n=>n.x), ys = allNodes.map(n=>n.y);
  const minX=Math.min(...xs)-30, maxX=Math.max(...xs)+30, minY=Math.min(...ys)-25, maxY=Math.max(...ys)+25;
  hull.setAttribute('x',minX); hull.setAttribute('y',minY);
  hull.setAttribute('width',maxX-minX); hull.setAttribute('height',maxY-minY);
  hull.setAttribute('rx',18);
  hull.setAttribute('class','territory');
  zg.appendChild(hull);

  // generation feed connectors (drawn first, underneath)
  genEdges.forEach(([a,b])=>{
    const na=nodeById(a), nb=nodeById(b);
    const l = document.createElementNS(svgns,'line');
    l.setAttribute('x1',na.x); l.setAttribute('y1',na.y); l.setAttribute('x2',nb.x); l.setAttribute('y2',nb.y);
    l.setAttribute('class','line-gen flow-slow');
    zg.appendChild(l);
  });

  // backbone faultable lines
  lines.forEach((l,idx)=>{
    const na=nodeById(l.a), nb=nodeById(l.b);
    const isFault = idx===faultLine;
    const line = document.createElementNS(svgns,'line');
    line.setAttribute('x1',na.x); line.setAttribute('y1',na.y); line.setAttribute('x2',nb.x); line.setAttribute('y2',nb.y);
    line.setAttribute('class', isFault ? 'line-fault' : (l.kv>=220 ? 'line-hi flow' : 'line-lo flow'));
    zg.appendChild(line);
    const hit = document.createElementNS(svgns,'line');
    hit.setAttribute('x1',na.x); hit.setAttribute('y1',na.y); hit.setAttribute('x2',nb.x); hit.setAttribute('y2',nb.y);
    hit.setAttribute('class','line-hit');
    hit.addEventListener('click', ()=> openLineDetail(idx));
    zg.appendChild(hit);
  });

  // grid nodes (rectangles)
  gridNodes.forEach(s=>{
    const grp = document.createElementNS(svgns,'g'); grp.style.cursor='pointer';
    const rect = document.createElementNS(svgns,'rect');
    rect.setAttribute('x',s.x-32); rect.setAttribute('y',s.y-12); rect.setAttribute('width',64); rect.setAttribute('height',24); rect.setAttribute('rx',3);
    rect.setAttribute('class','node-box');
    grp.appendChild(rect);
    const breaker = document.createElementNS(svgns,'circle');
    breaker.setAttribute('cx',s.x-26); breaker.setAttribute('cy',s.y-7); breaker.setAttribute('r',2.6);
    const adj = lines.some((l,idx)=> idx===faultLine && (l.a===s.id||l.b===s.id));
    breaker.setAttribute('class', adj ? 'breaker-off pulse' : 'breaker-on');
    grp.appendChild(breaker);
    const t1 = document.createElementNS(svgns,'text');
    t1.setAttribute('x',s.x); t1.setAttribute('y',s.y-1); t1.setAttribute('text-anchor','middle'); t1.setAttribute('class','node-label'); t1.textContent = s.name;
    grp.appendChild(t1);
    const t2 = document.createElementNS(svgns,'text');
    t2.setAttribute('x',s.x); t2.setAttribute('y',s.y+9); t2.setAttribute('text-anchor','middle'); t2.setAttribute('class','node-sub'); t2.textContent = s.kv+' kV';
    grp.appendChild(t2);
    grp.addEventListener('click', ()=> openSubDetail(s.id));
    zg.appendChild(grp);
  });

  // generation nodes (circles)
  genNodes.forEach(g=>{
    const grp = document.createElementNS(svgns,'g'); grp.style.cursor='pointer';
    const circ = document.createElementNS(svgns,'circle');
    circ.setAttribute('cx',g.x); circ.setAttribute('cy',g.y); circ.setAttribute('r',9);
    circ.setAttribute('class','node-box gen');
    grp.appendChild(circ);
    const bolt = document.createElementNS(svgns,'text');
    bolt.setAttribute('x',g.x); bolt.setAttribute('y',g.y+3); bolt.setAttribute('text-anchor','middle');
    bolt.setAttribute('style','font-size:9px; fill:var(--gen-col); pointer-events:none;');
    bolt.textContent = '⚡';
    grp.appendChild(bolt);
    const t1 = document.createElementNS(svgns,'text');
    t1.setAttribute('x',g.x); t1.setAttribute('y',g.y-13); t1.setAttribute('text-anchor','middle'); t1.setAttribute('class','node-sub'); t1.textContent = g.name;
    grp.appendChild(t1);
    grp.addEventListener('click', ()=> openGenDetail(g.id));
    zg.appendChild(grp);
  });

  applyView();
}

const overlay = document.getElementById('detailOverlay');
document.getElementById('detailClose').addEventListener('click', ()=> overlay.classList.remove('show'));
overlay.addEventListener('click', e=>{ if(e.target===overlay) overlay.classList.remove('show'); });

function drawDetailChart(hist, colorVar){
  const svg = document.getElementById('detailChart');
  if(hist.length<2){ svg.innerHTML=''; return; }
  const min=Math.min(...hist), max=Math.max(...hist), range=(max-min)||1;
  const pts = hist.map((v,i)=>{ const x=(i/(hist.length-1))*300; const y=100-((v-min)/range)*90-5; return `${x.toFixed(1)},${y.toFixed(1)}`; });
  svg.innerHTML = `<polyline points="${pts.join(' ')}" fill="none" stroke="var(${colorVar})" stroke-width="2"/>`;
}
function openSubDetail(id){
  const s = nodeById(id);
  document.getElementById('detailTitle').textContent = s.name;
  document.getElementById('detailSub').textContent = `Podstansiya — ${s.kv} kV — Tarixiy yuklama grafigi`;
  drawDetailChart(s.hist, '--line-hi');
  const last = s.hist[s.hist.length-1]||s.base;
  document.getElementById('detailGrid').innerHTML = `
    <div><span>Joriy yuklama</span>${last.toFixed(1)} MVt</div>
    <div><span>Bazaviy yuklama</span>${s.base} MVt</div>
    <div><span>Oqim</span>${Math.round(last*1000/(s.kv*1.73))} A</div>
    <div><span>Holat</span>${last>s.base*1.12?'Yuqori yuklama':'Norma'}</div>`;
  document.getElementById('detailMapLink').href = s.mapsUrl || '#';
  overlay.classList.add('show');
}
function openGenDetail(id){
  const g = nodeById(id);
  document.getElementById('detailTitle').textContent = g.name;
  document.getElementById('detailSub').textContent = `Generatsiya manbai — Qobiliyat: ${g.cap} MVt`;
  drawDetailChart(g.hist, '--gen-col');
  const last = g.hist[g.hist.length-1]||0;
  document.getElementById('detailGrid').innerHTML = `
    <div><span>Joriy ishlab chiqarish</span>${last.toFixed(0)} MVt</div>
    <div><span>Nominal qobiliyat</span>${g.cap} MVt</div>
    <div><span>Yuklanish</span>${Math.round(last/g.cap*100)}%</div>
    <div><span>Holat</span>Ishda</div>`;
  document.getElementById('detailMapLink').href = g.mapsUrl || '#';
  overlay.classList.add('show');
}
function openLineDetail(idx){
  const l = lines[idx];
  document.getElementById('detailTitle').textContent = l.name;
  document.getElementById('detailSub').textContent = `Magistral liniya — ${l.kv} kV — Tarixiy yuklama grafigi (%)`;
  drawDetailChart(l.hist, idx===faultLine?'--line-fault':'--line-lo');
  const last = l.hist[l.hist.length-1]||0;
  document.getElementById('detailGrid').innerHTML = `
    <div><span>Joriy yuklama</span>${last}%</div>
    <div><span>Kuchlanish</span>${l.kv} kV</div>
    <div><span>Holat</span>${idx===faultLine?'Avariya':'Ishlamoqda'}</div>
    <div><span>ID</span>Liniya #${idx+1}</div>`;
  document.getElementById('detailMapLink').href = nodeById(l.a).mapsUrl || '#';
  overlay.classList.add('show');
}

function simTick(){
  gridNodes.forEach(s=>{ pushHist(s.hist, Math.max(10, s.base + rnd(-8,8))); });
  lines.forEach((l,i)=>{ pushHist(l.hist, i===faultLine ? 0 : Math.round(rnd(38,96))); });
  genNodes.forEach(g=>{ pushHist(g.hist, g.cap*rnd(0.5,0.97)); });
  const total = gridNodes.reduce((sum,s)=> sum + (s.hist[s.hist.length-1]||s.base), 0);
  pushHist(loadHistory, total, 20);

  if(faultLine===-1 && Math.random()<0.05){
    faultLine = Math.floor(Math.random()*lines.length);
    pushAlarm(`AVARIYA: "${lines[faultLine].name}" liniyasida uzilish aniqlandi`, 'crit');
    buildMimic();
  } else if(faultLine!==-1 && Math.random()<0.35){
    pushAlarm(`Tiklandi: "${lines[faultLine].name}" liniyasi qayta ishga tushirildi`, 'info');
    faultLine = -1;
    buildMimic();
  } else if(Math.random()<0.18){
    const s = gridNodes[Math.floor(Math.random()*gridNodes.length)];
    pushAlarm(`${s.name}: yuklama chegarasiga yaqinlashmoqda`, 'warn');
  }
  renderTables();
}

let mapsFilter='';
function renderMapsLinks(){
  const cardStyle="background:var(--bg); border:1px solid var(--border); border-radius:5px; padding:7px 9px; display:flex; flex-direction:column; gap:2px; text-decoration:none; color:var(--text); font-size:10px;";
  document.getElementById('mapsLinksGen').innerHTML = genNodes.filter(g=>g.name.toLowerCase().includes(mapsFilter)).map(g=>`
    <a href="${g.mapsUrl}" target="_blank" rel="noopener" style="${cardStyle}">
      <span style="color:var(--gen-col); font-weight:600;">⚡ ${g.name}</span>
      <span style="color:var(--dim); font-size:9px;">${g.cap} MVt qobiliyat · 📍 xaritada ko'rish</span>
    </a>`).join('') || '<div style="color:var(--dim);font-size:10px;padding:6px;">Topilmadi</div>';
  document.getElementById('mapsLinksGrid').innerHTML = gridNodes.filter(s=>s.name.toLowerCase().includes(mapsFilter)).map(s=>`
    <a href="${s.mapsUrl}" target="_blank" rel="noopener" style="${cardStyle}">
      <span style="color:var(--line-lo); font-weight:600;">◆ ${s.name}</span>
      <span style="color:var(--dim); font-size:9px;">${s.kv} kV podstansiya · 📍 xaritada ko'rish</span>
    </a>`).join('') || '<div style="color:var(--dim);font-size:10px;padding:6px;">Topilmadi</div>';
}
document.getElementById('mapsSearch').addEventListener('input', e=>{ mapsFilter=e.target.value.toLowerCase(); renderMapsLinks(); });

(async function init(){
  await loadAlarmsFromStorage();
  gridNodes.forEach(s=> pushHist(s.hist, s.base));
  lines.forEach(l=> pushHist(l.hist, Math.round(rnd(38,96))));
  genNodes.forEach(g=> pushHist(g.hist, g.cap*0.75));
  pushHist(loadHistory, gridNodes.reduce((sum,s)=>sum+s.base,0), 20);
  buildMimic();
  renderTables();
  renderMapsLinks();
  if(alarms.length===0) pushAlarm('Tizim ishga tushirildi. Barcha liniyalar nazoratda.', 'info');
  setInterval(simTick, 3000);
})();
</script>

</body>
</html>
