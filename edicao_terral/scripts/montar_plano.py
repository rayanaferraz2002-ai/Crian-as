"""Gera plano.json: cena -> clipe, entrada/saída na fonte, posição na timeline encaixada nas batidas.
Edite a lista PLANOS (ou o plano.json e rode com --recalcular) para trocar trechos.
Uso: python3 -I montar_plano.py <musica.json> <plano.json> <pasta_proxies> [--recalcular]
"""
import sys, json, os
import numpy as np
import cv2

FPS = 24000 / 1001
CONFIG = {
    "fps_num": 24000, "fps_den": 1001, "largura": 1080, "altura": 1920,
    "duracao_alvo_s": 20.0,
    "rotacao_fonte_graus": -90,  # clipes gravados com câmera deitada: girar 90° anti-horário
    "musica": {"arquivo": "Drop Top Summer (Instrumental).mp4", "inicio_s": 13.932,
               "fade_out_s": 1.5, "fade_video_frames": 12},
    "originais_dir": "/home/user/material_drive",
}
# batidas = duração do plano em batidas da música; entrada_s = ponto de entrada no clipe original
PLANOS = [
 {"id": "A", "cena": 2, "clipe": "MVI_9197.MP4", "entrada_s": 0.15, "batidas": 4,
  "transicao_saida": {"tipo": "Cross Dissolve", "frames": 4},
  "motivo": "Perfil @terralgastrobar no Instagram; dedo vai até o link da bio. Abre a ação do pedido."},
 {"id": "B", "cena": 2, "clipe": "MVI_9197.MP4", "entrada_s": 6.05, "batidas": 4,
  "motivo": "Tela 'Carregando' vira o cardápio próprio do Terral (Destaques/10% de desconto)."},
 {"id": "C", "cena": 2, "clipe": "MVI_9197.MP4", "entrada_s": 9.00, "batidas": 5,
  "motivo": "Rolagem do cardápio com fotos dos pratos; foco bom, mão estável."},
 {"id": "D", "cena": 2, "clipe": "MVI_9197.MP4", "entrada_s": 19.70, "batidas": 3,
  "motivo": "Abre o prato (Risoto de Mignon com Funghi): fecha a cena do pedido com comida em destaque, antes do drop."},
 {"id": "F", "cena": 3, "clipe": "MVI_9200.MP4", "entrada_s": 1.40, "batidas": 5,
  "motivo": "Sacola Terral entra em quadro e é pousada no balcão (lateral). Corte cai no drop da música."},
 {"id": "G", "cena": 3, "clipe": "MVI_9199.MP4", "entrada_s": 7.05, "batidas": 6,
  "motivo": "Corte na ação: sacola pousada de frente, logo nítido."},
 {"id": "H", "cena": 4, "clipe": "MVI_9200.MP4", "entrada_s": 3.80, "batidas": 7,
  "motivo": "Mãos dobrando/fechando a boca da sacola ('embalagem sendo fechada')."},
 {"id": "I", "cena": 4, "clipe": "MVI_9201.MP4", "entrada_s": 0.30, "batidas": 6,
  "motivo": "Sacola fechada em destaque e entregue a outra pessoa (recebimento). Clímax da música."},
 {"id": "K", "cena": 4, "clipe": "MVI_9199.MP4", "entrada_s": 9.85, "batidas": 3,
  "transicao_saida": {"tipo": "Fade to Black", "frames": 12},
  "motivo": "Pack shot final da sacola com logo; sem material de consumo (cena 5), fecha na marca."},
]

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
                 batida_musica_s=round(float(beats[k - p["batidas"]]), 3))
        q["qualidade"] = qualidade(os.path.join(proxies, p["clipe"].split(".")[0] + ".mp4"),
                                   src_in / FPS, src_out / FPS)
        out.append(q)
    cfg = dict(cfg, duracao_final_f=out[-1]["timeline_out_f"],
               duracao_final_s=round(out[-1]["timeline_out_f"] / FPS, 3),
               bpm=musica["bpm"], musica=dict(cfg["musica"], inicio_s=round(float(beats[j0]), 3)))
    return {"config": cfg, "planos": out}

def tc(f):  # timecode 23.976 NDF (base 24)
    return f"{f//86400:02d}:{f//1440%60:02d}:{f//24%60:02d}:{f%24:02d}"

if __name__ == "__main__":
    mus, dst, proxies = sys.argv[1:4]
    musica = json.load(open(mus))
    if "--recalcular" in sys.argv and os.path.exists(dst):
        old = json.load(open(dst)); cfg = old["config"]
        planos = [{k: v for k, v in p.items() if k in ("id","cena","clipe","entrada_s","batidas","transicao_saida","motivo")} for p in old["planos"]]
    else:
        cfg, planos = CONFIG, PLANOS
    plano = resolver(cfg, planos, musica, proxies)
    json.dump(plano, open(dst, "w"), indent=1, ensure_ascii=False)
    for p in plano["planos"]:
        print(f"{p['id']} c{p['cena']} {p['clipe']} src {p['entrada_s']:.2f}-{p['fonte_saida_s']:.2f} "
              f"TL {p['timeline_in_tc']}-{p['timeline_out_tc']} q={p['qualidade']}")
    print("duração final", plano["config"]["duracao_final_s"], "s")
