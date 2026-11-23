"""Gera legendas.srt (fala), texto_na_tela.srt (título da cena 1) e checklist_premiere.md a partir de plano.json."""
import math
from comum import PROJ, ANALISE, SEQ_H, f2s, tc, srt_tc, ler_json

P = ler_json(PROJ / "plano.json"); pos = ler_json(ANALISE / "posicoes_premiere.json")


def srt(itens, nome):
    out = []
    for i, t in enumerate(itens, 1):
        out += [str(i), f"{srt_tc(math.ceil(f2s(t['tl_in'])*1000)/1000)} --> {srt_tc(math.floor(f2s(t['tl_out'])*1000)/1000 - 0.001)}", t["texto"], ""]
    (PROJ / nome).write_text("\n".join(out), encoding="utf-8")


srt([t for t in P["textos"] if t["tipo"] == "legenda"], "legendas.srt")
srt([t for t in P["textos"] if t["tipo"] == "titulo"], "texto_na_tela.srt")

ab = P["abertura"]; e = ab["efeito"]; n = ab["quadros"]
tit = next(t for t in P["textos"] if t["tipo"] == "titulo")
ax, ay = e["ancora"]
pos_y_fim = ay * SEQ_H + (0.5 - ay) * SEQ_H * e["zoom_fim"]
db = lambda g: "-∞ dB" if g == 0 else f"{20*math.log10(g):+.1f} dB"
L = ["# Checklist — aplicar no Premiere", "",
     "Timecodes da sequência `CASO DE EMERGENCIA` (23,976 fps, começa em 00:00:00:00).", "",
     "## 0. Ao importar",
     "- [ ] **Vincular mídia** aos ORIGINAIS (ver LEIA-ME). `abertura_tensao.mov` fica na mesma pasta dos originais.",
     "- [ ] Se algum clipe 4K aparecer **deitado**: Efeitos > Controles de efeito > Movimento > Rotação = 90° (o XML assume que o Premiere lê a rotação do arquivo, como faz nas versões atuais).",
     "- [ ] Conferir se os clipes 4K vieram com **Escala 50%** (ocupam o quadro 1080×1920 inteiro).", "",
     "## 1. Cena 1 — abertura (00:00:00:00 → " + tc(n) + ")",
     f"- [ ] **SFX de telefone** na trilha A5 em 00:00:00:00 (marcador \"SFX telefone\"). Não havia esse som no Drive.",
     f"- [ ] **Texto \"{tit['texto']}\"** de {tc(tit['tl_in'])} até {tc(tit['tl_out']-1)}: Gráficos essenciais, fonte sem serifa extra-negrito, branco, terço superior (Y ≈ 25%). Ou importe `texto_na_tela.srt`.",
     f"- [ ] O visual P&B + efeito já está **renderizado** em `abertura_tensao.mov` (só imagem; a fala vem do `{ab['clipe']}` nas trilhas A1/A2). Se quiser refazer no Premiere sobre o `{ab['clipe']}` original:", "",
     "| Parâmetro | Início (00:00:00:00) | Fim (" + tc(n-1) + ") | Onde |", "|---|---|---|---|",
     (f"| Velocidade | {ab['velocidade']*100:.1f}% (Interpolação: Fluxo óptico) | — | Clique direito > Velocidade/Duração |"
      if abs(ab['velocidade'] - 1) > 1e-3 else f"| Trecho de origem | {ab['clipe']} {ab['src_in']:.2f}s → {ab['src_out']:.2f}s, velocidade 100% (há fala) | — | — |"),
     f"| Saturação | 0 | 0 | Lumetri > Correção básica |",
     f"| Contraste | +{round((e['contraste_ini']-1)*100)} | +{round((e['contraste_fim']-1)*100)} (keyframe linear) | Lumetri > Correção básica |",
     f"| Vinheta (Quantidade) | -1,5 | -3,0 (keyframe linear); Ponto médio 40, Difusão 50 | Lumetri > Vinheta |",
     f"| Grão | Ruído 8% (desmarcar ruído colorido) | igual | Efeitos > Ruído e granulação > Ruído |",
     f"| Escala | 50% | {50*e['zoom_fim']:.0f}% (Bezier, **aceleração no fim** = ease-in) | Movimento |",
     f"| Posição | 540 × 960 | 540 × {pos_y_fim:.0f} (zoom ancorado no rosto) | Movimento |", "",
     f"- [ ] Virada P&B → cor em **{tc(n)}** = drop da música ({P['virada']['musica_s']:.3f} s da faixa, tempo forte). Não mover.", "",
     "## 2. Enquadramentos (zoom digital nos originais 4K) — o XML já leva, só conferir", "",
     "| Plano | Entrada | Saída | Clipe | Escala | Posição (X × Y) |", "|---|---|---|---|---|---|"]
for v in P["video"][1:]:
    s, d = pos[v["id"]]["escala_pct"], pos[v["id"]]["deslocamento_y_px"]
    L.append(f"| {v['id']} {v.get('enquadramento', v['papel'])} | {tc(v['tl_in'])} | {tc(v['tl_out'])} | {v['clipe']} | {s:g}% | 540 × {960+d:.0f} |")
L += ["",
      "## 3. Textos e legendas",
      "- [ ] Arquivo > Importar `legendas.srt` → arrastar para a linha do tempo (cria trilha de legendas). Revisar grafia: a transcrição é automática e foi corrigida à mão.",
      "- [ ] Estilo sugerido (como na referência): branco, contorno preto fino, centralizado a ~65% da altura.", "",
      "## 4. Áudio",
      "- [ ] Locução (A1/A2, áudio da câmera): Som essencial > Diálogo > Loudness: Corresponder automaticamente (-16 LUFS para Reels).",
      "- [ ] Música (A3/A4): o XML leva keyframes de nível. Conferir:"]
for k in P["musica"]["niveis"]:
    L.append(f"  - {tc(k['quadro'])}: {db(k['ganho'])}")
L += ["  Se os keyframes não vierem, recrie com a ferramenta Caneta nos pontos acima.",
      "- [ ] **Fade-out da música** nos últimos 2 tempos (marcador \"Fade-out música\").", "",
      "## 5. Final",
      f"- [ ] Mergulho para preto ({P['fusoes']['fim_para_preto_quadros']} quadros) no fim — o XML leva uma Dissolução cruzada; se não vier, aplique *Mergulhar para preto*.",
      "- [ ] **Desligar o botão de proxy** antes de exportar. Exportar H.264, 1080×1920, 23,976, \"Corresponder à sequência\", taxa alvo 16–20 Mbps.", ""]
(PROJ / "checklist_premiere.md").write_text("\n".join(L), encoding="utf-8")
print("ok: legendas.srt, texto_na_tela.srt, checklist_premiere.md")
