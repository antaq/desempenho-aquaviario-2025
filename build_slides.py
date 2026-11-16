#!/usr/bin/env python3
"""Gera os slides do deck Desempenho Aquaviário 2025 — Estatísticas da Fiscalização.

Mesma sequência do relatório anterior (250220 Apresentação SFC Estatístico Aquaviário.pptx),
com os números refeitos e três slides novos sobre os portos brasileiros:

  01 capa · 02 estrutura da SFC · 03 ambiente fiscalizado
  04 portos em números · 05 mapa dos portos e terminais · 06 cargas e instalações
  07 perfil das fiscalizações · 08 o ano de 2025 · 09 resultado · 10 encerramento

Fontes:
  - PIF (SFIS), captura de 23/09/2026: séries de fiscalização (quadros Fiscalizações
    Realizadas, Fiscalizações Realizadas por Área e detalhe por procedimento).
  - Universo Fiscalizado (PIF), 16/11/2026: serviços regulados por área, modalidade e unidade.
  - Estatístico Aquaviário da ANTAQ (dados públicos), via conector MCP independente:
    slides 04 a 06, a partir de dados/portos.json.

Todo o deck sai deste script, inclusive capa e encerramento. Para regerar: python3 build_slides.py
"""

import json
from pathlib import Path

DST = Path(__file__).resolve().parent
TOTAL = 10
RODAPE = "Desempenho Aquaviário 2025 · Estatísticas da Fiscalização · SFC — ANTAQ"
TITULO_DECK = "Desempenho Aquaviário 2025"

ECHARTS = '<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js"></script>'
LEAFLET_CSS = '<link href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" rel="stylesheet"/>'
LEAFLET_JS = '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>'

# Cores por área: as mesmas em todos os slides (validadas em conjunto, ver graficos.js).
BASE_CSS = """
:root { --porto:#0066CC; --mar:#eb6834; --int:#1baf7a; --com:#D97706; }
body { margin:0; padding:0; overflow:hidden; font-family:'Open Sans',sans-serif; }
.slide { width:100vw; height:100vh; position:relative; display:flex; flex-direction:column; overflow:hidden; background:#ffffff; }
.font-montserrat { font-family:'Montserrat',sans-serif; }
.text-brand { color:#003366; } .bg-brand { background-color:#003366; }
.text-accent { color:#0066CC; } .bg-accent { background-color:#0066CC; }
.header-bar { height:10px; background:#003366; width:100%; }
.secondary-bar { height:4px; background:#0066CC; width:100%; }
.stat-card { background:linear-gradient(135deg,#003366,#004d99); border-radius:16px; padding:18px 16px; text-align:center; color:white; position:relative; overflow:hidden; }
.stat-num { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(46px * var(--tz)); line-height:1; margin:0; }
.stat-lbl { font-size:calc(16px * var(--tz)); line-height:1.3; color:#BFD3E8; margin:6px 0 0; }
.card { display:flex; align-items:flex-start; gap:16px; padding:14px 20px; background:#F8FAFC; border-radius:14px; border-left:5px solid #0066CC; }
.card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); border-left-color:#22C55E; }
.card-amber { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border-left-color:#F59E0B; }
.card-red   { background:linear-gradient(135deg,#FEF2F2,#FEE2E2); border-left-color:#EF4444; }
.card-gold  { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border-left-color:#FFD700; }
.ico { width:50px; height:50px; border-radius:12px; flex-shrink:0; display:flex; align-items:center; justify-content:center; background:#DBEAFE; }
.ico i { color:#0066CC; font-size:calc(22px * var(--tz)); }
.card-amber .ico { background:#FDE68A; } .card-amber .ico i { color:#B45309; }
.ct { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(21px * var(--tz)); line-height:1.25; margin:0; }
.cd { color:#475569; font-size:calc(17px * var(--tz)); line-height:1.45; margin:3px 0 0; }
.cd b, .cd strong { color:#003366; }
.pill { display:inline-block; padding:3px 12px; border-radius:999px; font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(14px * var(--tz)); letter-spacing:0.04em; }
.pill-a { background:#DCFCE7; color:#166534; } .pill-b { background:#DBEAFE; color:#1E40AF; }
.pill-c { background:#FEE2E2; color:#991B1B; } .pill-gold { background:#FEF3C7; color:#92400E; }
.destaque { background:linear-gradient(135deg,#003366,#0066CC); color:#fff; border-radius:16px; padding:18px 26px; }
.destaque p { margin:0; }
.legenda { color:#64748B; font-size:calc(14px * var(--tz)); line-height:1.5; margin:0; }
.sec { font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(15px * var(--tz)); letter-spacing:.12em; text-transform:uppercase; color:#64748B; margin:0; }
.hdr .text-5xl { font-size:46px; line-height:1; } .hdr .text-lg { font-size:19px; line-height:1.5; } .ftr .text-sm { font-size:14px; line-height:1.4; }
.gap-3 { row-gap:22px; } .gap-4 { row-gap:24px; } .gap-5 { row-gap:26px; } .gap-6 { row-gap:28px; }
/* painel de gráfico */
.painel { background:#fff; border:1px solid #E2E8F0; border-radius:16px; padding:16px 22px 8px; box-shadow:0 1px 3px rgba(15,23,42,.05); }
.painel .ct { margin-bottom:2px; }
.graf { width:100%; }
/* barra segmentada alta (uma soma, dividida em partes) */
.segbar { display:flex; gap:3px; height:46px; width:100%; }
.segbar .seg { border-radius:6px; display:flex; align-items:center; padding:0 14px; color:#fff; font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(18px * var(--tz)); white-space:nowrap; min-width:0; }
.sw { display:inline-block; width:14px; height:14px; border-radius:4px; vertical-align:-1px; margin-right:7px; }
.chaves { display:flex; flex-wrap:wrap; gap:6px 22px; color:#475569; font-family:'Montserrat',sans-serif; font-weight:600; font-size:calc(15px * var(--tz)); }
.num-r { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(30px * var(--tz)); line-height:1; margin:0; }
"""

HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
{head_extra}
<style>{css}</style>
</head>
<body>
<div class="slide">
  <div class="header-bar"></div>
  <div class="secondary-bar"></div>

  <div class="px-16 pt-6 pb-2 hdr">
    <div class="flex items-center gap-3">
      <div style="width:5px;height:44px;" class="bg-accent"></div>
      <div>
        <p class="font-montserrat font-bold text-gray-400 text-lg uppercase tracking-widest">{kicker}</p>
        <p class="text-5xl font-montserrat font-bold text-brand uppercase tracking-tight">{titulo}</p>
      </div>
      <div class="ml-auto flex items-center gap-3">
        <span class="font-montserrat font-bold text-accent uppercase tracking-widest" style="font-size:15px;"><i class="fas {tagico}"></i>&nbsp; {tag}</span>
        <img src="assets/logo-antaq-azul.png" alt="ANTAQ" style="height:32px;">
        <p class="font-montserrat font-bold text-gray-400 tracking-wider" style="font-size:12px; line-height:1.35;">SFC<br/>GPF</p>
      </div>
    </div>
  </div>

{body}

  <div class="px-16 pb-4 flex justify-between items-center border-t border-gray-100 pt-3 mx-8 ftr">
    <p class="text-gray-400 text-sm">{rodape}</p>
    <p class="text-gray-300 text-sm font-mono">{n} / {total}</p>
  </div>
</div>
<script src="zoom.js"></script>
<script src="anim.js"></script>
{js_extra}
<script>document.addEventListener("keydown",function(e){{if(["ArrowRight","ArrowLeft","PageDown","PageUp","Home","End"," ","f","F"].indexOf(e.key)!==-1){{e.preventDefault();window.parent.postMessage({{type:"slide-nav",key:e.key}},"*");}}}});</script>
</body>
</html>
"""

MODULOS = {
    1: ("SFC", "fa-sitemap"),
    2: ("Setor portuário", "fa-anchor"),
    3: ("Fiscalização", "fa-magnifying-glass-chart"),
}

SLIDES = []
BASES = {2: 1.3, 3: 1.3, 4: 1.2, 5: 1.0, 6: 1.1, 7: 1.15, 8: 1.1, 9: 1.15}


def slide(n, mod, title, kicker, titulo, body, extra_css="", base=1.0, head_extra="", js_extra=""):
    SLIDES.append(dict(n=n, mod=mod, title=title, kicker=kicker, titulo=titulo, body=body,
                       extra_css=extra_css, base=BASES.get(n, base), head_extra=head_extra, js_extra=js_extra))


def card(icon, titulo, texto, cls=""):
    return (f'<div class="card {cls}"><div class="ico"><i class="fas {icon}"></i></div>'
            f'<div><p class="ct">{titulo}</p><p class="cd">{texto}</p></div></div>')


def stat(num, rotulo):
    return f'<div class="stat-card"><p class="stat-num">{num}</p><p class="stat-lbl">{rotulo}</p></div>'


def br(v, d=0):
    """Número no padrão brasileiro: 1.234 ou 12,3."""
    s = f"{v:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def segbar(partes, altura=46):
    """Barra segmentada alta: partes = [(rótulo dentro, valor, cor)]. Larguras proporcionais."""
    tot = sum(v for _, v, _ in partes)
    segs = "".join(
        f'<div class="seg" style="width:{100 * v / tot:.2f}%; background:{c};" title="{r}">{r}</div>'
        for r, v, c in partes)
    return f'<div class="bar-row"><div class="bar-trk segbar" style="height:{altura}px;">{segs}</div></div>'


def chaves(itens):
    return '<div class="chaves">' + "".join(
        f'<span><span class="sw" style="background:{c};"></span>{t}</span>' for t, c in itens) + '</div>'


def graficos(js):
    return ECHARTS + '\n<script src="graficos.js"></script>\n<script>\n(function(){ var C = G.C;\n' + js + '\n})();\n</script>'


AREAS = [("Porto", "var(--porto)"), ("Marítima", "var(--mar)"), ("Interior", "var(--int)")]


# ---------------------------------------------------------------------------
# 02 — Estrutura da SFC
# ---------------------------------------------------------------------------
# Serviços regulados na jurisdição de cada gerência (a própria GRE mais as unidades
# subordinadas), por área. Universo Fiscalizado (PIF), 16/11/2026. 38 serviços sem
# unidade atribuída ficam fora; total com unidade = 2.451.
GRES = [
    ("GREBL", "Belém", "Norte", "URESL São Luís · URESN Santana · DREST Santarém", (366, 76, 243)),
    ("GREMN", "Manaus", "Norte", "UREPV Porto Velho", (194, 30, 308)),
    ("GRERJ", "Rio de Janeiro", "Sudeste", "UREVT Vitória", (147, 240, 1)),
    ("GRERE", "Recife", "Nordeste", "URESV Salvador · UREFT Fortaleza", (166, 102, 50)),
    ("GREFL", "Florianópolis", "Sul", "URECB Curitiba · UREPL Porto Alegre", (190, 73, 41)),
    ("GREST", "Santos", "Sudeste", "sem unidade subordinada", (137, 64, 23)),
]
assert sum(sum(a) for *_, a in GRES) == 2451
MAX_GRE = max(sum(a) for *_, a in GRES)


def gre_card(sig, cid, reg, ures, areas):
    tot = sum(areas)
    segs = "".join(
        f'<div class="seg" style="flex:{v} 0 0; background:{c}; height:100%; border-radius:4px;" title="{nome}: {br(v)}"></div>'
        for (nome, c), v in zip(AREAS, areas) if v > 0)
    return f"""
        <div class="card" style="flex-direction:column; align-items:stretch; gap:8px; padding:14px 20px 16px;">
          <div class="flex items-center justify-between"><p class="ct">{sig} · {cid}</p><span class="pill pill-b">{reg}</span></div>
          <p class="cd" style="margin:0;">{ures}</p>
          <div class="flex items-center gap-4" style="margin-top:4px;">
            <div style="flex:1;"><div class="bar-row"><div class="bar-trk" style="display:flex; gap:3px; height:16px; width:{100 * tot / MAX_GRE:.1f}%;">{segs}</div></div></div>
            <p class="num-r" style="font-size:calc(26px * var(--tz)); min-width:64px; text-align:right;">{br(tot)}</p>
          </div>
        </div>"""


gres_html = "\n".join(gre_card(*g) for g in GRES)
slide(2, 1, "Estrutura da SFC", "SFC · Gerências e Unidades Regionais", "Estrutura da SFC", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-8 items-center min-h-0">
    <div class="col-span-4 flex flex-col gap-4">
      <div class="destaque text-center">
        <p class="font-montserrat font-black" style="font-size:calc(38px * var(--tz));">SFC</p>
        <p style="font-size:calc(17px * var(--tz)); color:#DBEAFE;">Superintendência de Fiscalização e Coordenação das Unidades Regionais</p>
      </div>
      <div class="grid grid-cols-3 gap-4">
        {stat("6", "Gerências Regionais")}{stat("8", "Unidades Regionais")}{stat("1", "Divisão Regional")}
      </div>
      {card("fa-building-columns", "Na sede, em Brasília", "<b>GPF</b> planeja e cuida da inteligência, <b>GCOR</b> coordena as regionais e <b>GRAT</b> responde por recursos e apoio técnico.")}
      {card("fa-compass", "O Norte concentra a carga", "GREBL e GREMN respondem por <b>1.217</b> dos 2.451 serviços regulados com unidade definida: quase a metade.", "card-gold")}
    </div>
    <div class="col-span-8 flex flex-col gap-4">
      <div class="flex items-end justify-between">
        <p class="sec">Serviços regulados por gerência e área</p>
        {chaves(AREAS)}
      </div>
      <div class="grid grid-cols-2 gap-4">
{gres_html}
      </div>
      <p class="legenda">Fontes: Regimento Interno da ANTAQ, art. 83 (estrutura); Universo Fiscalizado (PIF), 16/11/2026 (serviços regulados). A jurisdição soma a gerência e as unidades subordinadas; 38 serviços sem unidade atribuída ficam fora.</p>
    </div>
  </div>""")


# ---------------------------------------------------------------------------
# 03 — Ambiente fiscalizado
# ---------------------------------------------------------------------------
MAX_FOLHA = 394


def folha(rotulo, v, cor):
    return (f'<div class="flex items-center gap-3" style="min-height:30px;">'
            f'<p class="cd" style="margin:0; width:52%; line-height:1.25;">{rotulo}</p>'
            f'<div style="flex:1;"><div class="bar-row"><div class="bar-trk" style="height:12px; width:{max(100 * v / MAX_FOLHA, 1.2):.1f}%;">'
            f'<div class="seg" style="width:100%; height:100%; background:{cor}; border-radius:0 4px 4px 0;"></div></div></div></div>'
            f'<p class="font-montserrat font-bold text-brand" style="margin:0; min-width:48px; text-align:right; font-size:calc(18px * var(--tz));">{br(v)}</p></div>')


def grupo(nome, v):
    return (f'<p class="sec" style="margin-top:6px; color:#334155;">{nome} · {br(v)}</p>')


def ramo(icone, nome, tot, cor, miolo, nota=""):
    nota_html = f'<p class="legenda" style="margin-top:4px;">{nota}</p>' if nota else ""
    return f"""
      <div class="card" style="flex-direction:column; align-items:stretch; gap:6px; border-left-color:{cor}; padding:16px 22px; flex:1;">
        <div class="flex items-center justify-between" style="margin-bottom:4px;">
          <p class="ct" style="font-size:calc(23px * var(--tz));"><i class="fas {icone}" style="color:#0066CC;"></i>&nbsp; {nome}</p>
          <p class="num-r">{br(tot)}</p>
        </div>
        {miolo}
        {nota_html}
      </div>"""


P, M, I = "var(--porto)", "var(--mar)", "var(--int)"
# Área portuária em duas colunas internas, como na árvore do relatório anterior:
# terminais públicos e operadores de um lado, terminais privados do outro.
port_esq = "\n".join([
    grupo("Portos organizados", 35), folha("Porto organizado", 35, P),
    grupo("Terminais nos portos", 167), folha("Arrendamento", 158, P), folha("Uso temporário (CUT)", 5, P), folha("Contrato de transição", 4, P),
    grupo("Operadores portuários", 332), folha("Operador portuário", 332, P),
])
port_dir = "\n".join([
    grupo("Terminais privados", 666), folha("Registro (IPR)", 379, P), folha("Uso privado (TUP)", 236, P),
    folha("Transbordo (ETC)", 45, P), folha("Turismo (IPT)", 6, P),
])
portuaria = (f'<div class="grid grid-cols-2 gap-8" style="row-gap:0;"><div class="flex flex-col" style="gap:4px;">{port_esq}</div>'
             f'<div class="flex flex-col" style="gap:4px;">{port_dir}</div></div>')
maritima = "\n".join([
    folha("Apoio portuário", 394, M), folha("Apoio marítimo", 72, M), folha("Apoio marítimo e portuário", 68, M),
    folha("Cabotagem", 20, M), folha("Cabotagem e outras navegações", 31, M),
])
interior = "\n".join([
    folha("Travessia", 301, I), folha("Longitudinal de carga", 264, I),
    folha("Longitudinal misto", 98, I), folha("Longitudinal de passageiros", 41, I),
])
slide(3, 1, "Ambiente fiscalizado", "Universo Fiscalizado · 16/11/2026", "Ambiente fiscalizado", f"""
  <div class="flex-1 px-16 pb-4 flex flex-col gap-5 min-h-0" style="justify-content:center;">
    <div class="grid grid-cols-12 gap-8 items-center">
      <div class="col-span-4 destaque flex items-center gap-5">
        <p class="font-montserrat font-black" style="font-size:calc(58px * var(--tz)); line-height:1;">2.489</p>
        <p style="font-size:calc(18px * var(--tz)); color:#DBEAFE; line-height:1.35;">serviços regulados,<br/>de <b style="color:#FFD700;">2.136 empresas</b></p>
      </div>
      <div class="col-span-8 flex flex-col gap-3">
        <div class="flex items-end justify-between"><p class="sec">Divisão por área</p>{chaves([("Área portuária", P), ("Navegação marítima", M), ("Navegação interior", I)])}</div>
        {segbar([("48,2% · 1.200", 1200, P), ("23,5% · 585", 585, M), ("28,3% · 704", 704, I)])}
      </div>
    </div>
    <div class="grid grid-cols-12 gap-6" style="align-items:stretch;">
      <div class="col-span-7 flex flex-col">
{ramo("fa-anchor", "Área portuária", 1200, P, portuaria, "Outros 87 operadores também têm arrendamento ou contrato e estão contados nessas linhas. Uma empresa pode ter mais de um serviço.")}
      </div>
      <div class="col-span-5 flex flex-col gap-5">
{ramo("fa-ship", "Navegação marítima", 585, M, maritima, "Das 31 combinações com cabotagem, 15 incluem longo curso.")}
{ramo("fa-water", "Navegação interior", 704, I, interior, "")}
      </div>
    </div>
    <p class="legenda">Fonte: Universo Fiscalizado (PIF), contagem de serviços por área e modalidade em 16/11/2026. Barras na mesma escala nas três áreas. Embarcações em construção não aparecem como modalidade no Universo Fiscalizado.</p>
  </div>""")


# ---------------------------------------------------------------------------
# 04–06 — Portos brasileiros (dados/portos.json, Estatístico Aquaviário)
# ---------------------------------------------------------------------------
PORTOS = DST / "dados" / "portos.json"
if PORTOS.exists():
    import slides_portos  # noqa: E402  (gera os slides 4, 5 e 6 a partir do JSON)
    slides_portos.gerar(slide, dict(card=card, stat=stat, br=br, segbar=segbar, chaves=chaves,
                                    graficos=graficos, ECHARTS=ECHARTS, LEAFLET_CSS=LEAFLET_CSS,
                                    LEAFLET_JS=LEAFLET_JS), json.loads(PORTOS.read_text(encoding="utf-8")))


# ---------------------------------------------------------------------------
# 07 — Perfil das fiscalizações
# ---------------------------------------------------------------------------
# PIF, captura de 23/09/2026. Série oficial (quadro Fiscalizações Realizadas, sem canceladas)
# e quadro Fiscalizações Realizadas por Área. 2026 fica fora das séries por ser parcial.
ANOS_TIPO = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]
PAF = [852, 838, 871, 792, 704, 537, 508]
EXT = [599, 462, 525, 602, 470, 775, 671]
ANOS_AREA = ["2021", "2022", "2023", "2024", "2025"]
A_PORTO = [686, 741, 649, 722, 645]
A_MAR = [316, 299, 213, 354, 407]
A_INT = [394, 354, 312, 240, 135]

js7 = f"""
function linha(nome, cor, dados) {{
  return {{ name: nome, type: 'line', data: dados, symbol: 'circle', symbolSize: 12, smooth: false,
    lineStyle: {{ width: 3, color: cor }}, itemStyle: {{ color: cor, borderColor: '#fff', borderWidth: 2 }},
    endLabel: {{ show: true, distance: 12, formatter: function (p) {{ return nome + '  ' + G.num(p.value); }},
      color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 18 }},
    emphasis: {{ focus: 'series' }} }};
}}
G.desenha('g-area', {{
  grid: {{ left: 60, right: 170, top: 54, bottom: 36 }},
  legend: G.legenda({{ data: ['Porto', 'Marítima', 'Interior'] }}),
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'line', lineStyle: {{ color: '#94A3B8' }} }}, valueFormatter: function (v) {{ return G.num(v); }} }}),
  xAxis: G.eixoCat({json.dumps(ANOS_AREA)}, {{ boundaryGap: false }}),
  yAxis: G.eixoVal({{ min: 0, max: 800 }}),
  series: [linha('Porto', C.porto, {A_PORTO}), linha('Marítima', C.maritima, {A_MAR}), linha('Interior', C.interior, {A_INT})]
}});
function coluna(nome, cor, dados) {{
  var ult = dados.length - 1;
  return {{ name: nome, type: 'bar', data: dados, barMaxWidth: 30, barGap: '10%',
    itemStyle: {{ color: cor, borderRadius: [4, 4, 0, 0] }},
    label: {{ show: true, position: 'top', distance: 6, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 17,
      formatter: function (p) {{ return (p.dataIndex === 0 || p.dataIndex === ult) ? G.num(p.value) : ''; }} }},
    emphasis: {{ focus: 'series' }} }};
}}
G.desenha('g-tipo', {{
  grid: {{ left: 60, right: 16, top: 54, bottom: 36 }},
  legend: G.legenda({{ data: ['PAF (programadas)', 'Extraordinárias'] }}),
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'shadow', shadowStyle: {{ color: 'rgba(148,163,184,.14)' }} }}, valueFormatter: function (v) {{ return G.num(v); }} }}),
  xAxis: G.eixoCat({json.dumps(ANOS_TIPO)}),
  yAxis: G.eixoVal({{ min: 0, max: 1000, interval: 250 }}),
  series: [coluna('PAF (programadas)', C.paf, {PAF}), coluna('Extraordinárias', C.ext, {EXT})]
}});
"""
slide(7, 3, "Perfil das fiscalizações", "Fiscalização · Série histórica", "Perfil das fiscalizações", f"""
  <div class="flex-1 px-16 pb-4 flex flex-col gap-5 min-h-0" style="justify-content:center;">
    <div class="grid grid-cols-2 gap-8">
      <div class="painel">
        <p class="ct">Fiscalizações por área, 2021–2025</p>
        <p class="cd" style="margin:0;">Porto, navegação marítima e navegação interior</p>
        <div id="g-area" class="graf" style="height:530px;"></div>
      </div>
      <div class="painel">
        <p class="ct">PAF e extraordinárias, 2019–2025</p>
        <p class="cd" style="margin:0;">Fiscalizações programadas no Plano Anual e fiscalizações extraordinárias</p>
        <div id="g-tipo" class="graf" style="height:530px;"></div>
      </div>
    </div>
    <div class="grid grid-cols-3 gap-6" style="align-items:stretch;">
      {card("fa-anchor", "Porto segue com mais da metade", "A área portuária teve <b>54%</b> das fiscalizações de 2025: 645 de 1.187.")}
      {card("fa-arrow-trend-up", "Marítima sobe, interior cai", "A marítima foi de <b>213</b> (2023) para <b>407</b> (2025); a interior, de 394 (2021) para <b>135</b>.")}
      {card("fa-right-left", "Extraordinárias passam o PAF", "Desde 2024 as extraordinárias superam as programadas: <b>671</b> contra <b>508</b> em 2025.", "card-gold")}
    </div>
    <p class="legenda">Fonte: PIF (SFIS), quadros Fiscalizações Realizadas e Fiscalizações Realizadas por Área, captura de 23/09/2026. Os dois quadros contam de modo um pouco diferente (1.179 e 1.187 em 2025). 2026 fica fora por ser parcial.</p>
  </div>""", head_extra="", js_extra=graficos(js7))


# ---------------------------------------------------------------------------
# 08 — O ano de 2025 em números
# ---------------------------------------------------------------------------
# Quem executou: quadro de detalhe por procedimento, soma da medida Fiscalizações, 2025.
# Sede = GEF Investimentos (182 PAF) + GEF Contêineres (153 extr.) + SFC (68 extr.) + GRAT (1 extr.).
EXEC = [("Sede · SFC, GRAT e GEFs", 182, 222), ("GREMN · Manaus", 56, 89), ("GREFL · Florianópolis", 42, 100),
        ("GREBL · Belém", 69, 72), ("GRERJ · Rio de Janeiro", 74, 58), ("GREST · Santos", 37, 92), ("GRERE · Recife", 62, 66)]
assert sum(p for _, p, _ in EXEC) == 522 and sum(e for *_, e in EXEC) == 699
js8 = f"""
var cats = {json.dumps([e[0] for e in EXEC], ensure_ascii=False)};
var paf = {[e[1] for e in EXEC]}, ext = {[e[2] for e in EXEC]};
G.desenha('g-exec', {{
  grid: {{ left: 250, right: 70, top: 46, bottom: 10 }},
  legend: G.legenda({{ data: ['PAF (programadas)', 'Extraordinárias'] }}),
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'shadow', shadowStyle: {{ color: 'rgba(148,163,184,.14)' }} }},
    formatter: function (ps) {{ var t = 0; var l = ps.map(function (p) {{ t += p.value; return p.marker + p.seriesName + ': <b>' + G.num(p.value) + '</b>'; }});
      return '<b>' + ps[0].name + '</b><br/>' + l.join('<br/>') + '<br/>Total: <b>' + G.num(t) + '</b>'; }} }}),
  xAxis: G.eixoVal({{ show: false, max: 420 }}),
  yAxis: G.eixoCat(cats, {{ inverse: true, axisLine: {{ show: false }}, axisLabel: {{ color: C.tinta2, fontFamily: G.FT, fontSize: 17, fontWeight: 600, margin: 16 }} }}),
  series: [
    {{ name: 'PAF (programadas)', type: 'bar', stack: 't', data: paf, barMaxWidth: 26,
       itemStyle: {{ color: C.paf, borderColor: '#fff', borderWidth: 2, borderRadius: [4, 0, 0, 4] }} }},
    {{ name: 'Extraordinárias', type: 'bar', stack: 't', data: ext, barMaxWidth: 26,
       itemStyle: {{ color: C.ext, borderColor: '#fff', borderWidth: 2, borderRadius: [0, 4, 4, 0] }},
       label: {{ show: true, position: 'right', distance: 10, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 18,
         formatter: function (p) {{ return G.num(paf[p.dataIndex] + ext[p.dataIndex]); }} }} }}
  ]
}});
"""
slide(8, 3, "O ano de 2025 em números", "Fiscalização · 2025 e 2026", "O ano de 2025 em números", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-8 items-center min-h-0">
    <div class="col-span-5 flex flex-col gap-4">
      <p class="sec">2025 · PAF e extraordinárias</p>
      <div class="grid grid-cols-3 gap-4">{stat("1.179", "fiscalizações no ano")}{stat("508", "do PAF")}{stat("671", "extraordinárias")}</div>
      <div class="flex items-end justify-between" style="margin-top:8px;"><p class="sec">Por área · quadro próprio, 1.187</p>{chaves(AREAS)}</div>
      {segbar([("54,3% · 645", 645, P), ("34,3% · 407", 407, M), ("11,4%", 135, I)])}
      {card("fa-triangle-exclamation", "Rotina: 538 registros, contra 2.421 em 2024", "A queda aparece em todas as unidades e sugere mudança na forma de registrar a rotina. Vale confirmar antes de comparar os anos.", "card-amber")}
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(21px * var(--tz));">2026, até 23 de setembro</p>
        <p style="font-size:calc(17px * var(--tz)); color:#DBEAFE; margin-top:6px !important; line-height:1.5;"><b style="color:#FFD700;">501</b> fiscalizações do PAF, <b style="color:#FFD700;">79,9%</b> das 627 planejadas para o ano · <b style="color:#FFD700;">196</b> extraordinárias · <b style="color:#FFD700;">889</b> registradas pelo aplicativo SFIS Mobile.</p>
      </div>
    </div>
    <div class="col-span-7 flex flex-col gap-4">
      <div class="painel">
        <p class="ct">Quem executou em 2025</p>
        <p class="cd" style="margin:0;">PAF e extraordinárias por gerência regional e pela sede</p>
        <div id="g-exec" class="graf" style="height:520px;"></div>
      </div>
      {card("fa-users-gear", "A sede fez um terço", "GEF Investimentos, GEF Contêineres e a própria SFC responderam por <b>404</b> das 1.221 fiscalizações do quadro de detalhe. As seis gerências regionais, por <b>817</b>.")}
      <p class="legenda">Fonte: PIF (SFIS), captura de 23/09/2026. Totais do ano: quadro Fiscalizações Realizadas (série oficial). Por unidade: quadro de detalhe por procedimento, que soma 1.221 em 2025 por critério de contagem diferente. Cada gerência inclui suas unidades subordinadas.</p>
    </div>
  </div>""", js_extra=graficos(js8))


# ---------------------------------------------------------------------------
# 09 — O que as fiscalizações encontram
# ---------------------------------------------------------------------------
# Fiscalizações PAF + extraordinárias com irregularidade constatada > 0 ÷ total (quadro de detalhe).
IRR = [(2019, 444, 1463), (2020, 388, 1344), (2021, 431, 1420), (2022, 363, 1420),
       (2023, 273, 1193), (2024, 329, 1338), (2025, 245, 1221)]
PCT = [round(100 * c / t, 1) for _, c, t in IRR]
assert PCT == [30.3, 28.9, 30.4, 25.6, 22.9, 24.6, 20.1], PCT
js9 = f"""
var anos = {json.dumps([str(a) for a, *_ in IRR])}, v = {PCT}, ult = v.length - 1;
G.desenha('g-irr', {{
  grid: {{ left: 64, right: 40, top: 30, bottom: 36 }},
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'line', lineStyle: {{ color: '#94A3B8' }} }},
    formatter: function (ps) {{ var i = ps[0].dataIndex, d = {json.dumps([[c, t] for _, c, t in IRR])}[i];
      return '<b>' + ps[0].name + '</b><br/>' + G.pct(ps[0].value) + ' com irregularidade<br/>' + G.num(d[0]) + ' de ' + G.num(d[1]) + ' fiscalizações'; }} }}),
  xAxis: G.eixoCat(anos, {{ boundaryGap: false }}),
  yAxis: G.eixoVal({{ min: 0, max: 35, interval: 10, axisLabel: {{ color: C.apagado, fontFamily: G.FC, fontSize: 16, formatter: function (x) {{ return x + '%'; }} }} }}),
  series: [{{ type: 'line', data: v, symbol: 'circle', symbolSize: 12,
    lineStyle: {{ width: 3, color: '#D97706' }}, itemStyle: {{ color: '#D97706', borderColor: '#fff', borderWidth: 2 }},
    areaStyle: {{ color: 'rgba(217,119,6,.10)' }},
    label: {{ show: true, position: 'top', distance: 10, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 19,
      formatter: function (p) {{ return (p.dataIndex === 0 || p.dataIndex === ult) ? G.pct(p.value) : ''; }} }} }}]
}});
"""
slide(9, 3, "O que as fiscalizações encontram", "Fiscalização · Resultado", "O que as fiscalizações encontram", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-8 items-center min-h-0">
    <div class="col-span-5 flex flex-col gap-4">
      <div class="destaque flex items-center gap-6" style="padding:22px 28px;">
        <p class="font-montserrat font-black" style="font-size:calc(84px * var(--tz)); line-height:1; color:#FFD700;">79,9%</p>
        <p style="font-size:calc(20px * var(--tz)); color:#DBEAFE; line-height:1.4;">das fiscalizações de 2025 terminaram <b style="color:#fff;">sem irregularidade constatada</b></p>
      </div>
      <div class="flex items-end justify-between" style="margin-top:6px;"><p class="sec">1.221 em 2025</p>{chaves([("Sem irregularidade", "#0066CC"), ("Com irregularidade", "var(--com)")])}</div>
      {segbar([("976 sem irregularidade", 976, "#0066CC"), ("245", 245, "var(--com)")])}
      <div class="grid grid-cols-2 gap-4" style="align-items:stretch;">
        <div class="card" style="flex-direction:column; gap:4px;"><p class="sec">PAF</p><p class="num-r" style="font-size:calc(40px * var(--tz));">12,6%</p><p class="cd">com irregularidade: 66 de 522</p></div>
        <div class="card card-amber" style="flex-direction:column; gap:4px;"><p class="sec">Extraordinárias</p><p class="num-r" style="font-size:calc(40px * var(--tz));">25,6%</p><p class="cd">com irregularidade: 179 de 699</p></div>
      </div>
      <p class="legenda">A extraordinária costuma nascer de denúncia ou de demanda externa, e encontra irregularidade duas vezes mais que a programada.</p>
    </div>
    <div class="col-span-7 flex flex-col gap-4">
      <div class="painel">
        <p class="ct">Parcela com irregularidade constatada, 2019–2025</p>
        <p class="cd" style="margin:0;">Fiscalizações PAF e extraordinárias com ao menos uma irregularidade, sobre o total do ano</p>
        <div id="g-irr" class="graf" style="height:440px;"></div>
      </div>
      <div class="grid grid-cols-2 gap-4" style="align-items:stretch;">
        {card("fa-chart-line", "Um terço a menos", "De <b>30,4%</b> em 2021 para <b>20,1%</b> em 2025. Em 2026, até setembro, o índice está em 16,0%.")}
        {card("fa-scale-unbalanced", "Leitura com cautela", "A queda pode vir de mais conformidade ou de mudança no foco das ações. O indicador sozinho não separa os dois efeitos.", "card-amber")}
      </div>
      <p class="legenda">Fonte: PIF (SFIS), quadro de detalhe por procedimento, captura de 23/09/2026. Este indicador substitui o índice de permanência de irregularidades do relatório de 2024, que os quadros atuais do PIF não permitem reproduzir.</p>
    </div>
  </div>""", js_extra=graficos(js9))


# ---------------------------------------------------------------------------
# 01 — Capa e 10 — Encerramento
# ---------------------------------------------------------------------------
ESCURO_CSS = """
body { margin:0; padding:0; overflow:hidden; font-family:'Open Sans',sans-serif; }
.slide { width:100vw; height:100vh; position:relative; display:flex; flex-direction:column; overflow:hidden; background: linear-gradient(135deg, #001a33 0%, #003366 45%, #004d99 100%); }
.font-montserrat { font-family:'Montserrat',sans-serif; }
.gold { color:#FFD700; } .bg-gold { background-color:#FFD700; }
.shape-circle { position:absolute; bottom:-140px; left:-140px; width:520px; height:520px; border-radius:50%; border:2px solid rgba(255,215,0,0.07); }
.shape-circle2 { position:absolute; top:-120px; right:-120px; width:420px; height:420px; border-radius:50%; border:2px solid rgba(255,215,0,0.06); }
.shape-right { position:absolute; top:0; right:0; width:40%; height:100%; background:linear-gradient(135deg, rgba(0,102,204,0.3) 0%, rgba(0,51,102,0.6) 100%); clip-path:polygon(30% 0, 100% 0, 100% 100%, 0% 100%); }
.recado { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:16px; padding:16px 22px; display:flex; gap:16px; align-items:flex-start; }
.recado i { color:#FFD700; font-size:calc(22px * var(--tz)); margin-top:3px; width:28px; text-align:center; }
.recado p { margin:0; }
.recado-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#fff; font-size:calc(19px * var(--tz)); }
.recado-d { color:#BFD3E8; font-size:calc(16px * var(--tz)); line-height:1.5; margin-top:3px !important; }
.gap-4 { row-gap:24px; }
"""

ESCURO_HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
<style>
:root {{ --tz-base: {base}; }}
{css}
</style>
</head>
"""
NAV = '<script>document.addEventListener("keydown",function(e){if(["ArrowRight","ArrowLeft","PageDown","PageUp","Home","End"," ","f","F"].indexOf(e.key)!==-1){e.preventDefault();window.parent.postMessage({type:"slide-nav",key:e.key},"*");}});</script>'


def chip(ic, rot, val):
    return f"""      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-full flex items-center justify-center" style="background:rgba(255,215,0,0.15);"><i class="fas {ic} gold text-lg"></i></div>
        <div><p class="text-gray-400 text-sm uppercase tracking-wider font-semibold">{rot}</p><p class="text-white font-semibold text-lg">{val}</p></div>
      </div>"""


CAPA = ESCURO_HEAD.format(title=f"Abertura — {TITULO_DECK}", base="1.15", css=ESCURO_CSS) + f"""<body>
<div class="slide">
  <div class="shape-right"></div>
  <div style="height:6px; background:#FFD700; width:100%;"></div>
  <div class="relative z-10 flex flex-col justify-center flex-1 pl-24 pr-16">
    <div class="absolute top-16 left-24 flex items-center gap-3">
      <div class="bg-gold" style="width:40px;height:3px;"></div>
      <p class="text-gray-400 text-lg font-montserrat font-medium tracking-widest uppercase">SFC · Estatísticas da Fiscalização</p>
    </div>
    <div class="mt-4">
      <p class="font-montserrat font-black text-white leading-none" style="font-size:calc(76px * var(--tz));">Desempenho</p>
      <p class="font-montserrat font-black gold leading-none mt-2" style="font-size:calc(92px * var(--tz));">Aquaviário 2025</p>
      <div class="bg-gold mt-6 mb-8" style="width:100px; height:4px;"></div>
      <p class="text-2xl text-gray-300 font-light leading-relaxed max-w-3xl">Estatísticas da fiscalização no ano de 2025<br/>e um panorama dos portos brasileiros</p>
    </div>
    <div class="flex gap-10 mt-12">
{chip("fa-database", "Fiscalização", "PIF (SFIS) até 23/09/2026")}
{chip("fa-ship", "Portos", "Estatístico Aquaviário da ANTAQ")}
{chip("fa-rotate", "Atualização", "16 de novembro de 2026")}
    </div>
  </div>
  <div class="relative z-10 px-24 pb-10 flex justify-between items-end border-t border-gray-700 pt-6 mx-8">
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-2 text-gray-400 text-sm"><i class="fas fa-sitemap"></i><span>SFC · Superintendência de Fiscalização e Coordenação das Unidades Regionais</span></div>
      <div class="flex items-center gap-2 text-gray-400 text-sm"><i class="fas fa-globe"></i><span>www.gov.br/antaq</span></div>
    </div>
    <p class="text-gray-500 text-sm font-montserrat font-bold tracking-wider">1 / {TOTAL}</p>
  </div>
  <div class="absolute top-1/2 right-12 transform -translate-y-1/2 opacity-5" style="z-index:0;"><img src="assets/logo-antaq-branca-vertical.png" alt="" style="height:400px;"></div>
</div>
<script src="zoom.js"></script>
{NAV}
</body>
</html>
"""

RECADOS = [
    ("fa-sitemap", "Ambiente fiscalizado", "<strong style='color:#FFD700;'>2.489 serviços</strong> de 2.136 empresas, quase metade na área portuária."),
    ("fa-anchor", "Portos", "{recado_portos}"),
    ("fa-magnifying-glass-chart", "Fiscalização", "<strong style='color:#FFD700;'>1.179 fiscalizações</strong> em 2025, e as extraordinárias já superam o PAF."),
    ("fa-circle-check", "Resultado", "<strong style='color:#FFD700;'>79,9%</strong> sem irregularidade; a parcela com irregularidade caiu de 30% para 20% desde 2021."),
]


def encerramento(recado_portos):
    rec = "\n".join(
        f'      <div class="recado"><i class="fas {i}"></i><div><p class="recado-t">{t}</p><p class="recado-d">{d.format(recado_portos=recado_portos)}</p></div></div>'
        for i, t, d in RECADOS)
    return ESCURO_HEAD.format(title=f"Encerramento — {TITULO_DECK}", base="1.3", css=ESCURO_CSS) + f"""<body>
<div class="slide">
  <div class="shape-circle"></div><div class="shape-circle2"></div>
  <div style="height:6px; background:#FFD700; width:100%;"></div>
  <div class="relative z-10 flex-1 px-24 pt-12 pb-4 grid grid-cols-12 gap-10 items-center">
    <div class="col-span-6">
      <div class="flex items-center gap-3 mb-6"><div class="bg-gold" style="width:40px;height:3px;"></div>
        <p class="text-gray-400 text-lg font-montserrat font-medium tracking-widest uppercase">Em síntese</p></div>
      <p class="font-montserrat font-black text-white leading-none" style="font-size:calc(52px * var(--tz));">Menos fiscalizações</p>
      <p class="font-montserrat font-black gold leading-none mt-1" style="font-size:calc(52px * var(--tz));">no plano,</p>
      <p class="font-montserrat font-black text-white leading-none mt-5" style="font-size:calc(52px * var(--tz));">mais por demanda.</p>
      <div class="bg-gold mt-8 mb-6" style="width:100px; height:4px;"></div>
      <p class="text-xl text-gray-300 font-light leading-relaxed max-w-xl">E uma parcela menor delas encontra irregularidade.</p>
    </div>
    <div class="col-span-6 flex flex-col gap-4">
{rec}
    </div>
  </div>
  <div class="relative z-10 px-24 pb-10 flex justify-between items-end border-t border-gray-700 pt-6 mx-8">
    <div><p class="font-montserrat font-bold text-white text-xl">Obrigado.</p>
      <p class="text-gray-400 text-sm mt-1">SFC · Superintendência de Fiscalização e Coordenação das Unidades Regionais — ANTAQ · www.gov.br/antaq</p></div>
    <div class="text-right"><p class="text-gray-400 text-sm">{TITULO_DECK} · Estatísticas da Fiscalização</p>
      <p class="text-gray-500 text-sm font-montserrat font-bold tracking-wider mt-1">{TOTAL} / {TOTAL}</p></div>
  </div>
  <div class="absolute bottom-24 left-1/2 transform -translate-x-1/2 opacity-5" style="z-index:0;"><img src="assets/logo-antaq-branca.png" alt="" style="height:220px;"></div>
</div>
<script src="zoom.js"></script>
<script src="anim.js"></script>
{NAV}
</body>
</html>
"""


def render(s):
    css = f':root {{ --tz-base: {s["base"]:.4g}; }}\n' + BASE_CSS + s["extra_css"]
    tag, ico = MODULOS[s["mod"]]
    return HEAD.format(title=f'{s["title"]} — {TITULO_DECK}', css=css, kicker=s["kicker"], titulo=s["titulo"],
                       tag=tag, tagico=ico, body=s["body"], rodape=RODAPE, n=s["n"], total=TOTAL,
                       head_extra=s["head_extra"], js_extra=s["js_extra"])


(DST / "slide-01.html").write_text(CAPA, encoding="utf-8")
print("slide-01.html (capa)")
for s in sorted(SLIDES, key=lambda s: s["n"]):
    (DST / f"slide-{s['n']:02d}.html").write_text(render(s), encoding="utf-8")
    print(f"slide-{s['n']:02d}.html")
try:
    from slides_portos import RECADO as RECADO_PORTOS
except ImportError:
    RECADO_PORTOS = "Movimentação dos portos organizados e dos terminais privados em 2025."
(DST / f"slide-{TOTAL:02d}.html").write_text(encerramento(RECADO_PORTOS), encoding="utf-8")
print(f"slide-{TOTAL:02d}.html (encerramento)")
