"""PASSO 5 — Monta plano.json a partir de decisoes.json + mapa de batidas.
Todo corte cai na batida mais próxima que não corta fala. Uso: python3 04_montar_plano.py"""
import numpy as np
from comum import PROJ, ANALISE, FPS, SEQ_W, SEQ_H, MUSICA, s2f, f2s, tc, ler_json, gravar_json

D = ler_json(PROJ / "decisoes.json")
M = ler_json(ANALISE / "mapa_batidas.json")
ab, mu = D["abertura"], D["musica"]
pre, folga = D["pre_rolagem_fala_s"], D["folga_min_pos_fala_s"]
B = M["batidas"]; drop = mu["virada_drop_s"]
i_drop = min(range(len(B)), key=lambda i: abs(B[i] - drop))
if "fala_inicio" in ab:
    # abertura COM fala: menor nº de batidas que cabe [respiro do título/telefone + fala + folga];
    # a música entra essas batidas antes do drop, e a fala termina logo antes da virada.
    precisa = ab["respiro_inicial_min_s"] + (ab["fala_fim"] - ab["fala_inicio"]) + folga
    k = next(k for k in range(1, i_drop + 1) if drop - B[i_drop - k] >= precisa)
    m0 = B[i_drop - k]
else:
    k, m0 = None, mu["entrada_s"]
batidas = [b - m0 for b in B if b >= m0 - 1e-3]
grade = sorted({s2f(b) for b in batidas})                      # batidas em quadros da sequência
fortes = {s2f(b - m0) for b in M["tempos_fortes"] if b >= m0 - 1e-3}


def mais_proxima(q, lo=None, hi=None):
    c = [g for g in grade if (lo is None or g >= lo) and (hi is None or g <= hi)]
    return min(c, key=lambda g: abs(g - q)) if c else None


def mapear(ancoras, t):
    a = np.array(ancoras, float)
    return float(np.interp(t, a[:, 0], a[:, 1]))


avisos, video, audio, textos, marcadores = [], [], [], [], []
virada = s2f(drop - m0)
assert virada in grade, "virada fora da grade de batidas"

# ---------- cena 1: abertura de tensão (render próprio, abertura_tensao.mov) ----------
if "fala_inicio" in ab:
    o_in = s2f(ab["fala_fim"] + folga) - virada               # 1º quadro da origem usado
    assert o_in >= 0, "clipe curto demais para a abertura"
    ab["src_in"], ab["src_out"] = round(f2s(o_in), 4), round(f2s(o_in + virada), 4)
    vel = 1.0
    a_in = s2f(ab["fala_inicio"] - pre)
    audio.append({"id": "A01", "cena": 1, "papel": "locucao", "clipe": ab["clipe"],
                  "tl_in": a_in - o_in, "tl_out": virada, "src_in": a_in, "src_out": a_in + virada - (a_in - o_in)})
    inicio_fala_abertura = a_in - o_in
    for w0, w1, txt in ab["legendas"]:
        r0, r1 = mapear(ab["ancoras_whisper"], w0), mapear(ab["ancoras_whisper"], w1)
        textos.append({"tipo": "legenda", "texto": txt, "tl_in": max(0, s2f(r0) - o_in), "tl_out": min(virada, s2f(r1) - o_in + 3)})
else:
    vel = round((s2f(ab["src_out"]) - s2f(ab["src_in"])) / virada, 4)
    inicio_fala_abertura = None
video.append({"id": "V01", "cena": 1, "papel": "abertura", "clipe": "abertura_tensao.mov", "origem": ab["clipe"],
              "tl_in": 0, "tl_out": virada, "src_in": 0, "src_out": virada,
              "origem_in_s": ab["src_in"], "origem_out_s": ab["src_out"],
              "velocidade": vel, "escala": 1.0, "ancora_y": 0.5, "motivo": ab["motivo"]})
t_txt = grade[ab["texto_desde_batida"]]
textos.insert(0, {"tipo": "titulo", "texto": ab["texto"], "tl_in": t_txt, "tl_out": virada})
marcadores.append({"quadro": 0, "nome": "SFX telefone", "nota": ab["sfx"]})
marcadores.append({"quadro": virada, "nome": "VIRADA (drop)", "nota": "P&B -> cor no tempo forte (drop da música)"})

# ---------- blocos de fala ----------
cursor = virada
n = 1
for b in D["blocos"]:
    tl0 = cursor
    # escolhe a pré-rolagem (dentro do silêncio disponível) que minimiza tempo morto e põe o fim numa batida
    melhor = None
    for pq in range(s2f(pre), s2f(b.get("pre_max", pre)) + 1):
        s_in_f = s2f(b["fala_inicio"]) - pq
        fim_fala = tl0 + s2f(b["fala_fim"] + b.get("folga_pos_fala", folga)) - s_in_f
        lim = tl0 + s2f(b["max_out"]) - s_in_f
        g = next((g for g in grade if fim_fala <= g <= lim), None)
        if g is not None and (melhor is None or pq + g - fim_fala < melhor[0]):
            melhor = (pq + g - fim_fala, s_in_f, g)
    if melhor is None:
        s_in_f = s2f(b["fala_inicio"] - pre); fim = tl0 + s2f(b["max_out"]) - s_in_f
        avisos.append(f"{b['clipe']}: sem batida entre fim da fala e max_out; corte fora da batida")
    else:
        _, s_in_f, fim = melhor
    def tl(src, s_in_f=s_in_f, tl0=tl0): return tl0 + s2f(src) - s_in_f
    # planos internos
    cortes = [tl0]
    for p in b["planos"]:
        if p["ate"] is None:
            cortes.append(fim)
        else:
            alvo = tl(p["ate"])
            g = mais_proxima(alvo, lo=cortes[-1] + 12, hi=fim - 12)
            cortes.append(g)
            if abs(g - alvo) > 4:
                avisos.append(f"{b['clipe']}: corte interno em {p['ate']}s deslocado {g-alvo:+d} quadros p/ batida")
    for i, p in enumerate(b["planos"]):
        a_, z_ = cortes[i], cortes[i + 1]
        n += 1
        if "broll" in p:
            br = p["broll"]; bi = s2f(br["src_in"])
            video.append({"id": f"V{n:02d}", "cena": p.get("cena", b["cena"]), "papel": "broll", "clipe": br["clipe"],
                          "tl_in": a_, "tl_out": z_, "src_in": bi, "src_out": bi + (z_ - a_),
                          "escala": 1.0, "ancora_y": 0.5, "mudo": True, "motivo": p["motivo"]})
        else:
            e = D["enquadramentos"][p["enq"]]
            video.append({"id": f"V{n:02d}", "cena": p.get("cena", b["cena"]), "papel": "fala", "clipe": b["clipe"],
                          "tl_in": a_, "tl_out": z_, "src_in": s_in_f + (a_ - tl0), "src_out": s_in_f + (z_ - tl0),
                          "enquadramento": p["enq"], "escala": e["zoom"], "ancora_y": e["ancora_y"], "motivo": p["motivo"]})
    audio.append({"id": f"A{len(audio)+1:02d}", "cena": b["cena"], "papel": "locucao", "clipe": b["clipe"],
                  "tl_in": tl0, "tl_out": fim, "src_in": s_in_f, "src_out": s_in_f + (fim - tl0)})
    for w0, w1, txt in b["legendas"]:
        r0, r1 = mapear(b["ancoras_whisper"], w0), mapear(b["ancoras_whisper"], w1)
        textos.append({"tipo": "legenda", "texto": txt, "tl_in": max(tl0, tl(r0)), "tl_out": min(fim, tl(r1) + 3)})
    cursor = fim

total = cursor
# legendas não se sobrepõem
leg = [t for t in textos if t["tipo"] == "legenda"]
for a_, b_ in zip(leg, leg[1:]):
    a_["tl_out"] = min(a_["tl_out"], b_["tl_in"])

# ---------- música: níveis (ganho linear, 1.0 = 0 dB) ----------
ultima_fala = max(t["tl_out"] for t in leg)
fade_q = int(round(mu["fade_saida_batidas"] * M["periodo_batida"] * float(FPS)))
sobe = min(ultima_fala + 6, total - 12)                      # respiro: música sobe quando a fala acaba
fim_fade = max(sobe, total - fade_q)
if inicio_fala_abertura is not None:      # música cheia no telefone/título, abaixa quando ela começa a falar
    niveis = [(0, mu["ganho_abertura"]), (max(1, inicio_fala_abertura - 4), mu["ganho_abertura"]),
              (inicio_fala_abertura + 6, mu["ganho_sob_fala_abertura"]), (virada, mu["ganho_sob_fala_abertura"]),
              (virada + 6, mu["ganho_sob_fala"]),
              (ultima_fala, mu["ganho_sob_fala"]), (sobe, mu["ganho_final"])]
else:
    niveis = [(0, mu["ganho_abertura"]), (virada + 3, mu["ganho_abertura"]), (virada + 12, mu["ganho_sob_fala"]),
          (ultima_fala, mu["ganho_sob_fala"]), (sobe, mu["ganho_final"])]
if fim_fade > sobe:
    niveis.append((fim_fade, mu["ganho_final"]))
niveis.append((total, 0.0))                                   # fade-out até o fim
assert all(a[0] < b[0] for a, b in zip(niveis, niveis[1:])), niveis
musica = {"arquivo": MUSICA, "entrada_s": m0, "src_in": s2f(m0), "src_out": s2f(m0) + total,
          "tl_in": 0, "tl_out": total, "niveis": [{"quadro": q, "ganho": g} for q, g in niveis],
          "bpm": M["bpm"], "drop_s": drop, "batidas_abertura": k}
marcadores.append({"quadro": fim_fade, "nome": "Fade-out música", "nota": f"{total-fim_fade} quadros até silêncio"})

# checagens
for v in video:
    assert v["tl_in"] in grade or v["tl_in"] == 0, v
    assert v["tl_out"] in grade or v["tl_out"] == total, v
cortes_fora = [v["id"] for v in video if v["tl_out"] not in grade]
plano = {
    "_leia": "Gerado por scripts/04_montar_plano.py a partir de decisoes.json. Quadros a 23,976 fps (tl_* = sequência, src_* = origem).",
    "sequencia": {"fps": "24000/1001", "largura": SEQ_W, "altura": SEQ_H, "duracao_quadros": total,
                  "duracao_s": round(f2s(total), 3), "duracao_tc": tc(total)},
    "virada": {"quadro": virada, "tc": tc(virada), "musica_s": drop, "tempo_forte": virada in fortes},
    "abertura": {**ab, "quadros": virada, "velocidade": vel},
    "video": video, "audio": audio, "musica": musica, "textos": textos, "marcadores": marcadores,
    "fusoes": D["fusoes"], "descartes": D["descartes"], "avisos": avisos,
    "cortes_fora_da_batida": cortes_fora}
gravar_json(PROJ / "plano.json", plano)
print(f"duração {f2s(total):.2f}s ({tc(total)}) | virada {tc(virada)} tempo_forte={virada in fortes}")
for v in video:
    print(f"{v['id']} cena {v['cena']!s:4} {v['clipe']:20} TL {tc(v['tl_in'])}-{tc(v['tl_out'])} "
          f"({f2s(v['tl_out']-v['tl_in']):.2f}s, {(v['tl_out']-v['tl_in'])/ (M['periodo_batida']*float(FPS)):.1f} bat) "
          f"src {f2s(v['src_in']):.2f}-{f2s(v['src_out']):.2f} {v.get('enquadramento', v['papel'])}")
for a in avisos: print("AVISO:", a)
