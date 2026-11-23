"""Gera sequencia.xml (Final Cut Pro 7 XML / xmeml v4) a partir de plano.json, para importar no Premiere.
Aponta para os ORIGINAIS pelo nome (não proxies); a cena 1 usa abertura_tensao.mov.
Uso: python3 07_gerar_xml.py [--src PASTA_ORIGINAIS] [--media-dir "/Users/voce/.../05. CASO DE EMERGÊNCIA"]"""
import argparse, xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote
from comum import PROJ, ANALISE, FPS, SEQ_W, SEQ_H, MUSICA, ffprobe, rotacao, ler_json, gravar_json, tc

ap = argparse.ArgumentParser()
ap.add_argument("--src", help="pasta dos originais (para ler duração/resolução)")
ap.add_argument("--media-dir", default="/MIDIA/05. CASO DE EMERGÊNCIA",
                help="caminho dos originais NO SEU MAC (o Premiere relinka por nome se não achar)")
ap.add_argument("--saida", default=str(PROJ / "sequencia.xml")); a = ap.parse_args()
P = ler_json(PROJ / "plano.json")

# ---- metadados das mídias ----
cache = ANALISE / "midia.json"
meta = ler_json(cache) if cache.exists() else {}
nomes = {v["clipe"] for v in P["video"]} | {x["clipe"] for x in P["audio"]} | {MUSICA}
for n in sorted(nomes):
    if n in meta: continue
    p = (PROJ / n) if n == "abertura_tensao.mov" else (Path(a.src) / n if a.src else None)
    if p is None: raise SystemExit(f"Sem metadados de {n}: rode com --src")
    i = ffprobe(p); v = next((s for s in i["streams"] if s["codec_type"] == "video"), None)
    au = next((s for s in i["streams"] if s["codec_type"] == "audio"), None)
    w, h = (v["width"], v["height"]) if v else (0, 0)
    if v and abs(rotacao(i)) in (90, 270): w, h = h, w
    meta[n] = {"dur_q": int(round(Fraction(i["format"]["duration"]) * FPS)) if v is None else int(v.get("nb_frames") or round(float(i["format"]["duration"]) * float(FPS))),
               "dur_s": float(i["format"]["duration"]), "w": w, "h": h, "video": v is not None,
               "canais": au["channels"] if au else 0, "sr": int(au["sample_rate"]) if au else 0}
gravar_json(cache, meta)


def sub(p, tag, text=None, **at):
    e = ET.SubElement(p, tag, {k: str(v) for k, v in at.items()})
    if text is not None: e.text = str(text)
    return e


def rate(p):
    r = sub(p, "rate"); sub(r, "timebase", 24); sub(r, "ntsc", "TRUE"); return r


def pathurl(nome):
    base = a.media_dir.rstrip("/")
    return "file://localhost" + quote(f"{base}/{nome}", safe="/")


feitos = set()
def arquivo(p, nome):
    fid = "file-" + Path(nome).stem.replace(" ", "_").replace("(", "").replace(")", "")[:40]
    f = sub(p, "file", id=fid)
    if fid in feitos: return
    feitos.add(fid); m = meta[nome]
    sub(f, "name", nome); sub(f, "pathurl", pathurl(nome)); rate(f); sub(f, "duration", m["dur_q"])
    md = sub(f, "media")
    if m["video"]:
        sc = sub(sub(md, "video"), "samplecharacteristics"); rate(sc)
        sub(sc, "width", m["w"]); sub(sc, "height", m["h"]); sub(sc, "anamorphic", "FALSE")
        sub(sc, "pixelaspectratio", "square"); sub(sc, "fielddominance", "none")
    if m["canais"]:
        ad = sub(md, "audio"); sc = sub(ad, "samplecharacteristics"); sub(sc, "depth", 16); sub(sc, "samplerate", m["sr"])
        sub(ad, "channelcount", m["canais"])


def motion(p, escala_pct, ancora_y, zoom):
    # posição para "zoom ancorado": centro da imagem desce/sobe conforme a âncora vertical
    dy = (ancora_y * SEQ_H + (0.5 - ancora_y) * SEQ_H * zoom) - SEQ_H / 2
    e = sub(sub(p, "filter"), "effect"); sub(e, "name", "Basic Motion"); sub(e, "effectid", "basic")
    sub(e, "effectcategory", "motion"); sub(e, "effecttype", "motion"); sub(e, "mediatype", "video")
    pr = sub(e, "parameter", authoringApp="PremierePro"); sub(pr, "parameterid", "scale"); sub(pr, "name", "Scale")
    sub(pr, "valuemin", 0); sub(pr, "valuemax", 1000); sub(pr, "value", round(escala_pct, 3))
    pr = sub(e, "parameter", authoringApp="PremierePro"); sub(pr, "parameterid", "center"); sub(pr, "name", "Center")
    v = sub(pr, "value"); sub(v, "horiz", 0); sub(v, "vert", round(dy / SEQ_H, 5))
    return round(dy, 1)


def niveis(p, kfs, in_q):
    e = sub(sub(p, "filter"), "effect"); sub(e, "name", "Audio Levels"); sub(e, "effectid", "audiolevels")
    sub(e, "effectcategory", "audiolevels"); sub(e, "effecttype", "audiolevels"); sub(e, "mediatype", "audio")
    pr = sub(e, "parameter"); sub(pr, "parameterid", "level"); sub(pr, "name", "Level")
    sub(pr, "valuemin", 0); sub(pr, "valuemax", 3.98109); sub(pr, "value", kfs[0]["ganho"] if kfs else 1)
    for k in kfs:
        kf = sub(pr, "keyframe"); sub(kf, "when", in_q + k["quadro"]); sub(kf, "value", k["ganho"])


xm = ET.Element("xmeml", version="4")
seq = sub(xm, "sequence", id="sequence-1")
total = P["sequencia"]["duracao_quadros"]
sub(seq, "name", "CASO DE EMERGENCIA"); sub(seq, "duration", total); rate(seq)
t = sub(seq, "timecode"); rate(t); sub(t, "string", "00:00:00:00"); sub(t, "frame", 0); sub(t, "displayformat", "NDF")
media = sub(seq, "media")
vid = sub(media, "video"); fmt = sub(sub(vid, "format"), "samplecharacteristics"); rate(fmt)
sub(fmt, "width", SEQ_W); sub(fmt, "height", SEQ_H); sub(fmt, "anamorphic", "FALSE")
sub(fmt, "pixelaspectratio", "square"); sub(fmt, "fielddominance", "none")
v1 = sub(vid, "track")
posicoes = {}
n = 0
for v in P["video"]:
    n += 1; m = meta[v["clipe"]]
    ci = sub(v1, "clipitem", id=f"clipitem-{n}")
    sub(ci, "name", f"{v['id']} cena {v['cena']} - {v['clipe']}"); sub(ci, "enabled", "TRUE")
    sub(ci, "duration", m["dur_q"]); rate(ci)
    for k in ("start", "end", "in", "out"):
        sub(ci, k, v[{"start": "tl_in", "end": "tl_out", "in": "src_in", "out": "src_out"}[k]])
    arquivo(ci, v["clipe"])
    base = 100.0 * SEQ_W / m["w"]                      # 4K vertical -> 50%; abertura 1080 -> 100%
    posicoes[v["id"]] = (round(base * v["escala"], 2), motion(ci, base * v["escala"], v["ancora_y"], v["escala"]))
fq = P["fusoes"]["fim_para_preto_quadros"]
tr = sub(v1, "transitionitem"); sub(tr, "start", total - fq); sub(tr, "end", total); sub(tr, "alignment", "end-black"); rate(tr)
ef = sub(tr, "effect"); sub(ef, "name", "Cross Dissolve"); sub(ef, "effectid", "Cross Dissolve")
sub(ef, "effectcategory", "Dissolve"); sub(ef, "effecttype", "transition"); sub(ef, "mediatype", "video")
sub(ef, "wipecode", 0); sub(ef, "wipeaccuracy", 100); sub(ef, "startratio", 0); sub(ef, "endratio", 1); sub(ef, "reverse", "FALSE")
sub(v1, "enabled", "TRUE"); sub(v1, "locked", "FALSE")

aud = sub(media, "audio"); sub(aud, "numOutputChannels", 2)
af = sub(sub(aud, "format"), "samplecharacteristics"); sub(af, "depth", 16); sub(af, "samplerate", 48000)
def trilha_audio(itens, canal, nome_trilha, kfs=None):
    tr = sub(aud, "track")
    global n
    for x in itens:
        n += 1; m = meta[x["clipe"]]
        ci = sub(tr, "clipitem", id=f"clipitem-{n}")
        sub(ci, "name", f"{nome_trilha} - {x['clipe']}"); sub(ci, "enabled", "TRUE"); sub(ci, "duration", m["dur_q"]); rate(ci)
        sub(ci, "start", x["tl_in"]); sub(ci, "end", x["tl_out"]); sub(ci, "in", x["src_in"]); sub(ci, "out", x["src_out"])
        arquivo(ci, x["clipe"])
        st = sub(ci, "sourcetrack"); sub(st, "mediatype", "audio"); sub(st, "trackindex", canal)
        if kfs is not None: niveis(ci, kfs, x["src_in"])
    sub(tr, "enabled", "TRUE"); sub(tr, "locked", "FALSE")
for c in (1, 2): trilha_audio(P["audio"], c, f"LOCUCAO {'L' if c == 1 else 'R'}")
mu = P["musica"]; item_m = [{"clipe": MUSICA, "tl_in": mu["tl_in"], "tl_out": mu["tl_out"], "src_in": mu["src_in"], "src_out": mu["src_out"]}]
for c in (1, 2): trilha_audio(item_m, c, f"MUSICA {'L' if c == 1 else 'R'}", mu["niveis"])
trilha_audio([], 1, "SFX")                              # A5 reservada p/ o som de telefone
for mk in P["marcadores"]:
    e = sub(seq, "marker"); sub(e, "name", mk["nome"]); sub(e, "comment", mk["nota"]); sub(e, "in", mk["quadro"]); sub(e, "out", -1)

ET.indent(xm)
Path(a.saida).write_text('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n' + ET.tostring(xm, encoding="unicode") + "\n", encoding="utf-8")
gravar_json(ANALISE / "posicoes_premiere.json", {k: {"escala_pct": s, "deslocamento_y_px": d, "posicao_premiere": [SEQ_W/2, SEQ_H/2 + d]} for k, (s, d) in posicoes.items()})
print("ok:", a.saida, f"| {n} clipitems | {tc(total)}")
