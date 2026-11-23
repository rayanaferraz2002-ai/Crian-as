"""Gera proxies_premiere.xml: só os vídeos (proxies) numa pasta (bin) do Premiere, SEM sequência/edição.
Uso: python3 10_gerar_xml_proxies.py [--pasta ../proxies] [--media-dir "/Users/voce/.../proxies"]"""
import argparse, xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote
from comum import PROJ, ffprobe

ap = argparse.ArgumentParser()
ap.add_argument("--pasta", default=str(PROJ / "proxies"), help="pasta com os proxies (para ler duração/formato)")
ap.add_argument("--media-dir", default=None, help="caminho dos proxies NO SEU MAC (padrão: a própria --pasta)")
ap.add_argument("--saida", default=str(PROJ / "proxies_premiere.xml")); a = ap.parse_args()
pasta = Path(a.pasta).resolve(); base = (a.media_dir or str(pasta)).rstrip("/")


def sub(p, tag, text=None, **at):
    e = ET.SubElement(p, tag, {k: str(v) for k, v in at.items()})
    if text is not None: e.text = str(text)
    return e


def rate(p, fps):
    ntsc = fps.denominator == 1001
    r = sub(p, "rate"); sub(r, "timebase", round(fps * (Fraction(1001, 1000) if ntsc else 1))); sub(r, "ntsc", "TRUE" if ntsc else "FALSE")


xm = ET.Element("xmeml", version="4")
binn = sub(xm, "bin"); sub(binn, "name", "PROXIES - CASO DE EMERGENCIA"); kids = sub(binn, "children")
n = 0
for f in sorted(pasta.glob("*.mov")):
    i = ffprobe(f); v = next(s for s in i["streams"] if s["codec_type"] == "video")
    au = next((s for s in i["streams"] if s["codec_type"] == "audio"), None)
    fps = Fraction(v["r_frame_rate"]); dur = int(v.get("nb_frames") or round(float(i["format"]["duration"]) * fps))
    clip = sub(kids, "clip", id=f"masterclip-{f.stem}")
    sub(clip, "name", f.name); sub(clip, "duration", dur); rate(clip, fps)
    media = sub(clip, "media")
    n += 1; ci = sub(sub(media, "video"), "track"); ci = sub(ci, "clipitem", id=f"clipitem-{n}")
    sub(ci, "name", f.name); sub(ci, "duration", dur); rate(ci, fps)
    fe = sub(ci, "file", id=f"file-{f.stem}")
    sub(fe, "name", f.name); sub(fe, "pathurl", "file://localhost" + quote(f"{base}/{f.name}", safe="/"))
    rate(fe, fps); sub(fe, "duration", dur)
    fm = sub(fe, "media"); sc = sub(sub(fm, "video"), "samplecharacteristics"); rate(sc, fps)
    sub(sc, "width", v["width"]); sub(sc, "height", v["height"]); sub(sc, "anamorphic", "FALSE")
    sub(sc, "pixelaspectratio", "square"); sub(sc, "fielddominance", "none")
    if au:
        fa = sub(fm, "audio"); s2 = sub(fa, "samplecharacteristics"); sub(s2, "depth", 16); sub(s2, "samplerate", au["sample_rate"])
        sub(fa, "channelcount", au["channels"])
        aud = sub(media, "audio")
        for c in range(1, au["channels"] + 1):
            n += 1; ca = sub(sub(aud, "track"), "clipitem", id=f"clipitem-{n}")
            sub(ca, "name", f.name); sub(ca, "duration", dur); rate(ca, fps); sub(ca, "file", id=f"file-{f.stem}")
            st = sub(ca, "sourcetrack"); sub(st, "mediatype", "audio"); sub(st, "trackindex", c)
    print(f"{f.name}: {v['width']}x{v['height']} {float(fps):.3f} fps, {dur} quadros, {au['channels'] if au else 0} canais")
ET.indent(xm)
Path(a.saida).write_text('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n' + ET.tostring(xm, encoding="unicode") + "\n", encoding="utf-8")
# validação básica
r = ET.fromstring(Path(a.saida).read_text(encoding="utf-8").split("\n", 2)[2])
assert r.find("sequence") is None and len(r.findall("bin/children/clip")) == len(list(pasta.glob("*.mov")))
assert all(f.find("pathurl") is not None for f in r.iter("file") if f.find("name") is not None)
print("ok:", a.saida, "| sem sequência |", len(r.findall("bin/children/clip")), "clipes")
