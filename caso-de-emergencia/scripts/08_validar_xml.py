"""Valida sequencia.xml: XML bem-formado, regras do xmeml, coerência com plano.json e
leitura independente com OpenTimelineIO (adaptador FCP7). Uso: python3 08_validar_xml.py"""
import sys, xml.etree.ElementTree as ET
from comum import PROJ, ler_json

P = ler_json(PROJ / "plano.json"); erros = []; ok = []
arq = PROJ / "sequencia.xml"
raw = arq.read_text(encoding="utf-8")
assert raw.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>'), "cabeçalho/DOCTYPE"
root = ET.fromstring(raw.split("\n", 2)[2]); ok.append("XML bem-formado + DOCTYPE xmeml")
seq = root.find("sequence")
fmt = seq.find("media/video/format/samplecharacteristics")
if (fmt.findtext("width"), fmt.findtext("height"), fmt.findtext("rate/timebase"), fmt.findtext("rate/ntsc")) != ("1080", "1920", "24", "TRUE"):
    erros.append("formato da sequência difere de 1080x1920 23,976")
else: ok.append("sequência 1080x1920 @ 23,976 (24 NTSC)")
total = int(seq.findtext("duration"))
if total != P["sequencia"]["duracao_quadros"]: erros.append("duração difere do plano")
defs = {}
for f in root.iter("file"):
    if f.find("pathurl") is not None: defs[f.get("id")] = f
for ti, tr in enumerate(seq.findall("media/*/track")):
    fim = 0
    for ci in tr.findall("clipitem"):
        s, e, i, o, d = (int(ci.findtext(k)) for k in ("start", "end", "in", "out", "duration"))
        nome = ci.findtext("name")
        if not (s < e and i < o): erros.append(f"{nome}: start/end ou in/out inválidos")
        if o - i != e - s: erros.append(f"{nome}: duração origem != duração na linha do tempo")
        if o > d: erros.append(f"{nome}: out {o} além da mídia {d}")
        if s < fim: erros.append(f"{nome}: sobreposição na trilha {ti}")
        fim = e
        if ci.find("file").get("id") not in defs: erros.append(f"{nome}: file sem definição")
        if e > total: erros.append(f"{nome}: passa do fim da sequência")
ok.append(f"{sum(1 for _ in root.iter('clipitem'))} clipitems checados (in/out, durações, sobreposição, arquivos)")
# coerência com o plano
v1 = seq.findall("media/video/track")[0].findall("clipitem")
for ci, v in zip(v1, P["video"]):
    if (int(ci.findtext("start")), int(ci.findtext("end")), int(ci.findtext("in")), int(ci.findtext("out"))) != (v["tl_in"], v["tl_out"], v["src_in"], v["src_out"]):
        erros.append(f"{v['id']}: difere do plano")
ok.append("V1 idêntica ao plano.json")
nomes = {f.findtext("name") for f in defs.values()}
if any("proxy" in n.lower() or n.endswith("_720.mp4") for n in nomes): erros.append("XML aponta para proxy")
ok.append("aponta para originais: " + ", ".join(sorted(nomes)))
# leitura independente
try:
    import opentimelineio as otio
    tl = otio.adapters.read_from_file(str(arq), adapter_name="fcp_xml")
    vt = [t for t in tl.tracks if t.kind == otio.schema.TrackKind.Video][0]
    clips = [c for c in vt if isinstance(c, otio.schema.Clip)]
    dur = tl.duration().to_frames()
    if len(clips) != len(P["video"]): erros.append(f"OTIO: {len(clips)} clipes de vídeo, esperado {len(P['video'])}")
    ok.append(f"OpenTimelineIO leu: {len(tl.tracks)} trilhas, {len(clips)} clipes V1, {dur} quadros")
except ImportError:
    ok.append("(OpenTimelineIO não instalado: leitura independente pulada)")
for x in ok: print("OK  ", x)
for x in erros: print("ERRO", x)
sys.exit(1 if erros else 0)
