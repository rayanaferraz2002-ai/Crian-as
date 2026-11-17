"""Gera legendas da locução (a partir da transcrição com tempo por palavra) + textos fixos (título).
Saídas: <saida>.srt (para o Premiere) e <saida>.ass (usado pela prévia).
Uso: python3 -I gerar_legendas.py <plano.json> <transcricao.json> <saida_sem_extensao>

Config (projeto.json → config.legendas):
  max_palavras (6), max_dur_s (2.6), correcoes_palavras [[palavra, nova]], correcoes [[trecho, novo]] (após quebrar), estilo_legenda/estilo_titulo (ASS)
  textos: [{"texto": "...", "plano": "T1", "estilo": "Titulo"}]  → texto fixo durante o plano
"""
import sys, json, re

plano_p, trans_p, saida = sys.argv[1:4]
P = json.load(open(plano_p)); cfg = P["config"]; FPS = cfg["fps_num"] / cfg["fps_den"]
L = cfg.get("legendas", {}); T = json.load(open(trans_p))
loc = P.get("locucao"); off = loc["offset_s"] if loc else 0.0
fim_tl = cfg["duracao_final_f"] / FPS

palavras = [dict(w=w["w"].strip(), i=w["i"] + off, f=w["f"] + off) for s in T for w in s["palavras"] if w["w"].strip()]
import math
cp = dict(L.get("correcoes_palavras", []))  # correção palavra a palavra antes de quebrar (pontuação, maiúsculas)
for w in palavras: w["w"] = cp.get(w["w"], w["w"])
maxp, maxd = L.get("max_palavras", 6), L.get("max_dur_s", 2.6)
# 1) quebra em orações (pontuação); 2) cada oração em n blocos equilibrados (sem palavra solta)
oracoes, cur = [], []
for w in palavras:
    cur.append(w)
    if re.search(r"[.,!?;:]$", w["w"]): oracoes.append(cur); cur = []
if cur: oracoes.append(cur)
blocos = []
for o in oracoes:
    n = max(math.ceil(len(o) / maxp), math.ceil((o[-1]["f"] - o[0]["i"]) / maxd))
    n = min(n, max(1, len(o) // 2))
    tam = len(o) / n
    for k in range(n): blocos.append(o[round(k * tam):round((k + 1) * tam)])
legs = []
for b in blocos:
    txt = " ".join(x["w"] for x in b)
    legs.append({"i": b[0]["i"], "f": b[-1]["f"], "t": txt, "estilo": "Legenda"})
for a, b in L.get("correcoes", []):
    for l in legs: l["t"] = l["t"].replace(a, b)
# encosta cada legenda na próxima (sem piscar) se o intervalo for curto
for x, y in zip(legs, legs[1:]):
    if y["i"] - x["f"] < 0.5: x["f"] = y["i"]
for l in legs: l["f"] = min(l["f"], fim_tl)
ps = {p["id"]: p for p in P["planos"]}
fixos = [{"i": ps[t["plano"]]["timeline_in_f"] / FPS, "f": ps[t["plano"]]["timeline_out_f"] / FPS,
          "t": t["texto"], "estilo": t.get("estilo", "Titulo")} for t in L.get("textos", [])]
todas = sorted(fixos + legs, key=lambda x: x["i"])

def ts(t, sep=","):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s % 1) * 1000)):03d}"
with open(saida + ".srt", "w") as f:
    for n, l in enumerate(todas, 1):
        f.write(f"{n}\n{ts(l['i'])} --> {ts(l['f'])}\n{l['t'].replace(chr(92) + 'N', chr(10))}\n\n")
W, H = cfg["largura"], cfg["altura"]
est_leg = L.get("estilo_legenda", "Legenda,DejaVu Sans,46,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,2,1,2,80,80,260,1")
est_tit = L.get("estilo_titulo", "Titulo,DejaVu Sans,64,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,3,2,8,80,80,330,1")
with open(saida + ".ass", "w") as f:
    f.write(f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
            "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: {est_leg}\nStyle: {est_tit}\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    for l in todas:
        a = ts(l["i"], ".")[:-1]; b = ts(l["f"], ".")[:-1]
        f.write(f"Dialogue: 0,{a},{b},{l['estilo']},,0,0,0,,{l['t']}\n")
print(f"ok {len(legs)} legendas + {len(fixos)} textos fixos")
