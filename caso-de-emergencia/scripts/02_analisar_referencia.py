"""PASSO 2 — Referência: formato, planos (PySceneDetect), ritmo em batidas.
Uso: python3 02_analisar_referencia.py --src PASTA_ORIGINAIS"""
import argparse
from fractions import Fraction
from scenedetect import detect, AdaptiveDetector
from comum import ANALISE, REFERENCIA, midia_dir, ffprobe, gravar_json, ler_json

ap = argparse.ArgumentParser(); ap.add_argument("--src"); a = ap.parse_args()
ref = midia_dir(a.src) / REFERENCIA
info = ffprobe(ref)
v = next(s for s in info["streams"] if s["codec_type"] == "video")
cenas = detect(str(ref), AdaptiveDetector())
planos = [{"n": i + 1, "inicio": round(s.get_seconds(), 3), "fim": round(e.get_seconds(), 3),
           "dur": round(e.get_seconds() - s.get_seconds(), 3)} for i, (s, e) in enumerate(cenas)]
per = ler_json(ANALISE / "mapa_batidas.json")["periodo_batida"]
for p in planos:
    p["batidas_86bpm"] = round(p["dur"] / per, 1)
dur = float(info["format"]["duration"])
terco = [[p["dur"] for p in planos if lo <= p["inicio"] < hi] for lo, hi in ((0, dur/3), (dur/3, 2*dur/3), (2*dur/3, dur+1))]
dados = {"arquivo": REFERENCIA, "duracao": round(dur, 2), "largura": v["width"], "altura": v["height"],
         "fps": float(Fraction(v["r_frame_rate"])), "n_planos": len(planos),
         "media_plano": round(sum(p["dur"] for p in planos) / len(planos), 2),
         "media_por_terco": [round(sum(x)/len(x), 2) if x else None for x in terco],
         "planos": planos,
         "observado_manualmente": {
             "transicoes": "somente cortes secos",
             "abertura_pb": "0,00-8,57 s em preto e branco (telefonema/urgencia), virada para cor no inicio do caso",
             "padrao": "cabeca falante longa + insercoes curtas de B-roll (1,4-3,9 s) sobre a fala; legenda o tempo todo",
             "estrutura": {"gancho": "0-8,6 s", "caso": "8,6-26 s", "desenvolvimento/explicacao": "27-85 s",
                           "conclusao": "85-111,7 s"}}}
gravar_json(ANALISE / "referencia.json", dados)
print(f"{dados['n_planos']} planos, média {dados['media_plano']}s, por terço {dados['media_por_terco']}")
