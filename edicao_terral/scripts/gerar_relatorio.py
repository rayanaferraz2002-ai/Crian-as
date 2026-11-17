"""Gera relatorio.md e checklist_premiere.md a partir de plano.json e musica.json.
Uso: python3 -I gerar_relatorio.py <plano.json> <musica.json> <pasta_saida>
"""
import sys, json, os
plano_p, mus_p, outd = sys.argv[1:4]
P = json.load(open(plano_p)); cfg = P["config"]; ps = P["planos"]; M = json.load(open(mus_p))
FPS = cfg["fps_num"] / cfg["fps_den"]
def tc(f): return f"{f//86400:02d}:{f//1440%60:02d}:{f//24%60:02d}:{f%24:02d}"
m0 = cfg["musica"]["inicio_s"]; mend = m0 + cfg["duracao_final_s"]
drop = next(s for s in M["secoes"] if s["energia"] == "alta" and s["inicio"] >= m0)["inicio"]
L = []
L += ["# Relatório de edição — Terral (delivery)", "",
"## Material recebido e interpretação", "",
"O Drive não seguiu a estrutura esperada: 5 arquivos soltos, sem subpastas.", "",
"| Arquivo | Interpretado como | Observação |", "|---|---|---|",
"| Drop Top Summer (Instrumental).mp4 | musica/ | Só áudio AAC, 187,9 s |",
"| MVI_9197.MP4 | clipes/ | Celular: Instagram → link → cardápio Terral → prato. 24,2 s |",
"| MVI_9199.MP4 | clipes/ | Balcão; sacola Terral pousada (6,8–11,4 s). 11,4 s |",
"| MVI_9200.MP4 | clipes/ | Sacola pousada e mãos fechando a boca da sacola. 10,8 s |",
"| MVI_9201.MP4 | clipes/ | Sacola em destaque e entregue a outra pessoa. 4,2 s |",
"| — | roteiro/ | Ausente no Drive; usado o roteiro enviado na conversa |",
"| — | referencia/ | **Ausente** |", "| — | locucao/ | **Ausente** |", "",
"Clipes: 1920×1080, 23,976 fps, gravados com a câmera deitada (conteúdo vertical). Girados 90° anti-horário → 1080×1920.", "",
"## Passo 1 — Roteiro", "",
"| Cena | Direção de imagem | Direção de edição | Duração | Áudio/fala | Status |", "|---|---|---|---|---|---|",
"| 1 Gancho | Pessoa em casa abrindo espaço na mesa | não especificada | não especificada | “Hoje você escolhe onde. A gente cuida da comida.” | **Cortada** (sem material) |",
"| 2 Pedido | Celular acessando o cardápio próprio do Terral | não especificada | não especificada | “Faça seu pedido pelo nosso link.” | Montada |",
"| 3 Preparo | Prato sendo preparado e colocado na embalagem | não especificada | não especificada | “O cuidado começa na cozinha…” | Montada com alternativa (embalagem) |",
"| 4 Recebimento | Embalagem sendo fechada → aberta pelo cliente | corte (match) fechada → aberta | não especificada | “…e acompanha o seu pedido.” | Montada parcialmente (fechada → entregue) |",
"| 5 Consumo | Comida à mesa e pessoa começando a refeição | não especificada | não especificada | “Peça Terral. Link na bio.” | **Cortada** (sem material) |", "",
"## Passo 2 — Referência", "", "Não havia vídeo de referência. Formato e ritmo definidos por você: 9:16, 20 s; fps = o dos clipes (23,976).", "",
"## Passo 3 — Música", "",
f"- BPM: **{M['bpm']}** (batida = {M['intervalo_batida']} s; compasso 4/4 ≈ {4*M['intervalo_batida']:.3f} s)",
f"- {len(M['batidas'])} batidas detectadas; a música começa com ~10 s de ambiência sem batida marcada.",
"- Seções de energia (s): " + "; ".join(f"{s['inicio']:.1f}–{s['fim']:.1f} {s['energia']}" for s in M["secoes"][:6]) + " …",
f"- Trecho usado: **{m0:.3f}–{mend:.3f} s** da faixa (começa num tempo forte). Subida/intro até o drop em {drop:.3f} s, que cai em {tc(int(round((drop-m0)*FPS)))} da timeline = início da cena 3. Cena 4 fica na parte de maior energia (clímax).",
"- Mapa completo de batidas: `analise/musica.json`.", "",
"## Passo 4/5 — Cena → clipe escolhido", "",
"| # | Cena | Arquivo original | Entrada → saída (fonte) | Timeline | Batidas | Motivo | Nitidez/mov. |", "|---|---|---|---|---|---|---|---|"]
for p in ps:
    q = p["qualidade"]
    L.append(f"| {p['id']} | {p['cena']} | {p['clipe']} | {tc(p['fonte_in_f'])} → {tc(p['fonte_out_f'])} ({p['entrada_s']:.2f}–{p['fonte_saida_s']:.2f} s) | "
             f"{p['timeline_in_tc']} → {p['timeline_out_tc']} | {p['batidas']} | {p['motivo']} | {q['nitidez_laplaciano']}/{q['movimento_medio']} |")
durs = [(p['timeline_out_f']-p['timeline_in_f'])/FPS for p in ps]
L += ["", f"Duração final {cfg['duracao_final_s']} s ({cfg['duracao_final_f']} quadros). Plano médio {sum(durs)/len(durs):.2f} s; cortes a cada 3–7 batidas: "
      "4 batidas na intro (calma), corte no drop, planos mais longos no clímax por falta de material.",
"Transições: corte seco em todos os cortes (sempre na batida), exceto fusão de 4 quadros A→B (tela branca 'Carregando') e fade para preto de 12 quadros no fim. Música com fade-out de 1,5 s.", "",
"## Descartados", "",
"| Trecho | Motivo |", "|---|---|",
"| MVI_9199 2,4–3,8 s (funcionária de touca ao fundo) | Testado no drop: fora de foco e escuro (nitidez 4,5 vs >100 nos outros). |",
"| MVI_9199 0–1,2 s / 4–6,7 s | Balcão vazio, sem ação. |",
"| MVI_9197 2,0–6,0 s | Tela escurecendo/branca e 'Carregando' (só o finzinho entra no plano B). |",
"| MVI_9197 12,5–14,0 s | Tela escura/rolagem borrada. |",
"| MVI_9197 23,0 s → fim | Pop-up 'Qual é o seu celular?' — não é do cardápio. |",
"| MVI_9200 9,3 s → fim / MVI_9201 3,2 s → fim | Sacola saindo de quadro, desfocado. |", "",
"## Premissas e decisões (registradas)", "",
"1. Cenas 1 e 5 removidas por falta de imagem (decisão sua). Os textos/falas não entram (decisão sua: “sem falas”) → sem trilha de locução e sem .srt.",
"2. Cena 3: não há imagem de cozinha/prato; usada a sacola chegando ao balcão (decisão sua).",
"3. Cena 4: não há cliente abrindo a sacola; usado ‘sacola sendo fechada’ → ‘sacola entregue’ (recebimento) e pack shot final da marca. MVI_9199 aparece em G e K (trechos diferentes, 7,05–9,76 e 9,85–11,22) por falta de material para o fechamento.",
"4. Sem referência: 1080×1920, 23,976 fps (fps nativo dos clipes), 20 s — o mais próximo de 20 s na grade de batidas é 20,02 s (43 batidas).",
"5. Velocidade, zoom e cor: nada pedido no roteiro; nada aplicado. Sugestões no checklist.",
"6. Originais intocados (somente leitura); tudo foi feito em cópias/proxies 720p.",
]
open(os.path.join(outd, "relatorio.md"), "w").write("\n".join(L) + "\n")

C = ["# Checklist — aplicar no Premiere", "",
"## Importar", "",
"1. Coloque os 5 arquivos originais numa pasta (nomes exatos: MVI_9197.MP4, MVI_9199.MP4, MVI_9200.MP4, MVI_9201.MP4, Drop Top Summer (Instrumental).mp4).",
"2. Premiere → Arquivo → Importar → `sequencia.xml`. Se aparecer “Link Media”, aponte para essa pasta (ele acha os demais pelo nome).",
"   - Ou gere o XML já com o seu caminho: `python3 -I scripts/gerar_xml.py plano.json saida/sequencia.xml --base \"/Users/VOCE/Terral\"`.",
"3. Confira a sequência: 1080×1920, 23,976 fps, 00:00:20:00.", "",
"## O que conferir/aplicar (o XML não carrega bem)", "",
"| Timecode | Item | Instrução |", "|---|---|---|",
f"| 00:00:00:00 → {tc(cfg['duracao_final_f'])} (todos os clipes) | Rotação | O XML aplica Rotação −90° e Escala 100. Se algum clipe vier deitado ou de cabeça para baixo, em Controles de Efeito → Movimento use −90 (ou 90) e Escala 100. A imagem deve preencher o quadro vertical inteiro. |",
]
for p in ps:
    if p.get("transicao_saida", {}).get("tipo") == "Cross Dissolve":
        C.append(f"| {ps[ps.index(p)+1]['timeline_in_tc']} | Fusão A→B | Cross Dissolve de {p['transicao_saida']['frames']} quadros centrado no corte. Se não vier, aplique (Ctrl/Cmd+D). |")
C += [f"| {tc(cfg['duracao_final_f']-12)} → {tc(cfg['duracao_final_f'])} | Fade para preto | Cross Dissolve/Dip to Black de 12 quadros no fim do último clipe. |",
f"| {tc(cfg['duracao_final_f']-int(round(cfg['musica']['fade_out_s']*FPS)))} → {tc(cfg['duracao_final_f'])} | Fade-out da música | Constant Power de 1,5 s no fim das trilhas A1/A2. Se não vier, aplique. |",
"| 00:00:00:00 | Áudio dos clipes | O XML não traz o áudio de câmera (só a música). Mantenha assim. |",
]
for p in ps:
    if p["clipe"] == "MVI_9201.MP4":
        C.append(f"| {p['timeline_in_tc']} → {p['timeline_out_tc']} | Cor | MVI_9201 está mais clara/quente que os demais (luminância ~84 vs ~65). Em Lumetri, baixe exposição ~0,3 e temperatura levemente para casar com 9199/9200. |")
    if p["id"] == "B":
        C.append(f"| {p['timeline_in_tc']} → {ps[3]['timeline_out_tc']} | Cor (opcional) | Planos do celular (MVI_9197) têm fundo preto e contraste diferente das cenas de balcão; ajuste fino opcional. |")
for p in ps:
    if p["cena"] == 3 and p["id"] == "F":
        C.append(f"| {p['timeline_in_tc']} | Drop da música | Corte no drop. Opcional: punch-in leve (Escala 100→108 em 6 quadros) para marcar o drop — não pedido no roteiro. |")
C += ["| — | Velocidade | Nenhuma alteração de velocidade aplicada (100% em todos). |",
"| — | Textos na tela | Nenhum (decisão: sem falas). Sem .srt. |", "",
"## Trocas depois", "", "Edite `plano.json` (campo `entrada_s` ou `batidas` de um plano) e rode `bash scripts/rodar_tudo.sh --recalcular`. Os cortes se re-encaixam nas batidas e preview/XML/relatórios são refeitos."]
open(os.path.join(outd, "checklist_premiere.md"), "w").write("\n".join(C) + "\n")
print("ok")
