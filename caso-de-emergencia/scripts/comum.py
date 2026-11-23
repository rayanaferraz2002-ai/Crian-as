"""Utilidades compartilhadas pelos scripts de edição (caminhos, fps, tempo)."""
import json, os, subprocess
from fractions import Fraction
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent          # caso-de-emergencia/
ANALISE = PROJ / "analise"
FPS = Fraction(24000, 1001)                             # 23,976 (nativo dos clipes)
SEQ_W, SEQ_H = 1080, 1920                               # 9:16 (proporção da referência)
MUSICA = "Hit Me Back (feat. Phury) (Instrumental).mp4"
REFERENCIA = "snapinsta-1795455482487.mp4"


def midia_dir(arg=None):
    """Pasta com os ORIGINAIS (somente leitura). --src ou variável MIDIA."""
    d = arg or os.environ.get("MIDIA")
    if not d:
        raise SystemExit("Informe a pasta dos originais com --src ou MIDIA=...")
    return Path(d)


def s2f(sec):
    """segundos -> quadro (arredondado) a 23,976."""
    return int(round(Fraction(sec).limit_denominator(100000) * FPS))


def f2s(fr):
    return float(Fraction(fr) / FPS)


def tc(fr):
    """quadro -> timecode HH:MM:SS:FF (base 24, non-drop, como o Premiere mostra)."""
    ff = fr % 24; s = fr // 24
    return f"{s//3600:02d}:{s//60%60:02d}:{s%60:02d}:{ff:02d}"


def srt_tc(sec):
    ms = int(round(sec * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ffprobe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def rotacao(info):
    for st in info["streams"]:
        if st.get("codec_type") == "video":
            for sd in st.get("side_data_list", []):
                if "rotation" in sd:
                    return int(sd["rotation"])
            return int(st.get("tags", {}).get("rotate", 0))
    return 0


def ler_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def gravar_json(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
