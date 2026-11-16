"""Slides 04 a 06 — portos brasileiros, a partir de dados/portos.json.

O JSON foi levantado em 16/11/2026 no Estatístico Aquaviário da ANTAQ e nos painéis de
instalações privadas e de administração portuária (dados públicos, via conector MCP
independente). Valores brutos da fonte; as variações são calculadas.

Chamado por build_slides.py; não roda sozinho.
"""

import json

FONTE = ("Fonte: ANTAQ, Estatístico Aquaviário (peso bruto movimentado), via conector MCP independente, "
         "consulta em 16/11/2026")
RECADO = ("<strong style='color:#FFD700;'>1,40 bilhão de toneladas</strong> movimentadas em 2025 (+6,1%), "
          "64,6% delas em terminais autorizados.")

# Rótulos curtos para o ranking e o mapa (o nome completo vai no tooltip).
CURTO = {
    "Terminal Marítimo de Ponta da Madeira": "Ponta da Madeira",
    "Terminal de Tubarão": "Tubarão",
    "Terminal Aquaviário de Angra dos Reis": "TA Angra dos Reis",
    "Terminal de Petróleo TPET/TOIL - Açu": "TPET/TOIL Açu",
    "Terminal Aquaviário de São Sebastião (Almirante Barroso)": "TA São Sebastião",
    "Terminal da Ilha Guaíba - TIG": "Ilha Guaíba (TIG)",
    "Porto Sudeste do Brasil S/A": "Porto Sudeste",
}
PERFIL_CURTO = {"Granel Sólido": "granel sólido", "Granel Líquido e Gasoso": "granel líquido e gasoso",
                "Carga Conteinerizada": "carga conteinerizada", "Carga Geral": "carga geral"}


def gerar(slide, h, d):
    br, card, stat, segbar, chaves, graficos = (h["br"], h["card"], h["stat"], h["segbar"], h["chaves"], h["graficos"])

    # ------------------------------------------------------------------ 04
    anos = [a for a in d["serie_total"]["anos"] if not a["parcial"]]
    tot = {a["ano"]: a["toneladas"] for a in anos}
    inst = d["serie_instalacao"]["por_tipo"]
    po = [round(inst["Porto Organizado"]["anos"][str(a)]["toneladas"] / 1e6, 1) for a in tot]
    ta = [round(inst["Terminal Autorizado"]["anos"][str(a)]["toneladas"] / 1e6, 1) for a in tot]
    t25, t24 = tot[2025], tot[2024]
    var25 = 100 * (t25 / t24 - 1)
    sh_ta = 100 * inst["Terminal Autorizado"]["anos"]["2025"]["participacao"]
    teu = {a["ano"]: a["teu"] for a in d["teu"]["anos"]}
    var_teu = 100 * (teu[2025] / teu[2024] - 1)
    p26 = d["serie_total"]["parcial_2026"]
    nav = {l["tipo_navegacao"]: l for l in d["navegacao_2025"]["linhas"]}
    perf = d["serie_perfil"]["por_perfil"]
    sh = lambda k: 100 * perf[k]["anos"]["2025"]["participacao"]
    assert abs(var25 - 6.07) < 0.01 and abs(sh_ta - 64.63) < 0.01 and abs(var_teu - 10.33) < 0.01

    CORES_PERFIL = [("Granel sólido", "#6250d6", "Granel Sólido", "#fff"),
                    ("Granel líquido e gasoso", "#1baf7a", "Granel Líquido e Gasoso", "#fff"),
                    ("Carga conteinerizada", "#eda100", "Carga Conteinerizada", "#0F172A"),
                    ("Carga geral", "#e87ba4", "Carga Geral", "#fff")]
    partes = []
    for nome, cor, k, tinta in CORES_PERFIL:
        p = sh(k)
        rot = f"{br(p, 1)}%" if p >= 8 else ""
        partes.append((rot, perf[k]["anos"]["2025"]["toneladas"], cor))
    barra_perfil = segbar(partes)
    # o amarelo pede texto escuro (contraste)
    barra_perfil = barra_perfil.replace("background:#eda100;", "background:#eda100; color:#0F172A;")

    js4 = f"""
var anos = {json.dumps([str(a) for a in tot])}, po = {po}, ta = {ta};
var totais = po.map(function (v, i) {{ return Math.round((v + ta[i]) * 10) / 10; }});
G.desenha('g-mov', {{
  grid: {{ left: 70, right: 20, top: 56, bottom: 36 }},
  legend: G.legenda({{ data: ['Terminais autorizados', 'Portos organizados'] }}),
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'shadow', shadowStyle: {{ color: 'rgba(148,163,184,.14)' }} }},
    formatter: function (ps) {{ var i = ps[0].dataIndex;
      return '<b>' + ps[0].name + '</b><br/>' + ps.map(function (p) {{ return p.marker + p.seriesName + ': <b>' + G.num(p.value, 1) + ' mi t</b> (' + G.pct(100 * p.value / totais[i]) + ')'; }}).join('<br/>')
        + '<br/>Total: <b>' + G.num(totais[i], 1) + ' mi t</b>'; }} }}),
  xAxis: G.eixoCat(anos),
  yAxis: G.eixoVal({{ min: 0, max: 1600, interval: 400, name: 'milhões de t', nameTextStyle: {{ color: C.apagado, fontFamily: G.FC, fontSize: 15, align: 'left' }} }}),
  series: [
    {{ name: 'Portos organizados', type: 'bar', stack: 'm', data: po, barMaxWidth: 64,
       itemStyle: {{ color: C.po, borderColor: '#fff', borderWidth: 2 }} }},
    {{ name: 'Terminais autorizados', type: 'bar', stack: 'm', data: ta, barMaxWidth: 64,
       itemStyle: {{ color: C.tup, borderColor: '#fff', borderWidth: 2, borderRadius: [4, 4, 0, 0] }},
       label: {{ show: true, position: 'top', distance: 8, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 18,
         formatter: function (p) {{ return G.num(totais[p.dataIndex], 1); }} }} }}
  ]
}});
"""
    slide(4, 2, "O setor portuário em 2025", "Portos brasileiros · Movimentação", "O setor portuário em 2025", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-8 items-center min-h-0">
    <div class="col-span-4 flex flex-col gap-4">
      <div class="grid grid-cols-2 gap-4">
        {stat(br(t25 / 1e9, 2) + " bi", "toneladas movimentadas em 2025")}
        {stat("+" + br(var25, 1) + "%", "sobre 2024; maior volume desde 2021")}
        {stat(br(sh_ta, 1) + "%", "em terminais autorizados (TUP, ETC e outros)")}
        {stat(br(teu[2025] / 1e6, 1) + " mi", f"TEU em contêineres, +{br(var_teu, 1)}%")}
      </div>
      {card("fa-earth-americas", "O longo curso leva " + br(100 * nav["Longo Curso"]["participacao"], 1) + "%",
            f"A cabotagem fica com <b>{br(100 * nav['Cabotagem']['participacao'], 1)}%</b> e a navegação interior com <b>{br(100 * nav['Interior']['participacao'], 1)}%</b> da tonelagem movimentada.")}
      {card("fa-arrow-trend-up", "2026 começou em alta",
            f"Em janeiro e fevereiro, <b>{br(p26['toneladas_2026_parcial'] / 1e6, 1)} mi t</b>, {br(100 * p26['variacao_calculada'], 1)}% acima do mesmo bimestre de 2025. É o único período de 2026 já apurado.", "card-gold")}
    </div>
    <div class="col-span-8 flex flex-col gap-4">
      <div class="painel">
        <p class="ct">Movimentação por tipo de instalação, 2021–2025</p>
        <p class="cd" style="margin:0;">Milhões de toneladas, peso bruto; total do ano sobre cada coluna</p>
        <div id="g-mov" class="graf" style="height:440px;"></div>
      </div>
      <div class="painel" style="padding-bottom:16px;">
        <div class="flex items-end justify-between" style="margin-bottom:10px;"><p class="ct">Perfil da carga em 2025</p>{chaves([(n, c) for n, c, *_ in CORES_PERFIL])}</div>
        {barra_perfil}
        <p class="legenda" style="margin-top:8px;">Granel sólido inclui minério, mas também soja, milho e fertilizantes. Carga geral: {br(sh("Carga Geral"), 1)}%.</p>
      </div>
      <p class="legenda">{FONTE}. TEU: microdados do Estatístico Aquaviário. Na movimentação a cabotagem conta duas vezes, no embarque e no desembarque.</p>
    </div>
  </div>""", js_extra=graficos(js4))

    # ------------------------------------------------------------------ 05
    rk_po = {l["porto"]: l for l in d["ranking_portos_2025"]["linhas"]}
    rk_tup = {l["terminal"]: l for l in d["ranking_tups_2025"]["linhas"]}
    pts = []
    for p in d["mapa"]["pontos"]:
        rk = rk_po.get(p["nome"]) if p["tipo"] == "porto_organizado" else rk_tup.get(p["nome"])
        v = rk.get("variacao_2024_2025_calculada") if rk else None
        pts.append(dict(
            n=p["nome"], c=CURTO.get(p["nome"], p["nome"]), t="po" if p["tipo"] == "porto_organizado" else "tup",
            uf=p["uf"], mun=p["municipio"],
            lat=p["lat"], lon=p["lon"], ton=p["toneladas_2025"],
            pf=PERFIL_CURTO.get(p["perfil_predominante"] or "", ""),
            pp=round(100 * p["participacao_do_perfil"]) if p["participacao_do_perfil"] else None,
            v=round(100 * v, 1) if v is not None else None, ap=p.get("autoridade_portuaria"), obs=p.get("obs")))
    # corrige os municípios que a fonte grava errado (ver municipio_nota no JSON)
    for q in pts:
        q["mun"] = {"Angra": "Angra dos Reis", "Aratu": "Candeias"}.get(q["mun"], q["mun"])
        if q["n"] == "Cabedelo":
            q["mun"] = "Cabedelo"
    n_po = sum(1 for q in pts if q["t"] == "po")
    n_tup = sum(1 for q in pts if q["t"] == "tup")
    assert (n_po, n_tup) == (35, 25)
    top = sorted([q for q in pts if q["ton"]], key=lambda q: -q["ton"])[:5]
    lista = "\n".join(
        f'        <button class="item-top" data-n="{q["n"]}" tabindex="-1"><span class="sw" style="background:{"#0066CC" if q["t"] == "po" else "#eb6834"}; border-radius:50%;"></span>'
        f'<span class="it-nome">{q["c"]} <span class="it-uf">{q["uf"]}</span></span><span class="it-val">{br(q["ton"] / 1e6, 1)}</span></button>'
        for q in top)

    css5 = """
.mapa-wrap { position:relative; border-radius:16px; overflow:hidden; border:1px solid #E2E8F0; box-shadow:0 8px 24px rgba(15,23,42,.10); }
#mapa { width:100%; height:100%; background:#E3EBF4; }
.leaflet-container { font-family:'Open Sans',sans-serif; }
.leaflet-control-zoom a { width:46px !important; height:46px !important; line-height:46px !important; font-size:26px !important; }
.leaflet-control-attribution { font-size:13px !important; }
.dica-mapa { font-family:'Open Sans',sans-serif; font-size:17px; line-height:1.45; padding:10px 14px; border-radius:10px; border:1px solid #E2E8F0; box-shadow:0 8px 24px rgba(15,23,42,.16); color:#0F172A; }
.dica-mapa b { font-family:'Montserrat',sans-serif; color:#003366; font-size:18px; }
.dica-mapa .tp { font-family:'Montserrat',sans-serif; font-weight:700; font-size:13px; letter-spacing:.06em; text-transform:uppercase; }
.rot-mapa span { font-family:'Montserrat',sans-serif; font-weight:700; font-size:16px; color:#0F172A; white-space:nowrap;
  text-shadow:0 0 3px #fff, 0 0 3px #fff, 0 0 3px #fff, 0 0 6px #fff; }
.filtros { display:flex; flex-wrap:wrap; gap:8px; }
.filtros button { font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(15px * var(--tz)); padding:7px 14px; border-radius:999px;
  border:1.5px solid #CBD5E1; background:#fff; color:#334155; cursor:pointer; transition:all .15s; }
.filtros button:hover { border-color:#0066CC; color:#0066CC; }
.filtros button.on { background:#003366; border-color:#003366; color:#fff; }
.item-top { display:flex; align-items:center; gap:10px; width:100%; padding:7px 10px; border-radius:10px; border:0; background:transparent; cursor:pointer; text-align:left; }
.item-top:hover { background:#EFF6FF; }
.it-nome { flex:1; font-family:'Montserrat',sans-serif; font-weight:600; color:#0F172A; font-size:calc(17px * var(--tz)); }
.it-uf { color:#64748B; font-weight:600; font-size:calc(14px * var(--tz)); margin-left:4px; }
.it-val { font-family:'Montserrat',sans-serif; font-weight:800; color:#003366; font-size:calc(18px * var(--tz)); font-variant-numeric:tabular-nums; }
"""
    js5 = """
var PTS = %s;
var REG = { brasil: [[-33.8, -73.9], [5.3, -34.7]], norte: [[-11.2, -64.6], [1.2, -47.6]], nordeste: [[-15.2, -46.2], [-1.6, -34.4]],
            sudeste: [[-24.4, -47.6], [-19.6, -39.6]], sul: [[-32.4, -53.6], [-25.0, -47.9]] };
var el = document.getElementById('mapa');
var map = L.map(el, { keyboard: false, zoomSnap: 0.25, zoomDelta: 0.5, minZoom: 3.75, maxZoom: 9, attributionControl: true, zoomControl: true });
map.attributionControl.setPrefix(false);
/* Fundo vetorial (malha estadual do IBGE, local): funciona sem internet e não sugere uma
   precisão de rua que as coordenadas aproximadas dos pontos não têm. */
L.geoJSON(window.BRASIL_UF, { interactive: false, attribution: 'Malha estadual: IBGE',
  style: { color: '#A3B1C2', weight: 1, fillColor: '#ffffff', fillOpacity: 1 } }).addTo(map);
map.fitBounds(REG.brasil, { padding: [8, 8] });

var MAXT = 172389190;
function raio(t) { return t > 0 ? 5 + 34 * Math.sqrt(t / MAXT) : 5; }
function dica(p) {
  var tipo = p.t === 'po' ? '<span class="tp" style="color:#0066CC;">Porto organizado</span>' : '<span class="tp" style="color:#c2410c;">Terminal de uso privado</span>';
  var s = tipo + '<br/><b>' + p.n + '</b><br/>' + (p.mun ? p.mun + ' (' + p.uf + ')' : p.uf);
  if (p.ton > 0) {
    s += '<br/><b style="font-size:20px;">' + G.num(p.ton / 1e6, 1) + ' mi t</b> em 2025';
    if (p.v !== null) s += ' &middot; ' + (p.v >= 0 ? '+' : '') + G.num(p.v, 1) + '%% sobre 2024';
    if (p.pf) s += '<br/>Perfil: ' + p.pf + (p.pp ? ' (' + p.pp + '%%)' : '');
  } else {
    s += '<br/>' + (p.ton === 0 ? 'Sem movimentação registrada em 2025' : 'Sem linha no Estatístico Aquaviário');
  }
  if (p.ap) s += '<br/>Autoridade portuária: ' + p.ap;
  return s;
}
var camadas = { po: L.layerGroup().addTo(map), tup: L.layerGroup().addTo(map) }, marc = {};
PTS.slice().sort(function (a, b) { return (b.ton || 0) - (a.ton || 0); }).forEach(function (p) {
  var cor = p.t === 'po' ? G.C.po : G.C.tup, r = raio(p.ton), cheio = p.ton > 0;
  var m = L.circleMarker([p.lat, p.lon], { radius: G.reduz ? r : 0.1, color: cheio ? '#ffffff' : cor, weight: cheio ? 1.5 : 2.5,
    fillColor: cor, fillOpacity: cheio ? 0.55 : 0, opacity: 1 });
  m._alvo = r;
  m.bindTooltip(dica(p), { className: 'dica-mapa', direction: 'top', offset: [0, -r + 2], opacity: 1 });
  m.on('mouseover', function () { m.setStyle({ fillOpacity: cheio ? 0.9 : 0, weight: 3 }); m.bringToFront(); });
  m.on('mouseout', function () { m.setStyle({ fillOpacity: cheio ? 0.55 : 0, weight: cheio ? 1.5 : 2.5 }); });
  camadas[p.t].addLayer(m); marc[p.n] = m;
});
/* rótulos fixos só nos quatro maiores, que não se sobrepõem em escala Brasil */
[['Terminal Marítimo de Ponta da Madeira', 'Ponta da Madeira', 'd'], ['Santos', 'Santos', 'e'],
 ['Terminal de Tubarão', 'Tubarão', 'd'], ['Paranaguá', 'Paranaguá', 'e']].forEach(function (x) {
  var p = PTS.filter(function (q) { return q.n === x[0]; })[0], r = raio(p.ton);
  var dx = x[2] === 'd' ? r + 6 : -(r + 6);
  L.marker([p.lat, p.lon], { interactive: false, keyboard: false,
    icon: L.divIcon({ className: 'rot-mapa', html: '<span style="position:absolute; top:-11px; ' + (x[2] === 'd' ? 'left:' + dx + 'px;' : 'right:' + (-dx) + 'px;') + '">' + x[1] + '</span>', iconSize: [0, 0] }) })
    .addTo(map);
});
/* bolhas crescem depois que o painel do mapa pousa */
var ordem = Object.keys(marc).map(function (k) { return marc[k]; });
if (!G.reduz) setTimeout(function () {
  var t0 = performance.now();
  (function passo(t) {
    var vivo = false;
    ordem.forEach(function (m, i) {
      var f = Math.min(1, Math.max(0, (t - t0 - i * 18) / 650)), e = 1 - Math.pow(1 - f, 3);
      m.setRadius(Math.max(0.1, m._alvo * e)); if (f < 1) vivo = true;
    });
    if (vivo) requestAnimationFrame(passo);
  })(t0);
}, G.atraso(el));

function filtro(qual) {
  ['po', 'tup'].forEach(function (k) { if (qual === 'todos' || qual === k) map.addLayer(camadas[k]); else map.removeLayer(camadas[k]); });
  document.querySelectorAll('[data-f]').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-f') === qual); });
}
document.querySelectorAll('[data-f]').forEach(function (b) { b.addEventListener('click', function () { filtro(b.getAttribute('data-f')); b.blur(); }); });
document.querySelectorAll('[data-r]').forEach(function (b) {
  b.addEventListener('click', function () {
    map.flyToBounds(REG[b.getAttribute('data-r')], { padding: [12, 12], duration: 0.9 });
    document.querySelectorAll('[data-r]').forEach(function (o) { o.classList.toggle('on', o === b); }); b.blur();
  });
});
document.querySelectorAll('.item-top').forEach(function (b) {
  b.addEventListener('click', function () {
    var m = marc[b.getAttribute('data-n')]; if (!m) return;
    filtro('todos');
    map.flyTo(m.getLatLng(), 8.5, { duration: 1.0 });
    map.once('moveend', function () { m.openTooltip(); });
    document.querySelectorAll('[data-r]').forEach(function (o) { o.classList.remove('on'); }); b.blur();
  });
});
""" % json.dumps(pts, ensure_ascii=False)

    def bolha(mt):
        import math
        return 5 + 34 * math.sqrt(mt * 1e6 / 172389190)
    r1, r2, r3 = bolha(10), bolha(50), bolha(170)
    T = 12  # folga no topo para o rótulo do maior círculo
    svg_bolhas = (f'<svg width="200" height="{2 * r3 + 4 + T:.0f}" viewBox="0 0 200 {2 * r3 + 4 + T:.0f}" aria-hidden="true">'
                  + "".join(f'<circle cx="{r3 + 2:.1f}" cy="{T + 2 * r3 + 2 - r:.1f}" r="{r:.1f}" fill="none" stroke="#94A3B8" stroke-width="1.5"/>'
                            f'<line x1="{r3 + 2:.1f}" y1="{T + 2 * r3 + 2 - 2 * r:.1f}" x2="{2 * r3 + 30:.1f}" y2="{T + 2 * r3 + 2 - 2 * r:.1f}" stroke="#CBD5E1" stroke-width="1"/>'
                            f'<text x="{2 * r3 + 34:.1f}" y="{T + 2 * r3 + 7 - 2 * r:.1f}" font-family="Montserrat" font-weight="700" font-size="15" fill="#475569">{lbl}</text>'
                            for r, lbl in ((r3, "170 mi t"), (r2, "50 mi t"), (r1, "10 mi t")))
                  + '</svg>')

    slide(5, 2, "Mapa dos portos e terminais", "Portos brasileiros · Mapa interativo", "Portos e terminais privados", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-8 min-h-0" style="align-items:stretch; padding-top:6px;">
    <div class="col-span-8 painel mapa-wrap" style="padding:0;"><div id="mapa"></div></div>
    <div class="col-span-4 flex flex-col gap-4" style="justify-content:center;">
      <div class="card" style="flex-direction:column; align-items:stretch; gap:10px;">
        <p class="sec">Mostrar</p>
        <div class="filtros"><button data-f="todos" class="on" tabindex="-1">Todos</button><button data-f="po" tabindex="-1">Portos organizados</button><button data-f="tup" tabindex="-1">Terminais privados</button></div>
        <p class="sec" style="margin-top:6px;">Ir para</p>
        <div class="filtros"><button data-r="brasil" class="on" tabindex="-1">Brasil</button><button data-r="norte" tabindex="-1">Norte</button><button data-r="nordeste" tabindex="-1">Nordeste</button><button data-r="sudeste" tabindex="-1">Sudeste</button><button data-r="sul" tabindex="-1">Sul</button></div>
      </div>
      <div class="card" style="flex-direction:column; align-items:stretch; gap:8px;">
        <p class="sec">Bolha proporcional à tonelagem de 2025</p>
        <div class="flex items-center gap-6">
          <div class="flex flex-col gap-2">
            {chaves([(f"Portos organizados ({n_po})", "#0066CC"), (f"Maiores TUPs ({n_tup})", "#eb6834")]).replace('class="chaves"', 'class="chaves" style="flex-direction:column;"').replace('<span class="sw" style="', '<span class="sw" style="border-radius:50%; ')}
          </div>
          <div style="margin-left:auto;">{svg_bolhas}</div>
        </div>
      </div>
      <div class="card" style="flex-direction:column; align-items:stretch; gap:2px; padding:12px 12px;">
        <div class="flex items-center justify-between" style="padding:0 10px 4px;"><p class="sec">As cinco maiores · clique para ver</p><p class="sec">mi t</p></div>
{lista}
      </div>
      <p class="legenda">Os 35 portos organizados e os 25 TUPs que mais movimentaram. Barra do Riacho e Laguna não têm linha no Estatístico Aquaviário; Forno e Manaus registram 0 t (círculo vazado). Posições aproximadas: nenhum painel publica coordenadas.</p>
      <p class="legenda">Fonte: ANTAQ, Estatístico Aquaviário e cadastros de portos e instalações privadas, via conector MCP independente, 16/11/2026. Malha: IBGE.</p>
    </div>
  </div>""", extra_css=css5, head_extra=h["LEAFLET_CSS"],
          js_extra=h["LEAFLET_JS"] + '\n<script src="dados/brasil-uf.js"></script>\n' + graficos(js5).replace(h["ECHARTS"] + "\n", ""))

    # ------------------------------------------------------------------ 06
    inst_all = ([("po", l["porto"], l["uf"], l["toneladas_2025"], l["variacao_2024_2025_calculada"], l["perfil_predominante"])
                 for l in d["ranking_portos_2025"]["linhas"]]
                + [("tup", l["terminal"], l["uf"], l["toneladas_2025"], l["variacao_2024_2025_calculada"], l["perfil_predominante"])
                   for l in d["ranking_tups_2025"]["linhas"]])
    top12 = sorted(inst_all, key=lambda x: -x[3])[:12]
    rk = [dict(r=f"{CURTO.get(n, n)} ({uf})", n=n, t=t, v=round(ton / 1e6, 1), var=round(100 * va, 1), pf=PERFIL_CURTO.get(pf, ""))
          for t, n, uf, ton, va, pf in top12]
    pm = next(x for x in rk if x["n"].startswith("Terminal Marítimo de Ponta"))
    santos = next(x for x in rk if x["n"] == "Santos")
    acima = 100 * (pm["v"] / santos["v"] - 1)

    merc = d["mercadorias_2025"]["top10"]
    nomes_m = {"Petróleo e Derivados (Óleo Bruto)": "Petróleo bruto", "Petróleo e Derivados (Sem Óleo Bruto)": "Derivados de petróleo",
               "Contêineres": "Contêineres", "Adubos (fertilizantes)": "Fertilizantes",
               "Minério de Ferro": "Minério de ferro", "Ferro e Aço": "Ferro e aço"}
    tm = [dict(name=nomes_m.get(m["mercadoria"], m["mercadoria"]), value=round(m["toneladas_2025"] / 1e6, 1),
               sh=round(100 * m["participacao_2025"], 1), var=round(100 * m["variacao_2024_2025_calculada"], 1))
          for m in merc]
    outros = t25 - sum(m["toneladas_2025"] for m in merc)
    tm.append(dict(name="Demais grupos", value=round(outros / 1e6, 1), sh=round(100 * outros / t25, 1), var=None))
    for m in tm:  # nome curto no bloco; o nome inteiro fica no tooltip
        m["curto"] = {"Derivados de petróleo": "Derivados", "Fertilizantes": "Adubos", "Ferro e aço": "Aço"}.get(m["name"], m["name"])
    # Abaixo de 60 mi t o bloco é estreito: leva só nome curto e valor, em fonte menor.
    soja = next(m for m in tm if m["name"] == "Soja")
    minerio = next(m for m in tm if m["name"] == "Minério de ferro")

    js6 = f"""
var RK = {json.dumps(rk, ensure_ascii=False)};
G.desenha('g-rank', {{
  grid: {{ left: 230, right: 120, top: 44, bottom: 6 }},
  legend: G.legenda({{ data: [{{ name: 'Terminal de uso privado' }}, {{ name: 'Porto organizado' }}] }}),
  tooltip: G.dica({{ trigger: 'item', formatter: function (p) {{ var x = RK[p.dataIndex];
    return '<b>' + x.n + '</b><br/>' + (x.t === 'po' ? 'Porto organizado' : 'Terminal de uso privado') + '<br/>' + G.num(x.v, 1) + ' mi t em 2025 &middot; '
      + (x.var >= 0 ? '+' : '') + G.num(x.var, 1) + '% sobre 2024' + (x.pf ? '<br/>Perfil predominante: ' + x.pf : ''); }} }}),
  xAxis: G.eixoVal({{ show: false, max: 190 }}),
  yAxis: G.eixoCat(RK.map(function (x) {{ return x.r; }}), {{ inverse: true, axisLine: {{ show: false }},
    axisLabel: {{ color: C.tinta2, fontFamily: G.FT, fontSize: 16, fontWeight: 600, margin: 14 }} }}),
  series: [
    {{ name: 'Terminal de uso privado', type: 'bar', stack: 'r', barMaxWidth: 24, data: RK.map(function (x) {{ return x.t === 'tup' ? x.v : '-'; }}),
       itemStyle: {{ color: C.tup, borderRadius: [0, 4, 4, 0] }},
       label: {{ show: true, position: 'right', distance: 8, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 16,
         formatter: function (p) {{ var x = RK[p.dataIndex]; return G.num(x.v, 1) + '  {{v|' + (x.var >= 0 ? '+' : '') + G.num(x.var, 1) + '%}}'; }},
         rich: {{ v: {{ color: C.apagado, fontFamily: G.FC, fontWeight: 600, fontSize: 14 }} }} }} }},
    {{ name: 'Porto organizado', type: 'bar', stack: 'r', barMaxWidth: 24, data: RK.map(function (x) {{ return x.t === 'po' ? x.v : '-'; }}),
       itemStyle: {{ color: C.po, borderRadius: [0, 4, 4, 0] }},
       label: {{ show: true, position: 'right', distance: 8, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 16,
         formatter: function (p) {{ var x = RK[p.dataIndex]; return G.num(x.v, 1) + '  {{v|' + (x.var >= 0 ? '+' : '') + G.num(x.var, 1) + '%}}'; }},
         rich: {{ v: {{ color: C.apagado, fontFamily: G.FC, fontWeight: 600, fontSize: 14 }} }} }} }}
  ]
}});
var TM = {json.dumps(tm, ensure_ascii=False)};
G.desenha('g-merc', {{
  tooltip: G.dica({{ formatter: function (p) {{ var x = p.data;
    return '<b>' + x.name + '</b><br/>' + G.num(x.value, 1) + ' mi t &middot; ' + G.pct(x.sh) + ' do total'
      + (x.var !== null ? '<br/>' + (x.var >= 0 ? '+' : '') + G.num(x.var, 1) + '% sobre 2024' : ''); }} }}),
  series: [{{ type: 'treemap', left: 0, right: 0, top: 4, bottom: 0, roam: false, nodeClick: false, breadcrumb: {{ show: false }},
    sort: 'desc', squareRatio: 1.2,
    itemStyle: {{ borderColor: '#fff', borderWidth: 3, gapWidth: 3, borderRadius: 6 }},
    label: {{ show: true, position: 'insideTopLeft', padding: [10, 12], overflow: 'truncate', color: '#fff', fontFamily: G.FT,
      formatter: function (p) {{ var x = p.data; return '{{n|' + x.curto + '}}\\n{{v|' + G.num(x.value, 1) + ' mi t}}  {{s|' + G.pct(x.sh) + '}}'; }},
      rich: {{ n: {{ fontSize: 18, fontWeight: 700, color: '#fff', lineHeight: 26, fontFamily: G.FT }},
              v: {{ fontSize: 16, fontWeight: 600, color: '#DBEAFE', lineHeight: 22, fontFamily: G.FC }},
              s: {{ fontSize: 15, fontWeight: 700, color: '#FFD700', lineHeight: 22, fontFamily: G.FT }},
              n2: {{ fontSize: 13, fontWeight: 700, color: '#fff', lineHeight: 18, fontFamily: G.FT }},
              v2: {{ fontSize: 13, fontWeight: 600, color: '#DBEAFE', lineHeight: 18, fontFamily: G.FC }} }} }},
    upperLabel: {{ show: false }},
    data: TM.map(function (x) {{
      var o = Object.assign({{}}, x, {{ itemStyle: {{ color: x.name === 'Demais grupos' ? C.apagado : '#1D5FA8' }} }});
      if (x.value < 60) o.label = {{ padding: [8, 5], overflow: 'none', formatter: function (p) {{
        return '{{n2|' + p.data.curto + '}}\\n{{v2|' + G.num(p.data.value, 1) + '}}'; }} }};
      else if (x.value < 130) o.label = {{ formatter: function (p) {{ var y = p.data;
        return '{{n|' + y.curto + '}}\\n{{v|' + G.num(y.value, 1) + ' mi t}}\\n{{s|' + G.pct(y.sh) + '}}'; }} }};
      return o; }})
  }}]
}});
"""
    slide(6, 2, "Onde e o que se movimenta", "Portos brasileiros · Instalações e cargas", "Onde e o que se movimenta", f"""
  <div class="flex-1 px-16 pb-4 flex flex-col gap-5 min-h-0" style="justify-content:center;">
    <div class="grid grid-cols-2 gap-8">
      <div class="painel">
        <p class="ct">As 12 instalações que mais movimentaram em 2025</p>
        <p class="cd" style="margin:0;">Milhões de toneladas e variação sobre 2024</p>
        <div id="g-rank" class="graf" style="height:500px;"></div>
      </div>
      <div class="painel">
        <p class="ct">O que passou pelos portos em 2025</p>
        <p class="cd" style="margin:0;">Dez maiores grupos de mercadoria, em milhões de toneladas</p>
        <div id="g-merc" class="graf" style="height:466px; margin-top:10px;"></div>
        <p class="legenda" style="margin:8px 0 0;">Nos blocos menores, só o valor em mi t. "Adubos" = fertilizantes; "Aço" = ferro e aço.</p>
      </div>
    </div>
    <div class="grid grid-cols-3 gap-6" style="align-items:stretch;">
      {card("fa-mountain", "Um terminal maior que Santos", f"Ponta da Madeira (MA) movimentou <b>{br(pm['v'], 1)} mi t</b>, {br(acima, 0)}% a mais que todo o porto de Santos.")}
      {card("fa-gem", f"Minério de ferro é {br(minerio['sh'], 0)}% de tudo", f"<b>{br(minerio['value'], 1)} mi t</b> em 2025. Petróleo bruto vem a seguir, com {br(next(m for m in tm if m['name'] == 'Petróleo bruto')['sh'], 1)}%.")}
      {card("fa-wheat-awn", "Soja puxa a alta do agro", f"A soja cresceu <b>{br(soja['var'], 1)}%</b>, e milho e fertilizantes, cerca de 10% cada.", "card-gold")}
    </div>
    <p class="legenda">{FONTE}. O porto organizado soma todos os terminais públicos e arrendados dentro dele; o TUP é uma instalação só. "Contêineres" é a carga conteinerizada inteira, sem abrir o conteúdo.</p>
  </div>""", js_extra=graficos(js6))
