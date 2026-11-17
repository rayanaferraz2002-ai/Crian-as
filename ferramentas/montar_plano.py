"""Gera plano.json: cena -> clipe, entrada/saída na fonte, posição na timeline encaixada nas batidas.
Lê config e planos de projeto.json (ou, com --recalcular, do plano.json existente).
Uso: python3 -I montar_plano.py <projeto.json> <musica.json> <plano.json> <pasta_proxies> [--recalcular]
"""
import sys, json, os
import numpy as np
import cv2

FPS = 24000 / 1001

def qualidade(proxy, a, b):
    cap = cv2.VideoCapture(proxy)
    cap.set(cv2.CAP_PROP_POS_MSEC, a * 1000)
    sharp, motion, lum, prev = [], [], [], None
    while cap.get(cv2.CAP_PROP_POS_MSEC) < b * 1000:
        ok, f = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(f, (360, 640)), cv2.COLOR_BGR2GRAY)
        sharp.append(cv2.Laplacian(g, cv2.CV_64F).var()); lum.append(g.mean())
        if prev is not None: motion.append(np.abs(g.astype(int) - prev).mean())
        prev = g.astype(int)
    return {"nitidez_laplaciano": round(float(np.median(sharp)), 1),
            "movimento_medio": round(float(np.mean(motion)), 2) if motion else 0,
            "luminancia_media": round(float(np.mean(lum)), 1)}

def fr(t):  # segundos -> frame inteiro
    return int(round(t * FPS))

def resolver(cfg, planos, musica, proxies):
    global FPS
    FPS = cfg["fps_num"] / cfg["fps_den"]
    beats = np.array(musica["batidas"]); m0 = cfg["musica"]["inicio_s"]
    j0 = int(np.argmin(np.abs(beats - m0)))
    k, out = j0, []
    for p in planos:
        t_in = beats[k] - beats[j0]; k += p["batidas"]; t_out = beats[k] - beats[j0]
        tl_in, tl_out = fr(t_in), fr(t_out)
        src_in = fr(p["entrada_s"]); src_out = src_in + (tl_out - tl_in)
        q = dict(p, timeline_in_f=tl_in, timeline_out_f=tl_out,
                 fonte_in_f=src_in, fonte_out_f=src_out,
                 fonte_saida_s=round(src_out / FPS, 3),
                 timeline_in_tc=tc(tl_in), timeline_out_tc=tc(tl_out),
                 batida_musica_s=round(float(beats[k - p["batidas"]]), 3), _k0=k - p["batidas"])
        q["qualidade"] = qualidade(os.path.join(proxies, p["clipe"].rsplit(".", 1)[0] + ".mp4"),
                                   src_in / FPS, src_out / FPS)
        out.append(q)
    cfg = dict(cfg, duracao_final_f=out[-1]["timeline_out_f"],
               duracao_final_s=round(out[-1]["timeline_out_f"] / FPS, 3),
               bpm=musica["bpm"], musica=dict(cfg["musica"], inicio_s=round(float(beats[j0]), 3)))
    return {"config": cfg, "planos": out, "_beats": [float(x) for x in beats], "_j0": j0}

def resolver_extras(plano):
    """Locução (alinhada ao início de um plano) e sobreposições (V2) em quadros da timeline."""
    cfg = plano["config"]; ps = {p["id"]: p for p in plano["planos"]}
    loc = cfg.get("locucao")
    if loc:
        ref = ps[loc["plano_inicio"]]
        fala_tl = ref["timeline_in_f"] + fr(loc.get("atraso_fala_s", 0.15))
        tl_in = fala_tl - fr(loc["fala_inicio_s"] - loc.get("entrada_s", 0))
        dur = fr(loc["saida_s"] - loc.get("entrada_s", 0))
        plano["locucao"] = {"arquivo": loc["arquivo"], "timeline_in_f": tl_in, "timeline_out_f": tl_in + dur,
                            "fonte_in_f": fr(loc.get("entrada_s", 0)), "fonte_out_f": fr(loc.get("entrada_s", 0)) + dur,
                            "offset_s": round(tl_in / FPS - loc.get("entrada_s", 0), 4)}
        a = ps[loc["abaixar_musica_de"]]["timeline_in_f"]; b = ps[loc["abaixar_musica_ate"]]["timeline_out_f"]
        plano["ducking"] = {"de_f": a, "ate_f": b, "ganho_db": loc.get("musica_ganho_db", -14)}
    sobre = []
    for s in cfg.get("sobreposicoes", []):
        ref = ps[s["plano"]]; beats = plano["_beats"]; k0 = ref["_k0"] + s.get("offset_batidas", 0)
        a = fr(beats[k0] - beats[plano["_j0"]]); b = fr(beats[k0 + s["batidas"]] - beats[plano["_j0"]])
        sobre.append(dict(s, timeline_in_f=a, timeline_out_f=b, timeline_in_tc=tc(a), timeline_out_tc=tc(b)))
    if sobre: plano["sobreposicoes"] = sobre
    for p in plano["planos"]: p.pop("_k0", None)
    plano.pop("_beats", None); plano.pop("_j0", None)

def tc(f):  # timecode NDF, base = fps arredondado
    b = round(FPS)
    return f"{f//(b*3600):02d}:{f//(b*60)%60:02d}:{f//b%60:02d}:{f%b:02d}"

if __name__ == "__main__":
    proj_p, mus, dst, proxies = sys.argv[1:5]
    proj = json.load(open(proj_p))
    musica = json.load(open(mus))
    if "--recalcular" in sys.argv and os.path.exists(dst):
        old = json.load(open(dst)); cfg = old["config"]
        planos = [{k: v for k, v in p.items() if k in ("id","cena","clipe","entrada_s","batidas","transicao_saida","motivo","rotacao_graus","texto")} for p in old["planos"]]
    else:
        cfg, planos = proj["config"], proj["planos"]
    plano = resolver(cfg, planos, musica, proxies)
    resolver_extras(plano)
    json.dump(plano, open(dst, "w"), indent=1, ensure_ascii=False)
    for p in plano["planos"]:
        print(f"{p['id']} c{p['cena']} {p['clipe']} src {p['entrada_s']:.2f}-{p['fonte_saida_s']:.2f} "
              f"TL {p['timeline_in_tc']}-{p['timeline_out_tc']} q={p['qualidade']}")
    print("duração final", plano["config"]["duracao_final_s"], "s")
