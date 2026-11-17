"""Gera sequencia.xml (Final Cut Pro 7 XML / xmeml v4) para importar no Premiere.
Aponta para os ARQUIVOS ORIGINAIS pelo nome, dentro de --base (pasta onde eles estarão na sua máquina).
Uso: python3 -I gerar_xml.py <plano.json> <saida.xml> [--base /pasta] [--sobre ID=arquivo.png ...]

Recursos (todos opcionais, lidos do plano.json):
- V1: planos (corte seco, Cross Dissolve, Fade to Black no fim)
- V2: sobreposições (imagens, ex.: placeholder de print)
- A1/A2: música (estéreo). Com ducking, a música vira 3 trechos (normal / mais baixa / normal) com Cross Fade entre eles
- A3: locução (se houver)
- Escala automática (config.escala_auto) para preencher a largura da sequência; rotação por plano ou padrão
- Timebase dos clipitems = timebase da sequência (in/out em quadros da sequência); <file> com fps e duração nativos
"""
import sys, json, subprocess, os, urllib.parse
import xml.etree.ElementTree as ET

args = sys.argv[1:]
base = args[args.index("--base") + 1] if "--base" in args else "/Terral_material"
imgs = dict(x.split("=", 1) for i, x in enumerate(args) if i > 0 and args[i - 1] == "--sobre")
plano_p, out = args[0], args[1]
P = json.load(open(plano_p)); cfg = P["config"]; ps = P["planos"]
FPS = cfg["fps_num"] / cfg["fps_den"]; TB = round(FPS); NTSC = "TRUE" if cfg["fps_den"] == 1001 else "FALSE"
W, H = cfg["largura"], cfg["altura"]; total = cfg["duracao_final_f"]
DIRS = cfg.get("originais_dirs") or [cfg["originais_dir"]]
mus = cfg["musica"]

def achar(nome):
    for d in DIRS + [os.path.dirname(os.path.abspath(out))]:
        if os.path.exists(os.path.join(d, nome)): return os.path.join(d, nome)
    for v in imgs.values():
        if os.path.basename(v) == nome: return v
    raise FileNotFoundError(nome)

def probe(nome):
    path = achar(nome)
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]))
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    info = {"dur": float(j["format"].get("duration", 0) or 0), "video": v is not None, "audio": a is not None,
            "canais": int(a["channels"]) if a else 0}
    if v:
        num, den = map(int, v.get("r_frame_rate", "0/1").split("/"))
        info.update(w=int(v["width"]), h=int(v["height"]), fps=num / den if den else 0, fden=den,
                    rot=next((int(sd.get("rotation", 0)) for sd in v.get("side_data_list", []) if "rotation" in sd), 0),
                    still=info["dur"] == 0 or v.get("codec_name") in ("png", "mjpeg"))
    return info

def sub(p, tag, text=None, **attr):
    e = ET.SubElement(p, tag, attr)
    if text is not None: e.text = str(text)
    return e
def rate(p, fps=None, den=None):
    fps = fps or FPS; den = den or cfg["fps_den"]
    r = sub(p, "rate"); sub(r, "timebase", round(fps)); sub(r, "ntsc", "TRUE" if den == 1001 else "FALSE"); return r
def pathurl(nome):
    return "file://localhost" + urllib.parse.quote(os.path.join(base, nome))

files_done = {}
def file_el(parent, nome):
    fid = "file-" + "".join(c if c.isalnum() else "_" for c in nome)
    if fid in files_done:
        sub(parent, "file", id=fid); return files_done[fid]
    info = probe(nome); files_done[fid] = info
    f = sub(parent, "file", id=fid); sub(f, "name", nome); sub(f, "pathurl", pathurl(nome))
    if info["video"] and not info.get("still"):
        rate(f, info["fps"], info["fden"]); sub(f, "duration", int(info["dur"] * info["fps"]))
    else:
        rate(f); sub(f, "duration", int(info["dur"] * FPS) if info["dur"] else 0)
    tcx = sub(f, "timecode"); rate(tcx); sub(tcx, "string", "00:00:00:00"); sub(tcx, "frame", 0); sub(tcx, "displayformat", "NDF")
    m = sub(f, "media")
    if info["video"]:
        v = sub(m, "video"); sc = sub(v, "samplecharacteristics"); rate(sc, info.get("fps") or FPS, info.get("fden") or cfg["fps_den"])
        sub(sc, "width", info["w"]); sub(sc, "height", info["h"]); sub(sc, "anamorphic", "FALSE")
        sub(sc, "pixelaspectratio", "square"); sub(sc, "fielddominance", "none")
    if info["audio"]:
        a = sub(m, "audio"); sc = sub(a, "samplecharacteristics"); sub(sc, "depth", 16); sub(sc, "samplerate", 48000)
        sub(a, "channelcount", info["canais"])
    return info

def escala(info, rot_aplicada):
    if not cfg.get("escala_auto"): return 100
    w, h = info["w"], info["h"]
    if (abs(info.get("rot", 0)) % 180 == 90) != (abs(rot_aplicada) % 180 == 90): w, h = h, w
    return round(100 * max(W / w, H / h), 3)

def motion_filter(ci, rot, scale):
    fl = sub(ci, "filter"); ef = sub(fl, "effect")
    sub(ef, "name", "Basic Motion"); sub(ef, "effectid", "basic"); sub(ef, "effectcategory", "motion")
    sub(ef, "effecttype", "motion"); sub(ef, "mediatype", "video")
    for pid, nm, val, mn, mx in [("scale", "Scale", scale, 0, 1000), ("rotation", "Rotation", rot, -8640, 8640)]:
        pr = sub(ef, "parameter", authoringApp="PremierePro"); sub(pr, "parameterid", pid); sub(pr, "name", nm)
        sub(pr, "valuemin", mn); sub(pr, "valuemax", mx); sub(pr, "value", val)
    pr = sub(ef, "parameter"); sub(pr, "parameterid", "center"); sub(pr, "name", "Center")
    v = sub(pr, "value"); sub(v, "horiz", 0); sub(v, "vert", 0)

def level_filter(ci, db):
    fl = sub(ci, "filter"); ef = sub(fl, "effect")
    sub(ef, "name", "Audio Levels"); sub(ef, "effectid", "audiolevels"); sub(ef, "effectcategory", "audiolevels")
    sub(ef, "effecttype", "audiolevels"); sub(ef, "mediatype", "audio")
    pr = sub(ef, "parameter"); sub(pr, "parameterid", "level"); sub(pr, "name", "Level")
    sub(pr, "valuemin", 0); sub(pr, "valuemax", 3.98109); sub(pr, "value", round(10 ** (db / 20), 5))

def transition(track, name, eid, start, end, align, media="video", cat="Dissolve"):
    t = sub(track, "transitionitem"); sub(t, "start", start); sub(t, "end", end); sub(t, "alignment", align); rate(t)
    ef = sub(t, "effect"); sub(ef, "name", name); sub(ef, "effectid", eid)
    sub(ef, "effectcategory", cat); sub(ef, "effecttype", "transition"); sub(ef, "mediatype", media)
    sub(ef, "wipecode", 0); sub(ef, "wipeaccuracy", 100); sub(ef, "startratio", 0); sub(ef, "endratio", 1); sub(ef, "reverse", "FALSE")

def clip_video(track, cid, nome, start, end, src_in, rot, marker=None):
    ci = sub(track, "clipitem", id=cid); sub(ci, "name", nome); sub(ci, "enabled", "TRUE")
    holder = ET.Element("tmp"); info = probe(nome)
    sub(ci, "duration", int(info["dur"] * FPS) if info["dur"] else end - start + src_in); rate(ci)
    sub(ci, "start", start); sub(ci, "end", end); sub(ci, "in", src_in); sub(ci, "out", src_in + end - start)
    file_el(ci, nome)
    motion_filter(ci, rot, escala(info, rot) if not info.get("still") else 100)
    st = sub(ci, "sourcetrack"); sub(st, "mediatype", "video"); sub(st, "trackindex", 1)
    if marker:
        mk = sub(ci, "marker"); sub(mk, "name", marker[0]); sub(mk, "comment", marker[1]); sub(mk, "in", src_in); sub(mk, "out", -1)
    return ci

def clip_audio(track, cid, nome, start, end, src_in, trackindex, db=None, links=()):
    ci = sub(track, "clipitem", id=cid); sub(ci, "name", nome); sub(ci, "enabled", "TRUE")
    info = probe(nome); sub(ci, "duration", int(info["dur"] * FPS)); rate(ci)
    sub(ci, "start", start); sub(ci, "end", end); sub(ci, "in", src_in); sub(ci, "out", src_in + end - start)
    file_el(ci, nome)
    st = sub(ci, "sourcetrack"); sub(st, "mediatype", "audio"); sub(st, "trackindex", trackindex)
    if db is not None: level_filter(ci, db)
    for k, (lid, ti) in enumerate(links, 1):
        lk = sub(ci, "link"); sub(lk, "linkclipref", lid); sub(lk, "mediatype", "audio"); sub(lk, "trackindex", ti); sub(lk, "clipindex", k)
    return ci

root = ET.Element("xmeml", version="4")
seq = sub(root, "sequence", id="sequence-1")
sub(seq, "name", cfg.get("nome_sequencia", "Sequencia")); sub(seq, "duration", total); rate(seq)
tcx = sub(seq, "timecode"); rate(tcx); sub(tcx, "string", "00:00:00:00"); sub(tcx, "frame", 0); sub(tcx, "displayformat", "NDF")
media = sub(seq, "media")
video = sub(media, "video"); fm = sub(video, "format"); sc = sub(fm, "samplecharacteristics"); rate(sc)
sub(sc, "width", W); sub(sc, "height", H); sub(sc, "anamorphic", "FALSE"); sub(sc, "pixelaspectratio", "square"); sub(sc, "fielddominance", "none")

# V1
vt = sub(video, "track")
for i, p in enumerate(ps):
    if i > 0:
        t = ps[i - 1].get("transicao_saida", {})
        if t.get("tipo") == "Cross Dissolve":
            c = p["timeline_in_f"]; d = t["frames"]
            transition(vt, "Cross Dissolve", "Cross Dissolve", c - d // 2, c + d - d // 2, "center")
    clip_video(vt, f"clipitem-{p['id']}", p["clipe"], p["timeline_in_f"], p["timeline_out_f"], p["fonte_in_f"],
               p.get("rotacao_graus", cfg["rotacao_fonte_graus"]), (f"Cena {p['cena']}", p["motivo"]))
lt = ps[-1].get("transicao_saida", {})
if lt.get("tipo") == "Fade to Black":
    transition(vt, "Cross Dissolve", "Cross Dissolve", total - lt["frames"], total, "end-black")
# V2: sobreposições
sobre = P.get("sobreposicoes", [])
if sobre:
    v2 = sub(video, "track")
    for s in sobre:
        nome = os.path.basename(imgs.get(s["id"], s["arquivo"]))
        clip_video(v2, f"clipitem-sobre-{s['id']}", nome, s["timeline_in_f"], s["timeline_out_f"], 0, 0,
                   (s["id"], s.get("instrucao", "")))

audio = sub(media, "audio"); sub(audio, "numOutputChannels", 2)
af = sub(audio, "format"); sc = sub(af, "samplecharacteristics"); sub(sc, "depth", 16); sub(sc, "samplerate", 48000)
m_in = int(round(mus["inicio_s"] * FPS)); fade = int(round(mus["fade_out_s"] * FPS)); xf = 12
d = P.get("ducking")
segs = [(0, total, 0)] if not d else [(0, d["de_f"], 0), (d["de_f"], d["ate_f"], d["ganho_db"]), (d["ate_f"], total, 0)]
for ch in (1, 2):
    at = sub(audio, "track")
    for k, (a, b, db) in enumerate(segs):
        if k > 0:
            transition(at, "Cross Fade (+3dB)", "KGAudioTransCrossFade3dB", a - xf // 2, a + xf - xf // 2, "center", media="audio", cat="")
        clip_audio(at, f"clipitem-musica-{k}-{ch}", mus["arquivo"], a, b, m_in + a, ch, db,
                   links=[(f"clipitem-musica-{k}-1", 1), (f"clipitem-musica-{k}-2", 2)])
    transition(at, "Cross Fade (+3dB)", "KGAudioTransCrossFade3dB", total - fade, total, "end-black", media="audio", cat="")
    sub(at, "outputchannelindex", ch)
loc = P.get("locucao")
if loc:
    at = sub(audio, "track")
    clip_audio(at, "clipitem-locucao", loc["arquivo"], loc["timeline_in_f"], min(loc["timeline_out_f"], total), loc["fonte_in_f"], 1, 0)

ET.indent(root)
with open(out, "wb") as fh:
    fh.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
    fh.write(ET.tostring(root, encoding="utf-8"))
print("ok", out, "| base dos originais:", base)
