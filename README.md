# Desempenho Aquaviário 2025 — Estatísticas da Fiscalização

Deck de 10 slides da SFC. Segue a sequência do relatório anterior (`../250220 Apresentação SFC Estatístico Aquaviário.pptx`) com os números refeitos, no mesmo template HTML dos decks `apresentacao_sfc_diretoria`, `apresentacao_paf_diretoria` e `planejamento-inteligencia-2026`. Acrescenta três slides novos sobre os portos brasileiros.

Estrutura: 01 capa · 02 estrutura da SFC · 03 ambiente fiscalizado · 04 o setor portuário em 2025 · 05 mapa dos portos e terminais privados · 06 onde e o que se movimenta · 07 perfil das fiscalizações · 08 o ano de 2025 em números · 09 o que as fiscalizações encontram · 10 encerramento.

Para ver: `python3 -m http.server 8767` nesta pasta e abrir `http://localhost:8767/`.

## Como regerar

Todo o deck, inclusive capa e encerramento, sai de `python3 build_slides.py`. Não edite os `slide-NN.html` à mão: a próxima geração apaga a edição.

- `build_slides.py`: o template (cabeçalho, rodapé, CSS), os slides de fiscalização (02, 03, 07–09), a capa e o encerramento. Os números do PIF estão escritos no próprio script.
- `slides_portos.py`: os slides 04 a 06. Lê `dados/portos.json` e é chamado por `build_slides.py`.
- `graficos.js`: utilitários dos gráficos ECharts (`window.G`), com cores por papel, eixos, tooltip e atraso até o card pousar.
- `BASES`, em `build_slides.py`: a escala de texto de cada slide, medida no Chrome em 1920×1080.

## Fontes

| Slides | Fonte | Data |
|---|---|---|
| 02, 03 | Universo Fiscalizado (PIF): serviços regulados por área, modalidade e unidade | 16/11/2026 |
| 02 | Regimento Interno da ANTAQ, art. 83 (estrutura) | — |
| 04–06 | Estatístico Aquaviário da ANTAQ e painéis de instalações (dados públicos), via conector MCP independente | 16/11/2026 |
| 07–09 | PIF (SFIS): Fiscalizações Realizadas, Fiscalizações Realizadas por Área e quadro de detalhe por procedimento | captura de 23/09/2026 |

- `dados/portos.json`: o levantamento dos slides 04 a 06. Traz a série 2021–2025, as instalações com coordenadas aproximadas, as mercadorias e o perfil de carga. Não traz CNPJ.
- `dados/brasil-uf.js`: malha estadual do IBGE (API de malhas, qualidade mínima), simplificada para 3 casas decimais. É o fundo do mapa do slide 05.

## Ressalvas

- **PIF é dado interno.** As séries de fiscalização vêm de captura interna de 23/09/2026. O deck não mostra razão social, CNPJ nem nome de servidor (art. 86 do Regimento). Mesmo assim, avalie antes de publicar abertamente.
- **Slide 09:** o "índice de permanência de irregularidades" do relatório anterior não é reproduzível com os quadros atuais do PIF. Foi trocado pela parcela de fiscalizações com irregularidade constatada.
- **Contagens diferentes por quadro:** em 2025, a série oficial dá 1.179 fiscalizações, o quadro por área 1.187 e o detalhe por procedimento 1.221. Cada slide diz qual quadro usou.
- **2024 revisado:** o PIF hoje dá 537 do PAF e 775 extraordinárias. O relatório anterior trazia 538 e 798.
- **Rotina:** 538 registros em 2025, contra 2.421 em 2024. A queda aparece em todas as unidades e sugere mudança na forma de registrar; convém confirmar antes de comparar os anos.
- **Mapa:** as posições são aproximadas, porque nenhum painel publica coordenadas. Barra do Riacho e Laguna não têm linha no Estatístico Aquaviário. Forno e Manaus aparecem com 0 t (círculo vazado).
- **Fundo do mapa:** os mosaicos do CARTO passaram a exigir chave de API, por isso o fundo é a malha do IBGE, salva localmente. O mapa não depende de servidor de mosaicos.
- Nomes e telefones das chefias do relatório anterior ficaram de fora.

## Gráficos e mapa

- ECharts 5.5.1 com renderizador SVG, para ficar nítido quando o visualizador escala o iframe. Cada gráfico só desenha depois que o card que o contém pousa.
- Cores por papel, iguais em todo o deck: porto, PAF e porto organizado em azul (#0066CC); marítima, extraordinárias e TUP em laranja (#eb6834); interior em verde-água (#1baf7a). A paleta foi validada para daltonismo. O verde-água fica abaixo de 3:1 sobre branco, por isso os gráficos usam rótulo direto.
- Mapa em Leaflet 1.9.4: bolha proporcional à tonelagem de 2025, filtros por tipo e por região e lista clicável das cinco maiores. O teclado do Leaflet fica desligado para não roubar as setas do passador.

## Animação de entrada

`anim.js` (do deck Dia de Fiscal 2026) faz os cards entrarem em sequência e as barras crescerem da esquerda para a direita. Os textos soltos deslizam. Os painéis de gráfico (`.painel`) entram como cards. A capa não anima. A animação respeita "reduzir movimento".

## Passador sem fio

O `index.html` descarta avanços por tecla que chegam menos de 600 ms depois de outro avanço por tecla. Para testar outro valor, use `?intervalo=800` na URL (em milissegundos; `0` desliga).

## Cartão de compartilhamento

`assets/og-capa.jpg` (1200×630) é captura de `assets/og-fonte.html`; o passo a passo está no comentário do próprio arquivo. Ao trocar a imagem, suba o `?v=` nas metatags do `index.html`.

## Publicação

Repositório `antaq/desempenho-aquaviario-2025`, publicado pelo GitHub Pages a partir da branch `main`, pasta raiz: https://antaq.github.io/desempenho-aquaviario-2025/. Cada push na `main` republica.
