"""Renderiza abertura_tensao.mov (cena 1): P&B + câmera lenta + zoom crescente + contraste/vinheta crescentes + grão.
Lê os parâmetros de plano.json. Uso: python3 05_render_abertura.py --src PASTA [--perfil 3]  (ProRes: 0 proxy,1 LT,2 422,3 HQ)"""
import argparse, subprocess
from comum import PROJ, FPS, SEQ_W, SEQ_H, midia_dir, ler_json, f2s

ap = argparse.ArgumentParser(); ap.add_argument("--src"); ap.add_argument("--perfil", default="1")
ap.add_argument("--saida", default=str(PROJ / "abertura_tensao.mov")); a = ap.parse_args()
P = ler_json(PROJ / "plano.json"); ab = P["abertura"]; e = ab["efeito"]
n = ab["quadros"]; T = f2s(n); vel = ab["velocidade"]
ax, ay = e["ancora"]
W, H = int(SEQ_W * 1.2), int(SEQ_H * 1.2)          # margem = zoom máximo (1:1 no fim)
dz = e["zoom_fim"] - e["zoom_ini"]
vf = ",".join([
    f"trim=start={ab['src_in']}:end={ab['src_out']}", "setpts=PTS-STARTPTS",
    f"scale={W}:{H}:flags=lanczos",
    f"setpts=PTS/{vel}",                                                    # câmera lenta
    f"minterpolate=fps={FPS.numerator}/{FPS.denominator}:mi_mode=mci:mc_mode=aobmc:vsbmc=1",
    "tpad=stop_mode=clone:stop_duration=0.5",                                # garante o nº exato de quadros
    f"zoompan=z='{e['zoom_ini']}+{dz}*pow(on/{n-1},2)':x='(iw-iw/zoom)*{ax}':y='(ih-ih/zoom)*{ay}'"
    f":d=1:s={SEQ_W}x{SEQ_H}:fps={FPS.numerator}/{FPS.denominator}",
    "hue=s=0",                                                              # preto e branco
    f"eq=contrast='{e['contraste_ini']}+{e['contraste_fim']-e['contraste_ini']}*t/{T:.4f}':brightness={e['brilho']}:eval=frame",
    f"vignette=angle='{e['vinheta_ini']}+{e['vinheta_fim']-e['vinheta_ini']}*t/{T:.4f}':eval=frame",
    f"noise=alls={e['grao']}:allf=t+u",
    "format=yuv422p10le"])
cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(midia_dir(a.src) / ab["clipe"]), "-an", "-vf", vf,
       "-frames:v", str(n), "-c:v", "prores_ks", "-profile:v", a.perfil, "-vendor", "apl0",
       "-r", f"{FPS.numerator}/{FPS.denominator}", "-timecode", "00:00:00:00", a.saida]
subprocess.run(cmd, check=True)
print("ok:", a.saida, f"{n} quadros, velocidade {vel:.3f}")
