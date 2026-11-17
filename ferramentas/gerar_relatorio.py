"""Gera relatorio.md e checklist_premiere.md a partir de projeto.json (seção 'relatorio'), plano.json e musica.json.
Uso: python3 -I gerar_relatorio.py <projeto.json> <plano.json> <musica.json> <pasta_saida>
"""
import sys, json, os
proj_p, plano_p, mus_p, outd = sys.argv[1:5]
R = json.load(open(proj_p))["relatorio"]; P = json.load(open(plano_p)); M = json.load(open(mus_p))
cfg, ps = P["config"], P["planos"]; FPS = cfg["fps_num"] / cfg["fps_den"]; B = round(FPS)
def tc(f): return f"{f//(B*3600):02d}:{f//(B*60)%60:02d}:{f//B%60:02d}:{f%B:02d}"
def tab(cab, rows): return ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)] + ["| " + " | ".join(map(str, r)) + " |" for r in rows]
m0 = cfg["musica"]["inicio_s"]; fim = cfg["duracao_final_f"]
alta = [s for s in M["secoes"] if s["energia"] == "alta" and s["fim"] > m0]
drop = alta[0]["inicio"] if alta else None
L = [f"# Relatório de edição — {R['titulo']}", "", "## Material recebido e interpretação", "",
     "Estrutura do Drive diferente da esperada (arquivos soltos). Interpretação:", ""]
L += tab(["Arquivo", "Interpretado como", "Observação"], R["material"]) + ["", R.get("nota_material", ""), "",
     "## Passo 1 — Roteiro", ""] + tab(R["roteiro_cab"], R["roteiro"]) + ["", "## Passo 2 — Referência", ""]
L += [f"- {x}" for x in R["referencia"]] + ["", "## Passo 3 — Música", "",
     f"- BPM **{M['bpm']}** (batida {M['intervalo_batida']} s), {len(M['batidas'])} batidas.",
     "- Seções de energia (s): " + "; ".join(f"{s['inicio']:.1f}–{s['fim']:.1f} {s['energia']}" for s in M["secoes"]),
     f"- Trecho usado: **{m0:.3f} → {m0 + fim / FPS:.3f} s**." + (f" Drop em {drop:.3f} s = {tc(int(round((drop - m0) * FPS)))} na timeline." if drop else ""),
     "- Mapa de batidas: `analise/musica.json`.", "", "## Passo 4/5 — Plano → clipe escolhido", ""]
rows = [[p["id"], p["cena"], p["clipe"], f"{p['entrada_s']:.2f} → {p['fonte_saida_s']:.2f} s", f"{p['timeline_in_tc']} → {p['timeline_out_tc']}",
         p["batidas"], p["motivo"], f"{p['qualidade']['nitidez_laplaciano']}/{p['qualidade']['movimento_medio']}/{p['qualidade']['luminancia_media']}"] for p in ps]
L += tab(["#", "Cena", "Arquivo original", "Entrada → saída (fonte)", "Timeline", "Batidas", "Motivo", "Nitidez/mov./lum."], rows)
durs = [(p["timeline_out_f"] - p["timeline_in_f"]) / FPS for p in ps]
trans = [f"{p['id']}: {p['transicao_saida']['tipo']} {p['transicao_saida']['frames']} quadros" for p in ps if p.get("transicao_saida")]
L += ["", f"Duração {cfg['duracao_final_s']} s ({fim} quadros), {len(ps)} planos, média {sum(durs)/len(durs):.2f} s (mín {min(durs):.2f}, máx {max(durs):.2f}).",
      R.get("ritmo", ""), f"Transições: corte seco na batida; " + ("; ".join(trans) if trans else "nenhuma") + f". Fade-out da música {cfg['musica']['fade_out_s']} s.",
      "", "## Descartados", ""] + tab(["Trecho", "Motivo"], R["descartados"]) + ["", "## Premissas", ""]
L += [f"{i}. {x}" for i, x in enumerate(R["premissas"], 1)]
open(os.path.join(outd, "relatorio.md"), "w").write("\n".join(L) + "\n")
nomes = sorted({p["clipe"] for p in ps} | {cfg["musica"]["arquivo"]})
C = ["# Checklist — Premiere", "", "## Importar", "",
     "1. Ponha numa pasta os originais: " + ", ".join(f"`{n}`" for n in nomes) + ".",
     "2. Arquivo → Importar → `sequencia.xml`. Na janela “Link Media”, aponte para essa pasta (os demais são achados pelo nome).",
     f"3. Confira a sequência `{cfg.get('nome_sequencia','')}`: {cfg['largura']}×{cfg['altura']}, {FPS:.3f} fps, {tc(fim)}.", "",
     "## Conferir / aplicar", ""]
rows = [[f"{tc(0)} → {tc(fim)}", "Rotação", f"XML aplica Rotação {cfg['rotacao_fonte_graus']}° e Escala 100 em todos. Se algum vier deitado/invertido, corrija em Controles de Efeito → Movimento."]]
for i, p in enumerate(ps):
    t = p.get("transicao_saida", {})
    if t.get("tipo") == "Cross Dissolve": rows.append([ps[i + 1]["timeline_in_tc"], "Fusão", f"Cross Dissolve {t['frames']} quadros centrado no corte."])
    if t.get("tipo") == "Fade to Black": rows.append([f"{tc(p['timeline_out_f'] - t['frames'])} → {tc(fim)}", "Fade para preto", f"{t['frames']} quadros no fim do último plano (se não vier, Dip to Black)."])
rows.append([f"{tc(fim - int(round(cfg['musica']['fade_out_s'] * FPS)))} → {tc(fim)}", "Fade-out da música", "Constant Power no fim de A1/A2 (se não vier, aplique)."])
rows.append(["—", "Áudio dos clipes", "Não incluído (só música)."])
for tcx, item, instr in R.get("checklist_extra", []):
    alvo = [p for p in ps if p["clipe"] in instr or p["id"] in instr.split()]
    rows.append([tcx if tcx != "todos" else f"{tc(0)} → {tc(fim)}", item, instr])
for p in ps:
    if p["clipe"] == "MVI_9149.MP4": rows.append([f"{p['timeline_in_tc']} → {p['timeline_out_tc']}", f"Cor plano {p['id']}", "MVI_9149 escuro: subir exposição (ver item Cor)."])
rows += [["—", "Velocidade", "100% em todos (nada aplicado)."], ["—", "Textos", "Nenhum. Sem .srt."]]
C += tab(["Timecode", "Item", "Instrução"], rows) + ["", "## Trocas", "",
     "Edite `projeto.json` (entrada_s/batidas/clipe de um plano) e rode `bash ../ferramentas/rodar_projeto.sh .`. Para ajuste fino sem perder o resto, edite `plano.json` e rode com `--recalcular`."]
open(os.path.join(outd, "checklist_premiere.md"), "w").write("\n".join(C) + "\n")
print("ok")
