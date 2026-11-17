"""Gera sequencia.xml (Final Cut Pro 7 XML / xmeml v4) para importar no Premiere.
Aponta para os ARQUIVOS ORIGINAIS pelo nome, dentro de --base (pasta onde eles estarão na sua máquina).
Uso: python3 -I gerar_xml.py <plano.json> <saida.xml> [--base /caminho/da/pasta/do/material]
"""
import sys, json, subprocess, os, urllib.parse
import xml.etree.ElementTree as ET

args = sys.argv[1:]
base = args[args.index("--base") + 1] if "--base" in args else "/Terral_material"
plano_p, out = args[0], args[1]
P = json.load(open(plano_p)); cfg = P["config"]; ps = P["planos"]
TB, W, H = round(cfg["fps_num"] / cfg["fps_den"]), cfg["largura"], cfg["altura"]
FPS = cfg["fps_num"] / cfg["fps_den"]; total = cfg["duracao_final_f"]
orig = cfg["originais_dir"]; mus = cfg["musica"]

def sub(p, tag, text=None, **attr):
    e = ET.SubElement(p, tag, attr)
    if text is not None: e.text = str(text)
    return e
NTSC = "TRUE" if cfg["fps_den"] == 1001 else "FALSE"
def rate(p):
    r = sub(p, "rate"); sub(r, "timebase", TB); sub(r, "ntsc", NTSC); return r
def dur_frames(path):
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                       "-of", "csv=p=0", path]).decode())
    return int(d * FPS)
def pathurl(name):
    return "file://localhost" + urllib.parse.quote(os.path.join(base, name))

files_done = {}
def file_el(parent, name, video=True):
    fid = "file-" + name.replace(" ", "_").replace("(", "").replace(")", "")
    if fid in files_done:
        sub(parent, "file", id=fid); return fid
    f = sub(parent, "file", id=fid); files_done[fid] = 1
    sub(f, "name", name); sub(f, "pathurl", pathurl(name)); rate(f)
    sub(f, "duration", dur_frames(os.path.join(orig, name)))
    tc = sub(f, "timecode"); rate(tc); sub(tc, "string", "00:00:00:00"); sub(tc, "frame", 0)
    sub(tc, "displayformat", "NDF")
    m = sub(f, "media")
    if video:
        v = sub(m, "video"); sc = sub(v, "samplecharacteristics"); rate(sc)
        w, h = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height", "-of", "csv=p=0", os.path.join(orig, name)]).decode().strip().split(",")
        sub(sc, "width", w); sub(sc, "height", h); sub(sc, "anamorphic", "FALSE")
        sub(sc, "pixelaspectratio", "square"); sub(sc, "fielddominance", "none")
    a = sub(m, "audio"); sc = sub(a, "samplecharacteristics"); sub(sc, "depth", 16); sub(sc, "samplerate", 48000)
    sub(a, "channelcount", 2)
    return fid

def motion_filter(ci, rot):
    fl = sub(ci, "filter"); ef = sub(fl, "effect")
    sub(ef, "name", "Basic Motion"); sub(ef, "effectid", "basic"); sub(ef, "effectcategory", "motion")
    sub(ef, "effecttype", "motion"); sub(ef, "mediatype", "video")
    for pid, nm, val, mn, mx in [("scale", "Scale", 100, 0, 1000), ("rotation", "Rotation", rot, -8640, 8640)]:
        pr = sub(ef, "parameter", authoringApp="PremierePro"); sub(pr, "parameterid", pid); sub(pr, "name", nm)
        sub(pr, "valuemin", mn); sub(pr, "valuemax", mx); sub(pr, "value", val)
    pr = sub(ef, "parameter"); sub(pr, "parameterid", "center"); sub(pr, "name", "Center")
    v = sub(pr, "value"); sub(v, "horiz", 0); sub(v, "vert", 0)

def transition(track, name, eid, start, end, align, media="video", cat="Dissolve"):
    t = sub(track, "transitionitem"); sub(t, "start", start); sub(t, "end", end)
    sub(t, "alignment", align); rate(t)
    ef = sub(t, "effect"); sub(ef, "name", name); sub(ef, "effectid", eid)
    sub(ef, "effectcategory", cat); sub(ef, "effecttype", "transition"); sub(ef, "mediatype", media)
    sub(ef, "wipecode", 0); sub(ef, "wipeaccuracy", 100); sub(ef, "startratio", 0); sub(ef, "endratio", 1)
    sub(ef, "reverse", "FALSE")

root = ET.Element("xmeml", version="4")
seq = sub(root, "sequence", id="sequence-1")
sub(seq, "name", cfg.get("nome_sequencia", "Sequencia")); sub(seq, "duration", total); rate(seq)
tc = sub(seq, "timecode"); rate(tc); sub(tc, "string", "00:00:00:00"); sub(tc, "frame", 0); sub(tc, "displayformat", "NDF")
media = sub(seq, "media")
video = sub(media, "video"); fm = sub(video, "format"); sc = sub(fm, "samplecharacteristics"); rate(sc)
sub(sc, "width", W); sub(sc, "height", H); sub(sc, "anamorphic", "FALSE")
sub(sc, "pixelaspectratio", "square"); sub(sc, "fielddominance", "none")
vt = sub(video, "track")
for i, p in enumerate(ps):
    if i > 0:
        t = ps[i-1].get("transicao_saida", {})
        if t.get("tipo") == "Cross Dissolve":
            c = p["timeline_in_f"]; d = t["frames"]
            transition(vt, "Cross Dissolve", "Cross Dissolve", c - d//2, c + d - d//2, "center")
    ci = sub(vt, "clipitem", id=f"clipitem-{p['id']}")
    sub(ci, "name", f"Cena{p['cena']}_{p['id']}_{p['clipe']}"); sub(ci, "enabled", "TRUE")
    sub(ci, "duration", dur_frames(os.path.join(orig, p["clipe"]))); rate(ci)
    sub(ci, "start", p["timeline_in_f"]); sub(ci, "end", p["timeline_out_f"])
    sub(ci, "in", p["fonte_in_f"]); sub(ci, "out", p["fonte_out_f"])
    file_el(ci, p["clipe"])
    motion_filter(ci, p.get("rotacao_graus", cfg["rotacao_fonte_graus"]))
    st = sub(ci, "sourcetrack"); sub(st, "mediatype", "video"); sub(st, "trackindex", 1)
    sub(ci, "comments")
    mk = sub(ci, "marker"); sub(mk, "name", f"Cena {p['cena']}"); sub(mk, "comment", p["motivo"])
    sub(mk, "in", p["fonte_in_f"]); sub(mk, "out", -1)
lt = ps[-1].get("transicao_saida", {})
if lt.get("tipo") == "Fade to Black":
    transition(vt, "Cross Dissolve", "Cross Dissolve", total - lt["frames"], total, "end-black")

audio = sub(media, "audio"); sub(audio, "numOutputChannels", 2)
af = sub(audio, "format"); sc = sub(af, "samplecharacteristics"); sub(sc, "depth", 16); sub(sc, "samplerate", 48000)
m_in = int(round(mus["inicio_s"] * FPS)); fade = int(round(mus["fade_out_s"] * FPS))
for ch in (1, 2):
    at = sub(audio, "track")
    ci = sub(at, "clipitem", id=f"clipitem-musica-{ch}")
    sub(ci, "name", mus["arquivo"]); sub(ci, "enabled", "TRUE")
    sub(ci, "duration", dur_frames(os.path.join(orig, mus["arquivo"]))); rate(ci)
    sub(ci, "start", 0); sub(ci, "end", total); sub(ci, "in", m_in); sub(ci, "out", m_in + total)
    file_el(ci, mus["arquivo"], video=False)
    st = sub(ci, "sourcetrack"); sub(st, "mediatype", "audio"); sub(st, "trackindex", ch)
    for o in (1, 2):
        lk = sub(ci, "link"); sub(lk, "linkclipref", f"clipitem-musica-{o}"); sub(lk, "mediatype", "audio")
        sub(lk, "trackindex", o); sub(lk, "clipindex", 1)
    transition(at, "Cross Fade (+3dB)", "KGAudioTransCrossFade3dB", total - fade, total, "end-black",
               media="audio", cat="")
    sub(at, "outputchannelindex", ch)

ET.indent(root)
with open(out, "wb") as fh:
    fh.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
    fh.write(ET.tostring(root, encoding="utf-8"))
print("ok", out, "| base dos originais:", base)
