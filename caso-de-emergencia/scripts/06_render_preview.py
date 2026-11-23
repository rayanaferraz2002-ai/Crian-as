"""Renderiza preview.mp4 (720x1280, leve) a partir de plano.json.
Usa proxies de análise (cria se faltar), abertura_tensao.mov, música com ducking, título e legendas.
Uso: python3 06_render_preview.py --src PASTA_ORIGINAIS --cache PASTA_PROXIES"""
import argparse, subprocess
from pathlib import Path
from comum import PROJ, FPS, MUSICA, midia_dir, ler_json, f2s

ap = argparse.ArgumentParser(); ap.add_argument("--src"); ap.add_argument("--cache", required=True)
ap.add_argument("--saida", default=str(PROJ / "preview.mp4")); a = ap.parse_args()
P = ler_json(PROJ / "plano.json"); src = midia_dir(a.src); cache = Path(a.cache); cache.mkdir(parents=True, exist_ok=True)
W, H = 720, 1280
R = f"{FPS.numerator}/{FPS.denominator}"
total = P["sequencia"]["duracao_quadros"]


def proxy(clipe):
    """proxy de análise 720 px (orientação já aplicada), mesmo fps e áudio."""
    out = cache / (Path(clipe).stem + "_720.mp4")
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src / clipe), "-vf", "scale=720:-2",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
    return out


entradas, idx = [], {}
def entrada(path):
    if str(path) not in idx:
        idx[str(path)] = len(entradas); entradas.append(str(path))
    return idx[str(path)]

fc, vlab = [], []
for i, v in enumerate(P["video"]):
    if v["papel"] == "abertura":
        k = entrada(PROJ / v["clipe"])
    else:
        k = entrada(proxy(v["clipe"]))
    z, ay = v["escala"], v["ancora_y"]
    zw = int(round(W * z / 2) * 2); zh = int(round(H * z / 2) * 2)
    fc.append(f"[{k}:v]trim=start_frame={v['src_in']}:end_frame={v['src_out']},setpts=PTS-STARTPTS,"
              f"scale={zw}:{zh},crop={W}:{H}:(iw-{W})/2:{ay}*(ih-{H}),setsar=1,fps={R},format=yuv420p[v{i}]")
    vlab.append(f"[v{i}]")
fq = P["fusoes"]["fim_para_preto_quadros"]
fc.append("".join(vlab) + f"concat=n={len(vlab)}:v=1:a=0,fade=t=out:start_frame={total-fq}:nb_frames={fq}[vcat]")

# ---- textos (ASS) ----
ass = cache / "textos.ass"
def t_ass(fr, fim=False):
    import math
    s = f2s(fr); s = (math.floor(s * 100) - (1 if fim else 0)) / 100 if fim else math.ceil(s * 100) / 100
    h = int(s // 3600); m = int(s // 60 % 60); return f"{h}:{m:02d}:{s%60:05.2f}"
linhas = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
          "[V4+ Styles]",
          "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV",
          "Style: Titulo,Inter ExtraBold,64,&H00FFFFFF,&H00000000,&H80000000,1,0,1,3,0,8,40,40,250",
          "Style: Legenda,Inter SemiBold,34,&H00FFFFFF,&H00000000,&H64000000,1,0,1,2.2,1,2,60,60,300",
          "", "[Events]", "Format: Layer, Start, End, Style, Text"]
for t in P["textos"]:
    estilo = "Titulo" if t["tipo"] == "titulo" else "Legenda"
    txt = t["texto"] if estilo == "Legenda" else r"{\fad(120,0)}" + t["texto"]
    linhas.append(f"Dialogue: 0,{t_ass(t['tl_in'])},{t_ass(t['tl_out'], fim=True)},{estilo},{txt}")
ass.write_text("\n".join(linhas), encoding="utf-8")
fc.append(f"[vcat]ass={ass}[vout]")

# ---- áudio: locução (trilha própria) + música com ducking ----
alab = []
for j, au in enumerate(P["audio"]):
    k = entrada(proxy(au["clipe"]))
    ms = int(round(f2s(au["tl_in"]) * 1000))
    fc.append(f"[{k}:a]atrim=start={f2s(au['src_in']):.5f}:end={f2s(au['src_out']):.5f},asetpts=PTS-STARTPTS,"
              f"afade=t=in:d=0.02,afade=t=out:st={f2s(au['src_out']-au['src_in'])-0.03:.4f}:d=0.03,"
              f"aresample=48000,aformat=channel_layouts=stereo,adelay={ms}:all=1[a{j}]")
    alab.append(f"[a{j}]")
fc.append("".join(alab) + f"amix=inputs={len(alab)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=7,"
          f"apad,atrim=end={f2s(total):.4f}[voz]")
mu = P["musica"]; km = entrada(src / MUSICA)
nv = [(f2s(n["quadro"]), n["ganho"]) for n in mu["niveis"]]
expr = str(nv[-1][1])
for (t0, g0), (t1, g1) in reversed(list(zip(nv, nv[1:]))):
    seg = f"{g0}" if g0 == g1 else f"({g0}+({g1}-{g0})*(t-{t0:.4f})/{max(t1-t0,1e-3):.4f})"
    expr = f"if(lt(t,{t1:.4f}),{seg},{expr})"
fc.append(f"[{km}:a]atrim=start={mu['entrada_s']}:duration={f2s(total):.4f},asetpts=PTS-STARTPTS,"
          f"aresample=48000,volume='{expr}':eval=frame[mus]")
fc.append("[voz][mus]amix=inputs=2:normalize=0,alimiter=limit=0.89[aout]")

cmd = ["ffmpeg", "-v", "error", "-y"]
for e in entradas:
    cmd += ["-i", e]
cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-r", R,
        "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart", "-t", f"{f2s(total):.4f}", a.saida]
subprocess.run(cmd, check=True)
print("ok:", a.saida)
