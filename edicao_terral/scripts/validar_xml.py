"""Valida sequencia.xml contra o plano.json: estrutura xmeml, continuidade, limites da mídia, transições,
e leitura independente via OpenTimelineIO (se instalado).
Uso: python3 -I validar_xml.py <sequencia.xml> <plano.json>
"""
import sys, json
import xml.etree.ElementTree as ET
xml_p, plano_p = sys.argv[1:3]
P = json.load(open(plano_p)); cfg = P["config"]
root = ET.parse(xml_p).getroot(); erros = []
def chk(c, msg): (None if c else erros.append(msg))
chk(root.tag == "xmeml" and root.get("version") == "4", "raiz xmeml v4")
seq = root.find("sequence"); sc = seq.find("media/video/format/samplecharacteristics")
chk(int(sc.findtext("width")) == cfg["largura"] and int(sc.findtext("height")) == cfg["altura"], "resolução")
chk(seq.findtext("rate/timebase") == "24" and seq.findtext("rate/ntsc") == "TRUE", "fps 23,976")
files = {f.get("id"): f for f in root.iter("file") if f.find("pathurl") is not None}
vt = seq.find("media/video/track"); clips = vt.findall("clipitem"); prev = 0
for c in clips:
    s, e, i, o = (int(c.findtext(k)) for k in ("start", "end", "in", "out"))
    dur = int(c.findtext("duration"))
    chk(s == prev, f"{c.get('id')}: buraco/sobreposição na timeline ({prev}->{s})"); prev = e
    chk(e - s == o - i, f"{c.get('id')}: duração timeline != fonte")
    chk(0 <= i and o <= dur, f"{c.get('id')}: fora da mídia ({i}-{o} de {dur})")
    chk(c.find("file").get("id") in files, f"{c.get('id')}: file sem definição")
chk(prev == cfg["duracao_final_f"], "duração total")
for t in vt.findall("transitionitem"):
    a, b, al = int(t.findtext("start")), int(t.findtext("end")), t.findtext("alignment")
    if al == "center":
        out_c = [c for c in clips if int(c.findtext("end")) == (a + b) // 2 or int(c.findtext("end")) in range(a, b + 1)][0]
        in_c = clips[clips.index(out_c) + 1]
        chk(int(out_c.findtext("out")) + (b - int(out_c.findtext("end"))) <= int(out_c.findtext("duration")), "handle saída")
        chk(int(in_c.findtext("in")) - (int(in_c.findtext("start")) - a) >= 0, "handle entrada")
for f in files.values():
    chk(f.findtext("pathurl").startswith("file://localhost/"), "pathurl")
    chk(not f.findtext("name").endswith(".mp4") or "Drop" in f.findtext("name"), f"proxy referenciado: {f.findtext('name')}")
for a in seq.findall("media/audio/track/clipitem"):
    chk(int(a.findtext("end")) == cfg["duracao_final_f"], "áudio com duração da sequência")
try:
    import opentimelineio as otio
    tl = otio.adapters.read_from_file(xml_p, adapter_name="fcp_xml")
    v = tl.video_tracks()[0]; au = tl.audio_tracks()
    print(f"OTIO: '{tl.name}' {len(list(v.find_clips()))} clipes de vídeo, {len(au)} trilhas de áudio, "
          f"duração {tl.duration().to_seconds():.3f}s")
except ImportError:
    print("OTIO não instalado: pulando leitura independente")
print("ERROS:", erros if erros else "nenhum")
sys.exit(1 if erros else 0)
